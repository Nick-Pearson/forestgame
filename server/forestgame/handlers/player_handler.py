from handlers.handler_exceptions import BadRequestException;
from handlers.handler_exceptions import ResourceNotFoundException;

class PlayerHandler():
  def __init__(self, game_registry):
    self.game_regsitry = game_registry;

  def lookup_player(self, game_id, client_id):
    game = self.game_regsitry.get_game_for_id(game_id);
    if game == None:
      raise ResourceNotFoundException("Game not found");

    player = game.get_player_for_client_id(client_id);
    if player == None:
      raise ResourceNotFoundException("Game not found");

    return player;

  def change_name(self, request):
    new_name = request.body.get("name", None);
    game_id = request.path["game_id"];

    if new_name == None:
      raise BadRequestException("New name must be provided")
    if type(new_name) != str:
      raise BadRequestException("New name must be a string")
    if len(new_name) < 2:
      raise BadRequestException("New name must be at least 2 characters")

    player = self.lookup_player(game_id, request.client_id);
    player.name = new_name;
    return {"name": new_name};

  def get_name(self, request):
    game_id = request.path["game_id"];

    player = self.lookup_player(game_id, request.client_id);
    return {"name": player.name};
    
  def get_player_stats(self, request):
    game_id = request.path["game_id"];

    player = self.lookup_player(game_id, request.client_id);

    stats = {
        "population": player.population,
        "wood": player.wood,
        "coin": player.coin,
        "food": player.food
    };
    return {"stats": stats};