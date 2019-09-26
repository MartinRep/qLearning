(x, y) = (10, 10) # Grid parameters
actions = ["up", "down", "left", "right"]
start_position = (2, 2)
player = start_position
score = 0
restart = False
move_reward = -1
goal_reward = 10
walls = []
specials = [(6, 6, goal_reward)]

def restart_game():
    global player, score, restart
    player = start_position
    score = 0
    restart = False

def has_restarted():
    return restart

def try_move(delta_x, delta_y):
    global player, x, y, score, move_reward, restart
    if restart == True:
        restart_game()
    new_x = player[0] + delta_x
    new_y = player[1] + delta_y
    score += move_reward
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
        player = (new_x, new_y)
    for (x_pos, y_pos, square_reward) in specials:  # List through all the possible special squares. Target or possible Negative square
        if new_x == x_pos and new_y == y_pos:
            score -= move_reward
            score += square_reward
            if score > 0:
                print("Success! score: ", score)
            else:
                print("Fail! score: ", score)
            restart = True
            return
