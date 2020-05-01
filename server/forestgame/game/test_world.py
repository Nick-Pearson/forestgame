import unittest

from forestgame.game.world import World;  

class WorldTest(unittest.TestCase):
  def test_world_inits_to_empty_data(self):
    world = World();

    self.assertEqual(0, world.get_size_x());
    self.assertEqual(0, world.get_size_y());
    self.assertEqual([], world.get_tile_data());

  def test_set_size_from_zero_initialsies_from_forest(self):
    world = World();

    world.set_size(3, 3);

    expectedTileData = [
      [1, 1, 1],
      [1, 1, 1],
      [1, 1, 1],
    ];
    self.assertEqual(expectedTileData, world.get_tile_data());
    self.assertEqual(3, world.get_size_x());
    self.assertEqual(3, world.get_size_y());

  def test_set_size_with_larger_x_y_pads_with_forest(self):
    world = World();
    world.set_size(2, 2);

    world.set_size(3, 3);

    expectedTileData = [
      [1, 1, 1],
      [1, 1, 1],
      [1, 1, 1],
    ];
    self.assertEqual(expectedTileData, world.get_tile_data());
    self.assertEqual(3, world.get_size_x());
    self.assertEqual(3, world.get_size_y());

  def test_set_size_with_larger_x_pads_with_forest(self):
    world = World();
    world.set_size(2, 3);

    world.set_size(3, 3);

    expectedTileData = [
      [1, 1, 1],
      [1, 1, 1],
      [1, 1, 1],
    ];
    self.assertEqual(expectedTileData, world.get_tile_data());
    self.assertEqual(3, world.get_size_x());
    self.assertEqual(3, world.get_size_y());

  def test_set_size_with_larger_y_pads_with_forest(self):
    world = World();
    world.set_size(3, 2);

    world.set_size(3, 3);

    expectedTileData = [
      [1, 1, 1],
      [1, 1, 1],
      [1, 1, 1],
    ];
    self.assertEqual(expectedTileData, world.get_tile_data());
    self.assertEqual(3, world.get_size_x());
    self.assertEqual(3, world.get_size_y());

  def test_set_size_with_smaller_x_y_removes_data(self):
    world = World();
    world.set_size(3, 3);

    world.set_size(2, 2);

    expectedTileData = [
      [1, 1],
      [1, 1],
    ];
    self.assertEqual(expectedTileData, world.get_tile_data());
    self.assertEqual(2, world.get_size_x());
    self.assertEqual(2, world.get_size_y());

  def test_set_size_with_smaller_x_removes_data(self):
    world = World();
    world.set_size(3, 3);

    world.set_size(2, 3);

    expectedTileData = [
      [1, 1],
      [1, 1],
      [1, 1],
    ];
    self.assertEqual(expectedTileData, world.get_tile_data());
    self.assertEqual(2, world.get_size_x());
    self.assertEqual(3, world.get_size_y());
  
  def test_set_size_with_smaller_y_removes_data(self):
    world = World();
    world.set_size(3, 3);

    world.set_size(3, 2);

    expectedTileData = [
      [1, 1, 1],
      [1, 1, 1],
    ];
    self.assertEqual(expectedTileData, world.get_tile_data());
    self.assertEqual(3, world.get_size_x());
    self.assertEqual(2, world.get_size_y());

  def test_set_size_with_same_x_y_does_nothing(self):
    world = World();
    world.set_size(3, 3);

    world.set_size(3, 3);

    expectedTileData = [
      [1, 1, 1],
      [1, 1, 1],
      [1, 1, 1],
    ];
    self.assertEqual(expectedTileData, world.get_tile_data());
    self.assertEqual(3, world.get_size_x());
    self.assertEqual(3, world.get_size_y());

  # set tile range checks

  def test_set_tile_changes_tile_data(self):
    world = World();
    world.set_size(5, 5);

    world.set_tile_at(2, 3, 0);

    self.assertEqual(0, world.get_tile_at(2, 3));
    expectedTileData = [
      [1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1],
      [1, 1, 0, 1, 1],
      [1, 1, 1, 1, 1]
    ];
    self.assertEqual(expectedTileData, world.get_tile_data());

