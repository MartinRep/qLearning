import qLearning


def main():
    ql = qLearning.Qlearning('agent1')
    actions = ql.actions
    res = ql.do_action(actions[0])
    print("result: {}".format(res))


if __name__ == "__main__":
    main()