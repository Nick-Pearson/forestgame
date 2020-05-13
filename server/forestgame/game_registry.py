import uuid
import random

from forestgame.game.world import World;  

class Player:
  def __init__(self, client_id, player_id, colour):
    self.client_id = client_id;
    self.id = player_id;
    self.name = "Player " + player_id;
    self.colour = colour;

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

startingColours = [
  (204, 0, 0), # red
  (51, 102, 153), # blue
  (153, 0, 153), #purple
  (255, 153, 0), #orange
  (153, 102, 51), #brown
  (51, 102, 0) # green
];

inviteCodeChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
def generateInviteCode():
  return random.choice(inviteCodeChars) + random.choice(inviteCodeChars) + random.choice(inviteCodeChars) + random.choice(inviteCodeChars);

class Game:
    def __init__(self, id, host):
        self.id = id;
        self.host = host;
        self._players = {};
        self.world = World();
        self.inviteCode = generateInviteCode();

        self.add_player(host);

    def add_player(self, client_id):
      playerId = len(self._players);
      player = Player(client_id, str(playerId), startingColours[playerId % len(startingColours)]);
      self._players[client_id] = player;
      return player

    def get_player_for_client_id(self, client_id):
      return self._players.get(client_id);

    def get_all_players(self):
      return list(self._players.values());
    
    def num_players(self):
      return len(self._players);

    def init_from_map(self, mapI, maxPlayers):
      self.world.set_size(mapI.sizeX, mapI.sizeY);
      self.mapId = mapI.id;
      self.maxPlayers = maxPlayers;

      for i in range(0, maxPlayers):
        playerStart = mapI.playerStarts[i];
        self.world.set_tile_at(playerStart[0], playerStart[1], 0)
        self.world.set_building_at(playerStart[0], playerStart[1], 0, str(i))
      
      for (x, y, tid) in mapI.mapData:
        self.world.set_tile_at(x, y, tid)
      
      # Move into game mode class
      hill = mapI.features["hill"]
      self.world.set_tile_at(hill[0], hill[1], 0)
      self.world.set_building_at(hill[0], hill[1], 2, None)

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