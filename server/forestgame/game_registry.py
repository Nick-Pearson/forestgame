import uuid
import random
import time

from forestgame.game.world import World

class Stats:
  def __init__(self, population, wood, coin, food):
    self.population = population
    self.wood = wood
    self.coin = coin
    self.food = food

  def spend(self, amount):
    if amount is None:
      return

    if "wood" in amount:
      self.wood -= amount["wood"]
    if "coin" in amount:
      self.coin -= amount["coin"]
    if "food" in amount:
      self.food -= amount["food"]

class Player:
  def __init__(self, client_id, player_id, colour, name, stats):
    self.client_id = client_id
    self.player_id = player_id
    self.colour = colour
    self.name = name
    self.stats = stats

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
  def __init__(self, game_id, host, players, max_players, world_uuid, invite_code, is_lobby, is_archived):
    self.game_id = game_id
    self.host = host
    self._players = players
    self.max_players = max_players
    self.world_uuid = world_uuid
    self.invite_code = invite_code
    self.is_lobby = is_lobby
    self.is_archived = is_archived

  def add_player(self, client_id):
    if client_id in self._players:
      return

    player_idx = len(self._players)
    colour = startingColours[player_idx % len(startingColours)]
    player = Player(client_id, player_idx, colour, "Player " + str(player_idx), Stats(30, 0, 0, 60))
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

  def insert_to_db(self, db):
    db.execute("""
      INSERT INTO game (uuid,
                        create_datetime,
                        host_uuid,
                        invite_code,
                        is_lobby,
                        is_archived,
                        max_players,
                        world_uuid)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
               (self.game_id,
                int(time.time()),
                self.host,
                self.invite_code,
                self.is_lobby,
                self.is_archived,
                self.max_players,
                self.world_uuid))

class GameRegistry:
  def __init__(self, db):
    self.db = db

  def __get_game_from_db(self, where, params):
    db_result = self.db.query("SELECT uuid, host_uuid, max_players, world_uuid, invite_code, is_lobby, is_archived FROM game " + where, params)
    if len(db_result) == 0:
      return None
    row = db_result[0]
    game_id = str(row[0])

    db_result = self.db.query("""SELECT client_uuid, player_idx, name, colour_r, colour_g, colour_b, population, wood, coin, food
                                FROM game_player WHERE game_uuid=%s""", (game_id, ))
    return Game(game_id, str(row[1]), {}, int(row[2]), str(row[3]), str(row[4]), bool(row[5]), bool(row[6]))

  def get_game_for_id(self, game_id):
    return self.__get_game_from_db("WHERE uuid=%s", (game_id, ))

  def get_game_for_invite_code(self, code):
    return self.__get_game_from_db("WHERE invite_code=%s", (code, ))

  def create_game(self, host, game_id=None):
    if game_id is None:
      game_id = str(uuid.uuid4())

    game = Game(game_id, host, {}, 0, str(uuid.uuid4()), generate_invite_code(), True, False)
    game.insert_to_db(self.db)
    game.add_player(host)
    return game
