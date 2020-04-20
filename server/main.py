from flask import *

from forestgame.client_registry import ClientRegistry;
from forestgame.game_registry import GameRegistry;
from forestgame.request import Request;

from forestgame.handlers.player_handler import PlayerHandler;
from forestgame.handlers.handler_exceptions import HandlerException;

app = Flask(__name__)

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR

DIST_DIRECTORY = "../dist"

CLIENT_ID_COOKIE_KEY = "forestgame_client_id_token"
CLIENT_ID_COOKIE_EXPIRATION = 30 * DAY

client_registry = ClientRegistry()
game_registry = GameRegistry();

# add some testing fake data
game = game_registry.create_game("6ae9e011-55ce-47f2-86a5-4c713d0f94fe")
game.add_player("4a7f81c1-6803-4e25-bf97-33a71567afec");

playerHandler = PlayerHandler(game_registry);

def get_client_id_token(req):
    if CLIENT_ID_COOKIE_KEY in req.cookies:
        return req.cookies[CLIENT_ID_COOKIE_KEY]
    else:
        return client_registry.add_player().id

def set_client_id_token(resp, token):
    resp.set_cookie(CLIENT_ID_COOKIE_KEY, value=token, max_age=CLIENT_ID_COOKIE_EXPIRATION, httponly=True)

@app.route('/', defaults={'u_path': ''})
@app.route('/game/<path:u_path>')
def no_params_page(u_path):
    print("hello");
    player_id = get_client_id_token(request)

    response = send_from_directory(DIST_DIRECTORY, 'index.html')
    set_client_id_token(response, player_id)
    return response

@app.route('/game.js')
def static_script():
    return send_from_directory(DIST_DIRECTORY, 'game.js')

@app.route('/assets/<path:u_path>')
def static_assets(u_path):
    return send_file(DIST_DIRECTORY + '/assets/' + u_path)

@app.route('/api/game', methods = ["POST"])
def create_game():
    return { "game_id":"6ae9e011-55ce-47f2-86a5-4c713d0f94fe" }

def build_request(path):
    client_id = get_client_id_token(request);
    return Request(client_id, path, request.get_json());

def handle_exception(e):
    return {"message": e.message}, e.status

@app.route('/api/game/<game_id>/player-name', methods = ["PUT"])
def change_name(game_id):
    try:
        return playerHandler.change_name(build_request({"game_id": game_id}));
    except HandlerException as e:
        return handle_exception(e);


@app.route('/api/game/<game_id>/player-name', methods = ["GET"])
def get_name(game_id):
    try:
        return playerHandler.get_name(build_request({"game_id": game_id}));
    except HandlerException as e:
        return handle_exception(e);

@app.route('/api/game/<game_id>/player-stats', methods = ["GET"])
def get_player_stats(game_id):
    try:
        return playerHandler.get_player_stats(build_request({"game_id": game_id}));
    except HandlerException as e:
        return handle_exception(e);

@app.route('/api/game/<game_id>/world')
def get_world_data(game_id):
    return {
        "tileData": [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 2, 0, 2, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 0, 2, 2, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ],
        "buildings": [
            {
            "type": 0,
            "x": 7,
            "y": 6
            },
            {
            "type": 1,
            "x": 6,
            "y": 7
            }
        ]
    }

if __name__ == "__main__":
    print("Starting server");

    app.testing = True;
    app.run(debug=True);