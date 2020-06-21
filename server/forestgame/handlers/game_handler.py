from forestgame.handlers.handler_exceptions import ResourceNotFoundException
from forestgame.handlers.handler_exceptions import BadRequestException
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
    body = request.body
    if (
        ("map_id" not in body) or
        ("max_players" not in body) or
        (not isinstance(body["map_id"], str)) or
        (not isinstance(body["max_players"], int))
      ):
      raise BadRequestException("Invalid parameters")
      
    map_inst = get_map_for_id(body["map_id"])
    if map_inst is None:
      raise ResourceNotFoundException("Map not found: " + body["map_id"])

    if body["max_players"] < 0 or body["max_players"] > map_inst.max_players:
      raise BadRequestException("Invalid parameters")

    game = self.game_regsitry.create_game(request.client_id)
    game.init_from_map(map_inst, int(body["max_players"]))
    return {"game_id": game.game_id}

  def join_game(self, request):
    invite_code = request.path["invite_code"].upper()
    name = request.body.get("name")
    if name is None:
      raise BadRequestException("Invalid parameters")
    if not isinstance(name, str) or len(name) < 2:
      raise BadRequestException("Invalid player name")

    game = self.game_regsitry.get_game_for_invite_code(invite_code)
    if game is None:
      raise ResourceNotFoundException("Game not found")
    player = game.get_player_for_client_id(request.client_id)

    if player is None:
      if game.is_archived or not game.is_lobby:
        raise ResourceNotFoundException("Game not found")

      if game.num_players() >= game.max_players:
        raise BadRequestException("Game is full")

      player = game.add_player(request.client_id)
    
    player.name = name
    player.persist()

    return {"game_id": game.game_id}

  def get_world(self, request):
    game_id = request.path["game_id"]
    game = self.lookup_game(game_id)
    player = game.get_player_for_client_id(request.client_id)
    if player is None:
      raise ResourceNotFoundException("Game not found")

    world = game.get_world()

    return {
      "tileData": world.get_tile_data(),
      "buildings": [{'id': b["id"], 'owner_id': b["owner_id"], 'x': b["x"], 'y': b["y"]} for b in world.get_building_data()],
    }

  def get_players(self, request):
    game_id = request.path["game_id"]
    game = self.lookup_game(game_id)
    player = game.get_player_for_client_id(request.client_id)
    if player is None:
      raise ResourceNotFoundException("Game not found")

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
    player = game.get_player_for_client_id(request.client_id)
    if player is None:
      raise ResourceNotFoundException("Game not found")

    return {
      "game_id": game.game_id,
      "invite_code": game.invite_code,
      "state": "GAME",
      "max_players": game.max_players,
      "num_players": game.num_players(),
      "map_id": world.map_id,
      "game_mode_name": "King of the Hill",
    }

  def action_deforest(self, request):
    game_id = request.path["game_id"]
    coords = request.body
    game = self.lookup_game(game_id)
    player = game.get_player_for_client_id(request.client_id)
    if player is None:
      raise ResourceNotFoundException("Game not found")

    if ("x" not in coords) or ("y" not in coords) or (type(coords["x"]) != int) or (type(coords["y"]) != int):
      raise BadRequestException("Invalid parameters")

    world = game.get_world()
    world.set_tile_at(coords["x"], coords["y"], 2)
    world.persist()

    player.stats.wood += 10
    player.persist()

    return {}

  def action_build(self, request):
    game_id = request.path["game_id"]
    body = request.body
    if (
        ("x" not in body) or
        ("y" not in body) or
        ("building_id" not in body) or
        (not isinstance(body["x"], int)) or
        (not isinstance(body["y"], int)) or
        (not isinstance(body["building_id"], int))
      ):
      raise BadRequestException("Invalid parameters")

    x = body["x"]
    y = body["y"]
    building_id = body["building_id"]
    building = get_building_for_id(building_id)
    if building is None:
      raise ResourceNotFoundException("Building not found: " + str(building_id))

    game = self.lookup_game(game_id)
    world = game.get_world()
    player = game.get_player_for_client_id(request.client_id)
    if player is None:
      raise ResourceNotFoundException("Game not found")

    if not player.stats.has_enough(building["cost"]):
      raise BadRequestException("Not enough money")

    current_tile = world.get_tile_at(x, y)
    if current_tile != 0 and current_tile != 2:
      raise BadRequestException("Tile is not a clearing")

    if world.get_building_at(x, y) != None:
      raise BadRequestException("Tile already contains building")

    player.stats.spend(building["cost"])
    player.persist()
    world.set_building_at(x, y, building_id, player.player_id)
    world.set_tile_at(x, y, 0)
    world.persist()
    return {}
