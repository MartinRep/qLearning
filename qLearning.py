import random
import csv
import requests
import time

# Q(S[t], A[t]) += alpha*(R[t+1] + gama * maxQ(S[t+1], A) - Q(S[t], A[t]))

class Qlearning:
    random.seed()
    
    def __init__(self, server = 'http://localhost:5100'):
        self.server = server
        while(self._join() is not True):
           print("Join unsuccessfull, trying in a second...")
           time.sleep(1) 
        self.gamma = 1 # How soon you care to get reward. 1 anytime in future. 0 - looking for eminent reward 
        self.epsilon = 0.1   # Rate of exploration(0.1 = 10%). How often random action is chosen over the best action accorting to Qtable 
        self.e_decay = 0.9   # How long it takes to stop exloring and just follow the best route. 
        self.alpha = 0.99     # Rate og learning.
        self.num_of_episodes = 1000
        self.max_moves = 100 # Maximum number of moves to restart the episode. (If goal is not found by this turn, it will restart)
        self.actions = ["up", "down", "left", "right"]
        self.grid = {'x': 10, 'y': 10}   # TODO - Fetch from world API
        self.policy = 0.0 # Set to 0.1 for greedy policy
        self.log = []    
        self.states = []
        for i in range(self.grid['x']):
            for j in range(self.grid['y']):
                self.states.append((i, j))
        empty_q = {}
        empty_e = {}
        for action in self.actions:
            empty_q[action] = self.policy 
            empty_e[action] = 0.0
        self.Q = {}
        for state in self.states:
            self.Q[state] = empty_q
        self.result = {}    # Results of an move/action taken

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
            if self.agent['steps'] >= 100:
                result = requests.get(self.server + '/restart/' + self.agent['name'])
                self.agent = result.json()
            # TODO Implement alpha and epsilon decay, logging
            return self.agent['finished'], {'x': last_pos[0], 'y': last_pos[1], 'action': action, 'Q': newQ}
        return None

    # Return action with highest Q value
    def _max_Q(self, pos):
        curr_Qs = self.Q[pos]
        maxQ = curr_Qs[self.actions[0]]
        max_action = 0
        for i in range(1,4):
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
        self.Q[pos][action] += self.alpha*(float(reward) + self.gamma*self.Q[pos][self._max_Q((self.agent['x'], self.agent['y']))] - self.Q[pos][action])
        return self.Q[pos][action]

    def get_Q(self):
        print(self.Q)
        return self.Q


#         
#         alpha = max(0.1, pow(episode_num+1, -0.4))
#         epsilon = min(0.3, pow(episode_num+1, -1.2))


