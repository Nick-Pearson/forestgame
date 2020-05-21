
def colour_to_hex(colour):
  r = '{:02x}'.format(colour[0])
  g = '{:02x}'.format(colour[1])
  b = '{:02x}'.format(colour[2])
  return ('#' + r + g + b).upper()
