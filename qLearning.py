import random
import csv
import requests

# Q(S[t], A[t]) += alpha*(R[t+1] + gama * maxQ(S[t+1], A) - Q(S[t], A[t]))

class Qlearning:
    random.seed(0)
    
    def __init__(self, name, server = 'http://localhost:5100'):
        self.name = name
        self.server = server
        self.gamma = 1 # How soon you care to get reward. 1 anytime in future. 0 - looking for eminent reward 
        self.epsilon = 0.1   # Rate of exploration(0.1 = 10%). How often random action is chosen over the best action accorting to Qtable 
        self.e_decay = 0.9   # How long it takes to stop exloring and just follow the best route. 
        self.alpha = 0.1     # Rate og learning.
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
        self.E = {}
        for state in self.states:
            self.Q[state] = empty_q
            self.E[state] = empty_e

    def do_action(self, action):
        if action == self.actions[0]:
            result = requests.get(self.server + '/move/' + self.name + '?deltaX=0&deltaY=-2')
        elif action == self.actions[1]:
            result = requests.get('http://localhost:5100/move/' + self.name + '?deltaX=0&deltaY=1')
        elif action == self.actions[2]:
            result = requests.get('http://localhost:5100/move/' + self.name + '?deltaX=-1&deltaY=0')
        elif action == self.actions[3]:
            result = requests.get('http://localhost:5100/move/' + self.name + '?deltaX=1&deltaY=0')
        if result.text == 'False':
            return False
        else:
            return result.json()



#     else:
#         return
#     s2 = world.player
#     r += world.score
#     return s, action, r, s2


# def reset_E():
#     for state in states:
#         for action in actions:
#             E[state][action] = 0

# def max_Q(s):
#     val = None
#     act = None
#     for a, q in Q[s].items():
#         if val is None or (q > val):
#             val = q
#             act = a
#     return act, val


# def policy(s, eps=epsilon):
#     if random.random() > eps:
#         return max_Q(s)
#     else:
#         l = [(a, q) for a, q in Q[s].items()]
#         random.shuffle(l)
#         return random.choice(l)


# def inc_Q(s, a, alpha, inc):
#     Q[s][a] += alpha * inc * E[s][a]

# def main():
#     global gamma
#     global epsilon
#     global alpha
#     global log
#     score = 0
#     s1 = world.player
#     a1, q_val1 = policy(s1)
#     for episode_num in range(num_of_episodes):
#         steps = 0
#         score = 0
#         while not world.has_restarted():
#             # Do the action
#             (s1, a1, r1, s2) = do_action(a1)
#             score += r1

#             # Update Q
#             a2, q_val2 = policy(s2) # Change to max_Q(s2) for Greedy policy
#             a_best, q_best = max_Q(s2)
#             delta = r1 + gamma * q_best - Q[s1][a1]
#             E[s1][a1] = 1


#             for state in states:
#                 for action in actions:
#                     inc_Q(state, action, alpha, delta)
#                     if a_best == a2:
#                         E[state][action] *= gamma * e_decay
#                     else:
#                         E[state][action] = 0
#             # print('new q:', Q[s1][a1])
#             s1 = s2
#             a1 = a2
#             q_val1 = q_val2

#             steps += 1
#             if steps > max_moves:
#                 break

#         print("Steps: {}".format(steps))
#         world.restart_game()
#         reset_E()
#         log.append({'episode': episode_num, 'score': score, 'steps': steps, 'alpha': alpha, 'epsilon': 0})
#         alpha = max(0.1, pow(episode_num+1, -0.4))
#         epsilon = min(0.3, pow(episode_num+1, -1.2))

#     with open('output/log.csv', 'w') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=['episode', 'score', 'steps', 'alpha', 'epsilon'])
#         writer.writeheader()
#         for episode in log:
#             writer.writerow(episode)

# if __name__ == "__main__":
#     main()