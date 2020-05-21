import unittest

from forestgame.colour import colour_to_hex

class ToHexTest(unittest.TestCase):
  def test_convert_solid_black(self):
    hex_code = colour_to_hex((0, 0, 0))
    self.assertEqual(hex_code, "#000000")

  def test_convert_solid_whex_codeite(self):
    hex_code = colour_to_hex((255, 255, 255))
    self.assertEqual(hex_code, "#FFFFFF")

  def test_convert_solid_red(self):
    hex_code = colour_to_hex((255, 0, 0))
    self.assertEqual(hex_code, "#FF0000")

  def test_convert_solid_green(self):
    hex_code = colour_to_hex((0, 255, 0))
    self.assertEqual(hex_code, "#00FF00")

  def test_convert_solid_blue(self):
    hex_code = colour_to_hex((0, 0, 255))
    self.assertEqual(hex_code, "#0000FF")

  def test_convert_low_values(self):
    hex_code = colour_to_hex((15, 15, 15))
    self.assertEqual(hex_code, "#0F0F0F")
