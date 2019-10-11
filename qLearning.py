import random
import csv
import requests
import time

class Qlearning:
    random.seed()
    
    def __init__(self, server = 'http://localhost:5100', alpha = 0.9, epsilon = 0.1, e_decay = 0.99, decay = True, gamma = 1, max_moves = 100, policy = 0.0):
        self.server = server
        while(self._server_info() is not True):     # Gets grid size and reward and penalties
           print("Getting Server Info was unsuccessful, trying in a second...")
           time.sleep(1)
        while(self._join() is not True):
           print("Joining Server was unsuccessful, trying in a second...")
           time.sleep(1) 
        self.alpha = alpha     # Rate of learning.
        self.decay = decay
        self.epsilon = epsilon   # Rate of exploration(0.1 = 10%). How often random action is chosen over the best action accorting to Qtable 
        self.e_decay = e_decay   # How long it takes to stop exloring and just follow the best route. 
        self.gamma = gamma # How soon you care to get reward. 1 anytime in future. 0 - looking for eminent reward 
        self.max_moves = max_moves # Maximum number of moves to restart the episode. (If goal is not found by this turn, it will restart)
        self.actions = ["up", "down", "left", "right"]
        self.policy = policy # Set to 0.1 for greedy policy
        self.log = []    
        self.states = []
        for i in range(self.grid_world['x']):
            for j in range(self.grid_world['y']):
                self.states.append((i, j))
        self.Q = {}
        for state in self.states:
            empty_q = {}
            for action in self.actions:
                empty_q[action] = self.policy 
            self.Q[state] = empty_q
        self.result = {}    # Results of an move/action taken

    def _server_info(self):
        try:
            result = requests.get(self.server + '/')
            if result.text == "False":
                return False
            self.grid_world = result.json()
            return True
        except:
            return False
    
    def _join(self):
        try:
            result = requests.get(self.server + '/join')
            if result.text == "False":
                return False
            self.agent = result.json()
            return True
        except:
            return False

    def move(self):
        last_pos = (self.agent['x'], self.agent['y'])
        action = self._next_action()
        if (self._move(action)): # If the move was successfully executed, update the Q table.
            newQ = self._updateQ(action, self.agent['latest_move'], last_pos)
            if self.agent['steps'] >= self.max_moves:
                result = requests.get(self.server + '/restart/' + self.agent['name'])
                if self.decay:
                    self._decay_all()
                self.agent = result.json()
            if self.agent['finished'] == True and self.decay:
                self._decay_all()
            # TODO logging and maybe implement alpha decay
            return self.agent, {'x': last_pos[0], 'y': last_pos[1], 'action': action, 'Q': newQ}
        return None

    # Return action with highest Q value
    def _max_Q(self, pos):
        curr_Qs = self.Q[pos]
        maxQ = curr_Qs[self.actions[0]]
        max_action = 0
        for i in range(1, len(self.actions)):
            if (curr_Qs[self.actions[i]] > maxQ):
                maxQ = curr_Qs[self.actions[i]]
                max_action = i
        return self.actions[max_action]
    
    # Return next action determined by epsilon
    def _next_action(self):
        if random.random() > self.epsilon:      # Exloration chance
            pos = (self.agent['x'], self.agent['y'])
            if not all(elem == self.Q[pos][self.actions[0]] for elem in self.Q[pos].values()):  # if all Qs in the position are the same, chose random direction instead.
                return self._max_Q(pos)
        return random.SystemRandom().choice(self.actions)
    
    def _move(self, action):
        try:
            if action == self.actions[0]:
                result = requests.get(self.server + '/move/' + self.agent['name'] + '?deltaX=0&deltaY=-1')
            elif action == self.actions[1]:
                result = requests.get(self.server + '/move/' + self.agent['name'] + '?deltaX=0&deltaY=1')
            elif action == self.actions[2]:
                result = requests.get(self.server + '/move/' + self.agent['name'] + '?deltaX=-1&deltaY=0')
            elif action == self.actions[3]:
                result = requests.get(self.server + '/move/' + self.agent['name'] + '?deltaX=1&deltaY=0')
            if result.text is not 'False':
                self.agent = result.json()     # Update agent with result for the current move
                return True
        except:    
            return False

    def _updateQ(self, action, reward, pos):
        self.Q[pos][action] += self.alpha*(float(reward) + (self.gamma*self.Q[(self.agent['x'], self.agent['y'])][self._max_Q((self.agent['x'], self.agent['y']))]) - self.Q[pos][action])
        return self.Q[pos][action]

    def get_Q(self):
        print(self.Q)
        return self.Q

    def _decay_all(self):
        self.epsilon *= self.epsilon*self.e_decay



