(x, y) = (5, 5) # Grid parameters
actions = ["up", "down", "left", "right"]
start_position = (0, y-1)
player = start_position
score = 1
restart = False
move_reward = -0.04
walls = []
specials = [(4, 0, score)]

def restart_game():
    global player, score, restart
    player = start_position
    score = 1
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
