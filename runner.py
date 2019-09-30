import qLearning


def main():
    log = []
    ql = qLearning.Qlearning()
    newQ = ql.move()
    # TODO implement sharing the new Q entry with other agents via bprotocol
    print("result: {}".format(newQ))

    
    # TODO implement logging
    # log.append({'episode': episode_num, 'score': score, 'steps': steps})
    #     with open('output/log.csv', 'w') as csvfile:
    #         writer = csv.DictWriter(csvfile, fieldnames=['episode', 'score', 'steps', 'alpha', 'epsilon'])
    #         writer.writeheader()
    #         for episode in log:
    #             writer.writerow(episode)


if __name__ == "__main__":
    main()