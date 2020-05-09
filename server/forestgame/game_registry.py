import uuid

from forestgame.game.world import World;  

class Player:
  def __init__(self, client_id, player_id):
    self._client_id = client_id;
    self.id = player_id;
    self.name = "Player " + player_id;

    self.population = 30;
    self.wood = 0;
    self.coin = 0;
    self.food = 60;

  def spend(self, amount):
    if amount == None:
      return;
    
    if "wood" in amount:
      self.wood -= amount["wood"];
    if "coin" in amount:
      self.coin -= amount["coin"];
    if "food" in amount:
      self.food -= amount["food"];

class Game:
    def __init__(self, id, host):
        self.id = id;
        self.host = host;
        self._players = {};
        self.world = World();

        self.add_player(host);

    def add_player(self, client_id):
      player = Player(client_id, str(len(self._players)));
      self._players[client_id] = player;
      return player

    def get_player_for_client_id(self, client_id):
      return self._players.get(client_id);

    def init_from_map(self, mapI, maxPlayers):
      self.world.set_size(mapI.sizeX, mapI.sizeY);

      for i in range(0, maxPlayers):
        playerStart = mapI.playerStarts[i];
        self.world.set_tile_at(playerStart[0], playerStart[1], 0)
        self.world.set_building_at(playerStart[0], playerStart[1], 0)
      
      for (x, y, tid) in mapI.mapData:
        self.world.set_tile_at(x, y, tid)
      
      # Move into game mode class
      hill = mapI.features["hill"]
      self.world.set_tile_at(hill[0], hill[1], 0)
      self.world.set_building_at(hill[0], hill[1], 2)

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