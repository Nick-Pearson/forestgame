import unittest

from forestgame.handlers.game_handler import GameHandler
from forestgame.game_registry import GameRegistry
from forestgame.request import Request
from forestgame.data.map_data import Map

from forestgame.database.sql_database import generate_test_db

GAME_ID = "9ced424f-91c2-47b2-a8ea-6a4bb38f2d2b"
CLIENT_ID = "6fb8d67c-fee3-437d-9d08-05c27d8a9d15"

class GameWorldTest(unittest.TestCase):
  def setUp(self):
    self.game_registry = GameRegistry(generate_test_db())
    self.handler = GameHandler(self.game_registry)

  #missing game
  #missing player from game

  def test_get_world_with_initialised_data(self):
    game = self.game_registry.create_game(CLIENT_ID, GAME_ID)
    world = game.get_world()
    world.set_size(5, 5)
    world.persist()

    resp = self.handler.get_world(Request(CLIENT_ID, {"game_id": GAME_ID}))

    expected_tiles = [
      [1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1],
    ]
    self.assertEqual(expected_tiles, resp["tileData"])

class DeforestTest(unittest.TestCase):
  def setUp(self):
    self.game_registry = GameRegistry(generate_test_db())
    self.handler = GameHandler(self.game_registry)

  #missing game
  #missing player from game
  #non int
  #missing data

  def test_deforest_removes_forest_for_that_tile_and_increments_player_wood(self):
    game = self.game_registry.create_game(CLIENT_ID, GAME_ID)
    world = game.get_world()
    world.set_size(5, 5)
    world.persist()

    resp = self.handler.action_deforest(Request(CLIENT_ID, {"game_id": GAME_ID}, {"x": 0, "y": 0}))

    self.assertEqual(resp, {})
    game = self.game_registry.get_game_for_id(GAME_ID)
    player = game.get_player_for_client_id(CLIENT_ID)
    self.assertEqual(10, player.stats.wood)
    resp = self.handler.get_world(Request(CLIENT_ID, {"game_id": GAME_ID}))
    expected_tiles = [
      [2, 1, 1, 1, 1],
      [1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1],
    ]
    self.assertEqual(expected_tiles, resp["tileData"])

class BuildTest(unittest.TestCase):
  def setUp(self):
    self.game_registry = GameRegistry(generate_test_db())
    self.handler = GameHandler(self.game_registry)

  #missing game
  #missing player from game
  #invalid building id
  #not a clearing
  #already building there
  #not enough money

  def test_build_removes_clearing_for_that_tile_and_sets_building_and_decrements_player_resource(self):
    game = self.game_registry.create_game(CLIENT_ID, GAME_ID)
    world = game.get_world()
    world.set_size(5, 5)
    world.set_tile_at(0, 0, 2)
    world.persist()
    player = game.get_player_for_client_id(CLIENT_ID)
    player.stats.wood = 40
    player.persist()

    resp = self.handler.action_build(Request(CLIENT_ID, {"game_id": GAME_ID}, {"x": 0, "y": 0, "building_id": 1}))

    self.assertEqual(resp, {})
    game = self.game_registry.get_game_for_id(GAME_ID)
    player = game.get_player_for_client_id(CLIENT_ID)
    self.assertEqual(20, player.stats.wood)
    resp = self.handler.get_world(Request(CLIENT_ID, {"game_id": GAME_ID}))
    expected_tiles = [
      [0, 1, 1, 1, 1],
      [1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1],
    ]
    self.assertEqual(expected_tiles, resp["tileData"])
    expected_buildings = [
      {"x": 0, "y": 0, "id": 1, "owner_id": "0"}
    ]
    self.assertEqual(expected_buildings, resp["buildings"])


