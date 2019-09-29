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

grid = {'x': 10, 'y': 10}
move_reward = -1
goal_reward = 10
walls = []      # Tumble (X, y) for wall position
specials = [(6, 6, goal_reward, True)]    # Tumble (x, y, square_reward, square finished episode?)

start_pos = [{'name': 'agent1', 'x': 0, 'y': 0},
             {'name': 'agent2', 'x': 1, 'y': 1},
             {'name': 'agent3', 'x': 2, 'y': 2},
             {'name': 'agent4', 'x': 3, 'y': 3},]

agents = [{'name': 'agent1', 'x': 0, 'y':0, 'score': 0, 'finished': False},
            {'name': 'agent2', 'x': 1, 'y':1, 'score': 0, 'finished': False},
            {'name': 'agent3', 'x': 2, 'y':2, 'score': 0, 'finished': False},
            {'name': 'agent4', 'x': 3, 'y':3, 'score': 0, 'finished': False},]

@app.route("/move/<agentID>")
def try_move(agentID):
    if request.args.get('deltaX') is None or request.args.get('deltaY') is None:
        return Response(status=400)
    delta_x = int(request.args.get('deltaX'))
    delta_y = int(request.args.get('deltaY'))
    agent = next((item for item in agents if item["name"] == agentID), False)
    if agent is False:
        return Response(status=400)
    if agent['finished'] == True:
        st = next((item for item in start_pos if item["name"] == agentID))
        agent['x'] = st['x']
        agent['y'] = st['y']
        agent['score'] = 0
    new_x = agent['x'] + delta_x
    new_y = agent['y'] + delta_y
    agent['score'] += move_reward
    print(agent)
    if (new_x < 0) or (new_x == grid['x']) or (new_y < 0) or (new_y == grid['y']) or ((new_x, new_y) in walls): # agent moved outside the frid or into wall. No change of position, but still get move_reward
        return jsonify(agent)
    agent['x'] = new_x
    agent['y'] = new_y
    for (x, y, reward, finished) in specials:
        if (agent['x'], agent['y']) == (x,y):
            agent['score'] += reward
            agent['finished'] = finished
            break
    return jsonify(agent)


app.run(port=5100)
