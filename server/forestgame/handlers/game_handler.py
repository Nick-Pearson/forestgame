from forestgame.handlers.handler_exceptions import BadRequestException;
from forestgame.handlers.handler_exceptions import ResourceNotFoundException;

class GameHandler():
  def __init__(self, game_registry):
    self.game_regsitry = game_registry;

  def lookup_game(self, game_id, client_id):
    game = self.game_regsitry.get_game_for_id(game_id);
    if game == None:
      raise ResourceNotFoundException("Game not found");

    return game;