import uuid

from forestgame.game.world import World;  

class Player:
  def __init__(self, client_id, player_id):
    self._client_id = client_id;
    self.id = player_id;
    self.name = "Player " + player_id;

    self.population = 0;
    self.wood = 0;
    self.coin = 0;
    self.food = 0;

class Game:
    def __init__(self, id, host):
        self.id = id;
        self.host = host;
        self._players = {};
        self.world = World();
        self.world.set_size(40, 20);

        self.add_player(host);

    def add_player(self, client_id):
      player = Player(client_id, str(len(self._players)));
      self._players[client_id] = player;
      return player

    def get_player_for_client_id(self, client_id):
      return self._players.get(client_id);

class GameRegistry:
    def __init__(self):
      self._games = {};

    def get_game_for_id(self, id):
      return self._games.get(id, None);

    def create_game(self, host, id=None):
      if id == None:
        id = str(uuid.uuid4())
      
      game = Game(id, host);
      self._games[id] = game;
      return game;