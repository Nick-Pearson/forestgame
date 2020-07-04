import unittest

from flask import Flask

from forestgame.handlers.static_data_handler import StaticDataHandler
from forestgame.handlers.handler_exceptions import ResourceNotFoundException
from forestgame.request import Request

CLIENT_ID = "21fd7079-c7d8-48a7-8663-db924724f98e"

class GetBuildingsTest(unittest.TestCase):
  def setUp(self):
    self.handler = StaticDataHandler()

  def test_get_buildings(self):
    resp = self.handler.get_buildings()

    buildings = resp.get("buildings")
    self.assertIsNotNone(buildings)

class GetMapsTest(unittest.TestCase):
  def setUp(self):
    self.handler = StaticDataHandler()

  def test_get_maps(self):
    resp = self.handler.get_maps()

    maps = resp.get("maps")
    self.assertIsNotNone(maps)

class GetMapThumbnailTest(unittest.TestCase):
  def setUp(self):
    self.handler = StaticDataHandler()

  def test_get_for_existing_map(self):
    app = Flask(__name__)
    with app.test_request_context():
      resp = self.handler.get_map_thumbnail(Request(CLIENT_ID, {"map_id": "1"}))

    self.assertIsNotNone(resp)

  def test_get_for_non_existing_map_returns_not_found(self):
    with self.assertRaises(ResourceNotFoundException) as context:
      self.handler.get_map_thumbnail(Request(CLIENT_ID, {"map_id": "-1"}))

    self.assertEqual("Map not found", context.exception.message)

class GetMapTest(unittest.TestCase):
  def setUp(self):
    self.handler = StaticDataHandler()

  def test_get_for_existing_map(self):
    resp = self.handler.get_map(Request(CLIENT_ID, {"map_id": "1"}))

    self.assertIsNotNone(resp)

  def test_get_for_non_existing_map_returns_not_found(self):
    with self.assertRaises(ResourceNotFoundException) as context:
      self.handler.get_map(Request(CLIENT_ID, {"map_id": "-1"}))

    self.assertEqual("Map not found", context.exception.message)
