from forestgame.handlers.handler_exceptions import BadRequestException;
from forestgame.handlers.handler_exceptions import ResourceNotFoundException;
from forestgame.data.building_data import get_building_for_id;
from forestgame.data.map_data import get_map_for_id;

from forestgame.colour import colourToHex;

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
    mapI = get_map_for_id(request.body["mapId"]);
    game.init_from_map(mapI, int(request.body["maxPlayers"]));
    return {"game_id": game.id};

  def get_world(self, request):
    game_id = request.path["game_id"];
    game = self.lookup_game(game_id, request.client_id);

    return {
      "tileData": game.world.get_tile_data(),
      "buildings": game.world.get_building_data(),
    };

  def get_players(self, request):
    game_id = request.path["game_id"];
    game = self.lookup_game(game_id, request.client_id);

    players = game.get_all_players();

    return {
      "players": [
        {
          "id": p.id,
          "me": p.client_id == request.client_id,
          "colour": colourToHex(p.colour),
          "name": p.name,
        }
        for p in players
      ],
    };

  def get_game_data(self, request):
    game_id = request.path["game_id"];
    game = self.lookup_game(game_id, request.client_id);

    mapI = get_map_for_id(game.mapId);
    return {
      "gameId": game.id,
      "inviteCode": game.inviteCode,
      "state": "GAME",
      "maxPlayers": game.maxPlayers,
      "numPlayers": game.num_players(),
      "mapId": game.mapId,
      "gameModeName": "King of the Hill",
    }

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
    game.world.set_building_at(x, y, buildingId, player.id);
    game.world.set_tile_at(x, y, 0);
    return {};