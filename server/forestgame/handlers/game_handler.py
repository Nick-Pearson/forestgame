from forestgame.handlers.handler_exceptions import ResourceNotFoundException
from forestgame.data.building_data import get_building_for_id
from forestgame.data.map_data import get_map_for_id

from forestgame.colour import colour_to_hex

class GameHandler():
  def __init__(self, game_registry):
    self.game_regsitry = game_registry

  def lookup_game(self, game_id):
    game = self.game_regsitry.get_game_for_id(game_id)
    if game is None:
      raise ResourceNotFoundException("Game not found")

    return game

  def create_game(self, request):
    game = self.game_regsitry.create_game(request.client_id)
    map_inst = get_map_for_id(request.body["map_id"])
    game.init_from_map(map_inst, int(request.body["max_players"]))
    return {"game_id": game.game_id}

  def join_game(self, request):
    invite_code = request.path["invite_code"].upper()
    name = request.body.get("name")
    game = self.game_regsitry.get_game_for_invite_code(invite_code)
    player = game.add_player(request.client_id)
    player.name = name
    return {"game_id": game.game_id}

  def get_world(self, request):
    game_id = request.path["game_id"]
    game = self.lookup_game(game_id)
    world = game.get_world()

    return {
      "tileData": world.get_tile_data(),
      "buildings": [{'id': b["id"], 'owner_id': b["owner_id"], 'x': b["x"], 'y': b["y"]} for b in world.get_building_data()],
    }

  def get_players(self, request):
    game_id = request.path["game_id"]
    game = self.lookup_game(game_id)

    players = game.get_all_players()

    return {
      "players": [
        {
          "id": str(p.player_id),
          "me": p.client_id == request.client_id,
          "colour": colour_to_hex(p.colour),
          "name": p.name,
        }
        for p in players
      ],
    }

  def get_game_data(self, request):
    game_id = request.path["game_id"]
    game = self.lookup_game(game_id)
    world = game.get_world()

    return {
      "game_id": game.game_id,
      "inviteCode": game.invite_code,
      "state": "GAME",
      "max_players": game.max_players,
      "numPlayers": game.num_players(),
      "map_id": world.map_id,
      "gameModeName": "King of the Hill",
    }

  def action_deforest(self, request):
    game_id = request.path["game_id"]
    coords = request.body
    game = self.lookup_game(game_id)

    world = game.get_world()
    world.set_tile_at(coords["x"], coords["y"], 2)
    world.persist()

    player = game.get_player_for_client_id(request.client_id)
    player.stats.wood += 10
    player.persist()

    return {}

  def action_build(self, request):
    game_id = request.path["game_id"]
    body = request.body
    x = body["x"]
    y = body["y"]
    building_id = body["building_id"]
    building = get_building_for_id(building_id)
    game = self.lookup_game(game_id)

    player = game.get_player_for_client_id(request.client_id)
    player.stats.spend(building["cost"])
    player.persist()
    world = game.get_world()
    world.set_building_at(x, y, building_id, player.player_id)
    world.set_tile_at(x, y, 0)
    world.persist()
    return {}
