# Simple Flask application so all other agents can share the same world.

# World should hold: 
# - Grid size
# - Walls
# - Actions Enumerables list
# - Squares rewards
# - Move penalty
# - agents (dictionary - agents = {'name': 'agent1', 'x': 0, 'y':0, 'score': 0, 'finished': False})

# End points:
# GET, '/move<agentID>' + deltaX, deltaY -  return agent object (name,x, y, score, finished)


from flask import Flask, request, Response, jsonify

app = Flask(__name__)

grid_world = {'x': 10, 'y': 10, 'move_penalty': -1, 'goal_reward': 10}
walls = []      # Tumble (X, y) for wall position
specials = [(6, 6, grid_world['goal_reward'], True)]    # Tumble (x, y, square_reward, square finished episode?)

start_pos = [{'name': 'agent1', 'x': 0, 'y': 0},
             {'name': 'agent2', 'x': 1, 'y': 1},
             {'name': 'agent3', 'x': 2, 'y': 2},
             {'name': 'agent4', 'x': 3, 'y': 3},]

agents = [{'name': 'agent1', 'x': 0, 'y':0, 'latest_move': 0, 'score': 0, 'finished': False},
          {'name': 'agent2', 'x': 1, 'y':1, 'latest_move': 0, 'score': 0, 'finished': False},
          {'name': 'agent3', 'x': 2, 'y':2, 'latest_move': 0, 'score': 0, 'finished': False},
          {'name': 'agent4', 'x': 3, 'y':3, 'latest_move': 0, 'score': 0, 'finished': False},]

@app.route("/move/<agentID>")
def try_move(agentID):
    global agents
    if request.args.get('deltaX') is None or request.args.get('deltaY') is None:    # checks for incomplete request
        return "False"
    try:
        delta_x = int(request.args.get('deltaX'))
        delta_y = int(request.args.get('deltaY'))
    except:     # checks for integers
        return "False"
    if((delta_x is not 0 and delta_y is not 0) or (delta_x is 0 and delta_y is 0) or delta_x not in [-1,1] or delta_y not in [-1, 1]): # checks for ilegal moves
        return "False"
    agent = next((item for item in agents if item["name"] == agentID), False)
    if agent is False:
        return "False"
    if agent['finished'] == True:
        st = next((item for item in start_pos if item["name"] == agentID))
        agent['x'] = st['x']
        agent['y'] = st['y']
        agent['score'] = 0
        agent['latest_move'] = 0
    new_x = agent['x'] + delta_x
    new_y = agent['y'] + delta_y
    agent['latest_move'] = grid_world['move_penalty']
    print(agent)
    if (new_x < 0) or (new_x == grid_world['x']) or (new_y < 0) or (new_y == grid_world['y']) or ((new_x, new_y) in walls): # agent moved outside the grid or into wall. No change of position, but still get move_reward
        return jsonify(agent)
    agent['x'] = new_x
    agent['y'] = new_y
    for (x, y, grid_reward, finished) in specials:
        if (agent['x'], agent['y']) == (x,y):
            agent['latest_move'] += grid_reward
            agent['score'] += agent['latest_move']
            agent['finished'] = finished
            break
    return jsonify(agent)


@app.route("/")
def summary():
    return jsonify( grid_world, agents)

app.run(port=5100)