class CreateGameTest(unittest.TestCase):
  def setUp(self):
    self.game_registry = GameRegistry(generate_test_db())
    self.handler = GameHandler(self.game_registry)

  #missing game
  #missing player from game
  #client is none of the players
  #missing data in request

  def test_create_game_adds_game_to_registrty_with_that_id(self):
    resp = self.handler.create_game(Request(CLIENT_ID, {}, {"map_id": "0", "max_players": "2"}))

    game = self.game_registry.get_game_for_id(resp["game_id"])
    self.assertNotEqual(None, game)
    player = game.get_player_for_client_id(CLIENT_ID)
    self.assertNotEqual(None, player)
    self.assertEqual(CLIENT_ID, game.host)

class GetPlayersTest(unittest.TestCase):
  def setUp(self):
    self.game_registry = GameRegistry(generate_test_db())
    self.handler = GameHandler(self.game_registry)

  # game not found
  # client not in game

  def test_get_players_returns_players_with_ids_and_colours(self):
    game = self.game_registry.create_game(CLIENT_ID, GAME_ID)
    player = game.get_player_for_client_id(CLIENT_ID)
    player.colour = (255, 0, 0)
    player.persist()
    player = game.add_player("6fb8d67c-fee3-437d-9d08-05c27d8a9d16")
    player.colour = (0, 255, 0)
    player.persist()
    player = game.add_player("6fb8d67c-fee3-437d-9d08-05c27d8a9d17")
    player.colour = (0, 0, 255)
    player.persist()
    player = game.add_player("6fb8d67c-fee3-437d-9d08-05c27d8a9d18")
    player.colour = (255, 255, 0)
    player.persist()

    resp = self.handler.get_players(Request(CLIENT_ID, {"game_id": GAME_ID}))

    players = resp["players"]
    self.assertEqual(4, len(players))
    self.assertEqual("0", players[0]["id"])
    self.assertEqual("#FF0000", players[0]["colour"])
    self.assertEqual(True, players[0]["me"])
    self.assertEqual("1", players[1]["id"])
    self.assertEqual("#00FF00", players[1]["colour"])
    self.assertEqual(False, players[1]["me"])
    self.assertEqual("2", players[2]["id"])
    self.assertEqual("#0000FF", players[2]["colour"])
    self.assertEqual(False, players[2]["me"])
    self.assertEqual("3", players[3]["id"])
    self.assertEqual("#FFFF00", players[3]["colour"])
    self.assertEqual(False, players[3]["me"])

class GameDataTest(unittest.TestCase):
  def setUp(self):
    self.game_registry = GameRegistry(generate_test_db())
    self.handler = GameHandler(self.game_registry)

  # game not found
  # client not in game

  def test_get_game_data_returns_info(self):
    game = self.game_registry.create_game(CLIENT_ID, GAME_ID)
    map_inst = Map("0", "My Map", 10, 10, [(0, 0), (1, 1), (2, 2), (3, 3)], {"hill": (0, 0)}, [])
    game.init_from_map(map_inst, 4)

    resp = self.handler.get_game_data(Request(CLIENT_ID, {"game_id": GAME_ID}))

    self.assertEqual(GAME_ID, resp["game_id"])
    self.assertEqual(4, resp["max_players"])
    self.assertEqual(1, resp["numPlayers"])
    self.assertEqual("0", resp["map_id"])
    self.assertEqual("King of the Hill", resp["gameModeName"])

class JoinGameTest(unittest.TestCase):
  def setUp(self):
    self.game_registry = GameRegistry(generate_test_db())
    self.handler = GameHandler(self.game_registry)

  # game not found
  # game exists but not joinable
  # name not given
  # invalid player name
  # player name already taken?
  # game joinable but user is banned from game
  # player already in game
  # already at max number players

  def test_join_game_that_exists_returns_game_id(self):
    game = self.game_registry.create_game(CLIENT_ID, GAME_ID)

    resp = self.handler.join_game(Request("6fb8d67c-fee3-437d-9d08-05c27d8a9d16", {"invite_code": game.invite_code}))

    self.assertEqual(game.game_id, resp["game_id"])
