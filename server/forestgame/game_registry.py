import uuid
import random

from forestgame.game.world import World

class Player:
  def __init__(self, client_id, player_id, colour):
    self.client_id = client_id
    self.player_id = player_id
    self.name = "Player " + player_id
    self.colour = colour

    self.population = 30
    self.wood = 0
    self.coin = 0
    self.food = 60

  def spend(self, amount):
    if amount is None:
      return

    if "wood" in amount:
      self.wood -= amount["wood"]
    if "coin" in amount:
      self.coin -= amount["coin"]
    if "food" in amount:
      self.food -= amount["food"]

startingColours = [
  (204, 0, 0), # red
  (51, 102, 153), # blue
  (153, 0, 153), #purple
  (255, 153, 0), #orange
  (153, 102, 51), #brown
  (51, 102, 0) # green
]

INVITE_CODE_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def generate_invite_code():
  return random.choice(INVITE_CODE_CHARS) + random.choice(INVITE_CODE_CHARS) + random.choice(INVITE_CODE_CHARS) + random.choice(INVITE_CODE_CHARS)

class Game:
  def __init__(self, game_id, host):
    self.game_id = game_id
    self.host = host
    self._players = {}
    self.world = World()
    self.map_id = ""
    self.max_players = 0
    self.invite_code = generate_invite_code()

    self.add_player(host)

  def add_player(self, client_id):
    if client_id in self._players:
      return

    player_id = len(self._players)
    player = Player(client_id, str(player_id), startingColours[player_id % len(startingColours)])
    self._players[client_id] = player
    return player

  def get_player_for_client_id(self, client_id):
    return self._players.get(client_id)

  def get_all_players(self):
    return list(self._players.values())

  def num_players(self):
    return len(self._players)

  def init_from_map(self, map_inst, max_players):
    self.world.set_size(map_inst.size_x, map_inst.size_y)
    self.map_id = map_inst.map_id
    self.max_players = max_players

    for i in range(0, max_players):
      player_start = map_inst.player_starts[i]
      self.world.set_tile_at(player_start[0], player_start[1], 0)
      self.world.set_building_at(player_start[0], player_start[1], 0, str(i))

    for (x, y, tid) in map_inst.map_data:
      self.world.set_tile_at(x, y, tid)

    # Move into game mode class
    hill = map_inst.features["hill"]
    self.world.set_tile_at(hill[0], hill[1], 0)
    self.world.set_building_at(hill[0], hill[1], 2, None)

class GameRegistry:
  def __init__(self):
    self._games = {}

  def get_game_for_id(self, game_id):
    return self._games.get(game_id, None)

  def get_game_for_invite_code(self, code):
    for game_id in self._games:
      game = self._games[game_id]
      if game.invite_code == code:
        return game
    return None


  def create_game(self, host, game_id=None):
    if game_id is None:
      game_id = str(uuid.uuid4())

    game = Game(game_id, host)
    self._games[game_id] = game
    return game
