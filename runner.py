import qLearning
import json
import csv


def main():
    log = []

    # Initialization of QLearning
    ql = qLearning.Qlearning(e_decay = 0.96)
    for i in range(100):    # Number of episodes
        # Initial move
        agent, updated_q = ql.move()
        while(not agent['finished']):
            # DEV ONLY ------------------------------
            # print("Q updated: {}".format(updated_q))
            # input("press key to continue...")
            # ---------------------------------------
            # TODO implement sharing the new Q entry with other agents via bprotocol
            # updated_q = {'x': last_pos[0], 'y': last_pos[1], 'action': action, 'Q': newQ}
            agent, updated_q = ql.move()
        print("result: {}".format(ql.agent))
        log.append({'episode': i, 'score': agent['score'], 'steps': agent['steps']})
    
    with open('output/'+ ql.agent['name']+'.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['episode', 'score', 'steps'])
        writer.writeheader()
        for episode in log:
            writer.writerow(episode)


if __name__ == "__main__":
    main()