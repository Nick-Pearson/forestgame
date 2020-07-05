import json

from flask import Flask, request, abort, send_file, send_from_directory
from flask_socketio import SocketIO, join_room

from forestgame.database.sql_database import SQLDatabase
from forestgame.database.sql_connections import InMemoryConnectionFactory, PostgresConnectionFactory

from forestgame.client_registry import ClientRegistry
from forestgame.game_registry import GameRegistry
from forestgame.request import Request

from forestgame.game.event_system import EventSystem

from forestgame.handlers.player_handler import PlayerHandler
from forestgame.handlers.game_handler import GameHandler
from forestgame.handlers.static_data_handler import StaticDataHandler
from forestgame.handlers.handler_exceptions import HandlerException

from forestgame.data.map_data import get_map_for_id

from settings import load_settings

settings = load_settings()
print("Loaded settings")
print(json.dumps(settings, indent=1))

DIST_DIRECTORY = "../dist"
fapp = Flask(__name__, template_folder=DIST_DIRECTORY + '/templates')
fapp.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(fapp)

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR


CLIENT_ID_COOKIE_KEY = "forestgame_client_id_token"
CLIENT_ID_COOKIE_EXPIRATION = 30 * DAY

if settings["runMemoryDatabase"]:
  factory = InMemoryConnectionFactory()
  c = factory.get_conn()
  database = SQLDatabase(factory)
else:
  database = SQLDatabase(PostgresConnectionFactory(settings["databaseUrl"]))

client_registry = ClientRegistry(database)
game_registry = GameRegistry(database)

event_system = EventSystem()

playerHandler = PlayerHandler(game_registry)
gameHandler = GameHandler(game_registry, event_system)
staticDataHandler = StaticDataHandler()

def get_client_id_token(req, refresh_client):
  if CLIENT_ID_COOKIE_KEY in req.cookies:
    client_uuid = req.cookies[CLIENT_ID_COOKIE_KEY]
    if refresh_client:
      client_registry.refresh_client(client_uuid)
    return client_uuid
  else:
    return client_registry.add_client(req.headers.get('User-Agent')).client_id

def set_client_id_token(resp, token):
  resp.set_cookie(CLIENT_ID_COOKIE_KEY, value=token, max_age=CLIENT_ID_COOKIE_EXPIRATION, httponly=True)

@fapp.route('/', defaults={'u_path': ''})
@fapp.route('/<path:u_path>')
@fapp.route('/game/<path:u_path>')
def no_params_page(u_path):
  if u_path.startswith('api'):
    abort(404)

  client_id = get_client_id_token(request, len(u_path) == 0)

  response = send_from_directory(DIST_DIRECTORY, 'index.html')
  set_client_id_token(response, client_id)
  return response

@fapp.route('/game.js')
def static_script():
  return send_from_directory(DIST_DIRECTORY, 'game.js')

def build_request(path):
  client_id = get_client_id_token(request, False)
  return Request(client_id, path, request.get_json(), request.args)

def handle_exception(e):
  return {"message": e.message}, e.status

@fapp.route('/api/buildings')
def get_buildings():
  try:
    return staticDataHandler.get_buildings()
  except HandlerException as e:
    return handle_exception(e)

@fapp.route('/api/maps')
def get_all_maps():
  try:
    return staticDataHandler.get_maps()
  except HandlerException as e:
    return handle_exception(e)

@fapp.route('/api/maps/<map_id>')
def get_single_map(map_id):
  try:
    return staticDataHandler.get_map(build_request({"map_id": map_id}))
  except HandlerException as e:
    return handle_exception(e)

@fapp.route('/api/maps/<map_id>/thumbnail')
def get_maps_thumbnail(map_id):
  try:
    return staticDataHandler.get_map_thumbnail(build_request({"map_id": map_id}))
  except HandlerException as e:
    return handle_exception(e)

@fapp.route('/api/game/<game_id>/player-name', methods=["PUT"])
def change_name(game_id):
  try:
    return playerHandler.change_name(build_request({"game_id": game_id}))
  except HandlerException as e:
    return handle_exception(e)

@fapp.route('/api/game/<game_id>/player-name', methods=["GET"])
def get_name(game_id):
  try:
    return playerHandler.get_name(build_request({"game_id": game_id}))
  except HandlerException as e:
    return handle_exception(e)

@fapp.route('/api/game/<game_id>/player-stats', methods=["GET"])
def get_player_stats(game_id):
  try:
    return playerHandler.get_player_stats(build_request({"game_id": game_id}))
  except HandlerException as e:
    return handle_exception(e)

@fapp.route('/api/game/<game_id>/players', methods=["GET"])
def get_players(game_id):
  try:
    return gameHandler.get_players(build_request({"game_id": game_id}))
  except HandlerException as e:
    return handle_exception(e)

@fapp.route('/api/game', methods=["POST"])
def create_game():
  try:
    return gameHandler.create_game(build_request({}))
  except HandlerException as e:
    return handle_exception(e)

@fapp.route('/api/game/<game_id>/start', methods=["POST"])
def start_game(game_id):
  try:
    return gameHandler.start_game(build_request({"game_id": game_id}))
  except HandlerException as e:
    return handle_exception(e)

@fapp.route('/api/invite/<invite_code>/players', methods=["POST"])
def join_game(invite_code):
  try:
    return gameHandler.join_game(build_request({"invite_code": invite_code}))
  except HandlerException as e:
    return handle_exception(e)

@fapp.route('/api/game/<game_id>')
def get_game_data(game_id):
  try:
    return gameHandler.get_game_data(build_request({"game_id": game_id}))
  except HandlerException as e:
    return handle_exception(e)

@fapp.route('/api/game/<game_id>/world')
def get_world_data(game_id):
  try:
    return gameHandler.get_world(build_request({"game_id": game_id}))
  except HandlerException as e:
    return handle_exception(e)

@fapp.route('/api/game/<game_id>/actions/deforest', methods=["POST"])
def action_deforest(game_id):
  try:
    return gameHandler.action_deforest(build_request({"game_id": game_id}))
  except HandlerException as e:
    return handle_exception(e)

@fapp.route('/api/game/<game_id>/actions/build', methods=["POST"])
def action_build(game_id):
  try:
    return gameHandler.action_build(build_request({"game_id": game_id}))
  except HandlerException as e:
    return handle_exception(e)

@socketio.on('subscribe')
def on_join(data):
  room = data['game_id']
  join_room(room)
  print("Joining room for game " + room)

if __name__ == "__main__":
  print("Starting server")

  @fapp.route('/assets/<path:u_path>')
  def static_assets(u_path):
    return send_file(DIST_DIRECTORY + '/assets/' + u_path)

  if settings["debug"]:
    # add some testing fake data
    print("Adding fake data")
    game = game_registry.create_game("4a7f81c1-6803-4e25-bf97-33a71567afec", "6ae9e011-55ce-47f2-86a5-4c713d0f94fe")
    game.init_from_map(get_map_for_id("2"), 4)
    game.add_player('1')
    fapp.testing = True

  socketio.run(fapp, host='0.0.0.0', debug=settings["debug"], port=settings["port"])
