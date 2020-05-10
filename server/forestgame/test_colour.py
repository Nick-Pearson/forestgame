import unittest

from forestgame.colour import colourToHex;

class ToHexTest(unittest.TestCase):
  def test_convert_solid_black(self):
    h = colourToHex((0, 0, 0));
    self.assertEqual(h, "#000000")

  def test_convert_solid_white(self):
    h = colourToHex((255, 255, 255));
    self.assertEqual(h, "#FFFFFF")

  def test_convert_solid_red(self):
    h = colourToHex((255, 0, 0));
    self.assertEqual(h, "#FF0000")

  def test_convert_solid_green(self):
    h = colourToHex((0, 255, 0));
    self.assertEqual(h, "#00FF00")
  
  def test_convert_solid_blue(self):
    h = colourToHex((0, 0, 255));
    self.assertEqual(h, "#0000FF")
  
  def test_convert_low_values(self):
    h = colourToHex((15, 15, 15));
    self.assertEqual(h, "#0F0F0F")