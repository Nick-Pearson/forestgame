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
  def __init__(self, db, game_id, client_id, player_id, colour, name, stats):
    self.db = db
    self.game_id = game_id
    self.client_id = client_id
    self.player_id = player_id
    self.colour = colour
    self.name = name
    self.stats = stats

  def insert_to_db(self):
    self.db.execute("""
      INSERT INTO game_player (game_uuid,
                                client_uuid,
                                player_idx,
                                name,
                                colour_r,
                                colour_g,
                                colour_b,
                                population,
                                wood,
                                coin,
                                food)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
               (self.game_id,
                self.client_id,
                self.player_id,
                self.name,
                self.colour[0],
                self.colour[1],
                self.colour[2],
                self.stats.population,
                self.stats.wood,
                self.stats.coin,
                self.stats.food))

  def persist(self):
    self.db.execute("""
      UPDATE game_player SET name=%s,
                          colour_r=%s,
                          colour_g=%s,
                          colour_b=%s,
                          population=%s,
                          wood=%s,
                          coin=%s,
                          food=%s
                    WHERE game_uuid=%s AND client_uuid=%s AND player_idx=%s""",
               (self.name,
                self.colour[0],
                self.colour[1],
                self.colour[2],
                self.stats.population,
                self.stats.wood,
                self.stats.coin,
                self.stats.food,
                self.game_id,
                self.client_id,
                self.player_id))

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
  def __init__(self, db, game_id, host, players, max_players, world_uuid, invite_code, is_lobby, is_archived):
    self.db = db
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
    player = Player(self.db, self.game_id, client_id, player_idx, colour, "Player " + str(player_idx), Stats(30, 0, 0, 60))
    player.insert_to_db()
    self._players[client_id] = player
    return player

  def get_player_for_client_id(self, client_id):
    return self._players.get(client_id)

  def get_all_players(self):
    return list(self._players.values())

  def num_players(self):
    return len(self._players)

  def get_world(self):
    db_result = self.db.query("SELECT map_id, size_x, size_y FROM world WHERE uuid=%s", (self.world_uuid, ))
    tile_db_results = self.db.query("SELECT x, y, tile_id FROM world_tile WHERE world_uuid=%s", (self.world_uuid, ))
    row = db_result[0]
    return World(self.db, self.world_uuid, row[0], row[1], row[2], tile_db_results, [])

  def init_from_map(self, map_inst, max_players):
    world = self.get_world()
    world.set_size(map_inst.size_x, map_inst.size_y)
    self.max_players = max_players

    for i in range(0, max_players):
      player_start = map_inst.player_starts[i]
      world.set_tile_at(player_start[0], player_start[1], 0)
      world.set_building_at(player_start[0], player_start[1], 0, str(i))

    for (x, y, tid) in map_inst.map_data:
      world.set_tile_at(x, y, tid)

    # Move into game mode class
    hill = map_inst.features["hill"]
    world.set_tile_at(hill[0], hill[1], 0)
    world.set_building_at(hill[0], hill[1], 2, None)

    world.persist()
    self.persist()

  def insert_to_db(self):
    self.db.execute("""
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

  def persist(self):
    self.db.execute("""
      UPDATE game SET is_lobby=%s,
                  is_archived=%s,
                  max_players=%s
                  WHERE uuid=%s""",
               (self.is_lobby,
                self.is_archived,
                self.max_players,
                self.game_id))

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
    players = {}
    for player_row in db_result:
      client_uuid = player_row[0]
      colour = (player_row[3], player_row[4], player_row[5])
      stats = Stats(player_row[6], player_row[7], player_row[8], player_row[9])

      players[client_uuid] = Player(self.db, game_id, client_uuid, player_row[1], colour, player_row[2], stats)

    return Game(self.db, game_id, str(row[1]), players, int(row[2]), str(row[3]), str(row[4]), bool(row[5]), bool(row[6]))

  def get_game_for_id(self, game_id):
    return self.__get_game_from_db("WHERE uuid=%s", (game_id, ))

  def get_game_for_invite_code(self, code):
    return self.__get_game_from_db("WHERE invite_code=%s", (code, ))

  def create_game(self, host, game_id=None):
    if game_id is None:
      game_id = str(uuid.uuid4())

    world_uuid = str(uuid.uuid4())
    world = World(self.db, world_uuid, "0", 0, 0, [], [])
    world.insert_to_db()
    game = Game(self.db, game_id, host, {}, 0, world_uuid, generate_invite_code(), True, False)
    game.insert_to_db()
    game.add_player(host)
    return game
