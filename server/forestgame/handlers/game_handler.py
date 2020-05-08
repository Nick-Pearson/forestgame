from forestgame.handlers.handler_exceptions import BadRequestException;
from forestgame.handlers.handler_exceptions import ResourceNotFoundException;
from forestgame.data.building_data import get_building_for_id;

class GameHandler():
  def __init__(self, game_registry):
    self.game_regsitry = game_registry;

  def lookup_game(self, game_id, client_id):
    game = self.game_regsitry.get_game_for_id(game_id);
    if game == None:
      raise ResourceNotFoundException("Game not found");

    return game;

  def create_game(self, request):
    game = self.game_regsitry.create_game(request.client_id);
    return {"game_id": game.id};

  def get_world(self, request):
    game_id = request.path["game_id"];
    game = self.lookup_game(game_id, request.client_id);

    return {
      "tileData": game.world.get_tile_data(),
      "buildings": game.world.get_building_data(),
    };

  def action_deforest(self, request):
    game_id = request.path["game_id"];
    coords = request.body;
    game = self.lookup_game(game_id, request.client_id);
    
    game.world.set_tile_at(coords["x"], coords["y"], 2);

    player = game.get_player_for_client_id(request.client_id);
    player.wood += 10;

    return {};

  def action_build(self, request):
    game_id = request.path["game_id"];
    body = request.body;
    x = body["x"];
    y = body["y"];
    buildingId = body["buildingId"];
    building = get_building_for_id(buildingId);
    game = self.lookup_game(game_id, request.client_id);

    player = game.get_player_for_client_id(request.client_id);
    player.spend(building["cost"]);
    game.world.set_building_at(x, y, buildingId);
    game.world.set_tile_at(x, y, 0);
    return {};