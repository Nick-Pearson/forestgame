from flask import *

from client_registry import ClientRegistry;

app = Flask(__name__)

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR

CLIENT_ID_COOKIE_KEY = "forestgame_client_id_token"
CLIENT_ID_COOKIE_EXPIRATION = 30 * DAY

registry = ClientRegistry()

def get_client_id_token(req):
    if CLIENT_ID_COOKIE_KEY in req.cookies:
        return req.cookies[CLIENT_ID_COOKIE_KEY]
    else:
        return registry.add_player().id

def set_client_id_token(resp, token):
    resp.set_cookie(CLIENT_ID_COOKIE_KEY, value=token, max_age=CLIENT_ID_COOKIE_EXPIRATION, httponly=True)

@app.route('/', defaults={'u_path': ''})
@app.route('/game/<path:u_path>')
def no_params_page(u_path):
    player_id = get_client_id_token(request)

    response = send_from_directory('../dist', 'index.html')
    set_client_id_token(response, player_id)
    return response

@app.route('/game.js')
def static_script():
    return send_from_directory('../dist', 'game.js')

@app.route('/assets/<path:u_path>')
def static_assets(u_path):
    return send_file('../dist/assets/' + u_path)

@app.route('/api/game', methods = ["POST"])
def create_game():
    return { "game_id":"6ae9e011-55ce-47f2-86a5-4c713d0f94fe" }

@app.route('/api/game/<game_id>/player-name', methods = ["PUT"])
def change_name(game_id):
    return {}

if __name__ == "__main__":
    print("Starting server");

    app.testing = True;
    app.run(debug=True);