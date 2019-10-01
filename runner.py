import qLearning
import json


def main():
    log = []
    ql = qLearning.Qlearning()
    finished, newQ = ql.move()
    # TODO implement sharing the new Q entry with other agents via bprotocol
    
    for i in range(100):
        finished, newQ = ql.move()
        while(not finished):
            # print("result: {}".format(newQ))
            # input("press key to continue...")
            finished, newQ = ql.move()   
        print("result: {}".format(ql.agent))
    
    
    # TODO implement logging
    # log.append({'episode': episode_num, 'score': score, 'steps': steps})
    #     with open('output/log.csv', 'w') as csvfile:
    #         writer = csv.DictWriter(csvfile, fieldnames=['episode', 'score', 'steps', 'alpha', 'epsilon'])
    #         writer.writeheader()
    #         for episode in log:
    #             writer.writerow(episode)


if __name__ == "__main__":
    main()