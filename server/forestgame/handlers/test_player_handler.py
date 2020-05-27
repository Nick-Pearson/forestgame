import unittest

from forestgame.handlers.player_handler import PlayerHandler
from forestgame.handlers.handler_exceptions import BadRequestException
from forestgame.handlers.handler_exceptions import ResourceNotFoundException
from forestgame.game_registry import GameRegistry
from forestgame.request import Request

from forestgame.database.sql_database import generate_test_db

GAME_ID = "d01823a0-8667-41dc-a63f-0af11564fd87"
CLIENT_ID = "21fd7079-c7d8-48a7-8663-db924724f98e"

class PlayerNameTest(unittest.TestCase):
  def setUp(self):
    self.game_registry = GameRegistry(generate_test_db())
    self.handler = PlayerHandler(self.game_registry)

  def test_get_for_non_existant_game_returns_not_found(self):
    with self.assertRaises(ResourceNotFoundException) as context:
      self.handler.get_name(Request(CLIENT_ID, {"game_id": GAME_ID}))

    self.assertEqual("Game not found", context.exception.message)

  def test_get_for_existant_game_but_not_this_client_returns_not_found(self):
    self.game_registry.create_game("", GAME_ID)

    with self.assertRaises(ResourceNotFoundException) as context:
      self.handler.get_name(Request(CLIENT_ID, {"game_id": GAME_ID}))

    self.assertEqual("Game not found", context.exception.message)

  def test_get_returns_player_name(self):
    self.game_registry.create_game(CLIENT_ID, GAME_ID)

    get_resp = self.handler.get_name(Request(CLIENT_ID, {"game_id": GAME_ID}))

    self.assertEqual("Player 0", get_resp["name"])

  def test_put_for_non_existant_game_returns_not_found(self):
    with self.assertRaises(ResourceNotFoundException) as context:
      self.handler.change_name(Request(CLIENT_ID, {"game_id": GAME_ID}, {"name": "New Name"}))

    self.assertEqual("Game not found", context.exception.message)

  def test_put_for_existant_game_but_not_this_client_returns_not_found(self):
    self.game_registry.create_game("", GAME_ID)

    with self.assertRaises(ResourceNotFoundException) as context:
      self.handler.change_name(Request(CLIENT_ID, {"game_id": GAME_ID}, {"name": "New Name"}))

    self.assertEqual("Game not found", context.exception.message)

  def test_put_with_no_name_raises_bad_request(self):
    with self.assertRaises(BadRequestException) as context:
      self.handler.change_name(Request(CLIENT_ID, {"game_id": GAME_ID}, {}))

    self.assertEqual("New name must be provided", context.exception.message)

  def test_put_with_too_short_name_raises_bad_request(self):
    with self.assertRaises(BadRequestException) as context:
      self.handler.change_name(Request(CLIENT_ID, {"game_id": GAME_ID}, {"name": "a"}))

    self.assertEqual("New name must be at least 2 characters", context.exception.message)

  def test_put_with_non_string_name_raises_bad_request(self):
    with self.assertRaises(BadRequestException) as context:
      self.handler.change_name(Request(CLIENT_ID, {"game_id": GAME_ID}, {"name": 1234}))

    self.assertEqual("New name must be a string", context.exception.message)

  def test_put_changes_name_and_returns_new_name(self):
    self.game_registry.create_game(CLIENT_ID, GAME_ID)

    put_resp = self.handler.change_name(Request(CLIENT_ID, {"game_id": GAME_ID}, {"name": "New Name"}))

    self.assertEqual("New Name", put_resp["name"])
    get_resp = self.handler.get_name(Request(CLIENT_ID, {"game_id": GAME_ID}, None))
    self.assertEqual("New Name", get_resp["name"])

class PlayerStatsTest(unittest.TestCase):
  def setUp(self):
    self.db = generate_test_db()
    self.game_registry = GameRegistry(self.db)
    self.handler = PlayerHandler(self.game_registry)

  def test_get_for_non_existant_game_returns_not_found(self):
    with self.assertRaises(ResourceNotFoundException) as context:
      self.handler.get_player_stats(Request(CLIENT_ID, {"game_id": GAME_ID}))

    self.assertEqual("Game not found", context.exception.message)

  def test_get_for_existant_game_but_not_this_client_returns_not_found(self):
    self.game_registry.create_game("", GAME_ID)

    with self.assertRaises(ResourceNotFoundException) as context:
      self.handler.get_player_stats(Request(CLIENT_ID, {"game_id": GAME_ID}))

    self.assertEqual("Game not found", context.exception.message)

  def test_get_stats_returns_current_stats(self):
    game = self.game_registry.create_game(CLIENT_ID, GAME_ID)
    player = game.get_player_for_client_id(CLIENT_ID)
    player.stats.population = 10
    player.stats.wood = 20
    player.stats.coin = 30
    player.stats.food = 40
    player.persist()

    get_resp = self.handler.get_player_stats(Request(CLIENT_ID, {"game_id": GAME_ID}))

    stats = get_resp["stats"]
    self.assertEqual(10, stats["population"])
    self.assertEqual(20, stats["wood"])
    self.assertEqual(30, stats["coin"])
    self.assertEqual(40, stats["food"])
