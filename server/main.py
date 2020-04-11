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

@app.route('/', methods = ["GET"])
@app.route('/create-game', methods = ["GET"])
@app.route('/index.html', methods = ["GET"])
def root_html():
    player_id = get_client_id_token(request)

    response = send_from_directory('../dist', 'index.html')
    set_client_id_token(response, player_id)
    return response

@app.route('/game.js', methods = ["GET"])
def static_script():
    return send_from_directory('../dist', 'game.js')

if __name__ == "__main__":
    print("Starting server");

    app.testing = True;
    app.run(debug=True);