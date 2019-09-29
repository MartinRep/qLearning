import random
import csv

random.seed(0)

gamma = 1
epsilon = 0.1
e_decay = 0
alpha = 0.1
num_of_episodes = 1000
max_moves = 100
actions = ["up", "down", "left", "right"]
grid = {'x': 10, 'y': 10}   # TODO - Fetch from world API

log = []
states = []

policy = 0.0 # Set to 0.1 for greedy policy
for i in range(grid['x']):
    for j in range(grid['y']):
        states.append((i, j))

empty_q = {}
empty_e = {}
for action in actions:
    empty_q[action] = policy 
    empty_e[action] = 0.0
Q = {}
E = {}
for state in states:
    Q[state] = empty_q
    E[state] = empty_e

# for (i, j, w) in world.specials:
#     for action in actions:
#         Q[(i, j)][action] = w


# def do_action(action):
#     s = world.player
#     r = -world.score
#     if action == actions[0]:
#         world.try_move(0, -1)
#     elif action == actions[1]:
#         world.try_move(0, 1)
#     elif action == actions[2]:
#         world.try_move(-1, 0)
#     elif action == actions[3]:
#         world.try_move(1, 0)
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