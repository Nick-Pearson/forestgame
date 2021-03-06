class Map:
  def __init__(self, map_id, name, size_x, size_y, player_starts, features, map_data):
    self.map_id = map_id
    self.name = name
    self.max_players = len(player_starts)
    self.size_x = size_x
    self.size_y = size_y
    self.player_starts = player_starts
    self.features = features
    self.map_data = map_data

quadrantplayer_starts = [
  (10, 5),
  (30, 15),
  (10, 15),
  (30, 5),
]
quadrantFeatures = {
  "hill": (20, 10)
}

fourCornersStarts = [
  (0, 0),
  (15, 15),
  (0, 15),
  (15, 0),
]
fourCornersFeatures = {
  "hill": (7, 7)
}

mountainWallStarts = [
  (5, 3),
  (5, 15),
  (13, 3),
  (13, 15),
]
mountainWallFeatures = {
  "hill": (9, 9)
}
mountainWallmap_data = [
  (5, 7, 3),
  (5, 6, 3),
  (6, 6, 3),
  (7, 6, 3),
  (8, 6, 3),
  (9, 6, 3),
  (10, 6, 3),
  (11, 6, 3),
  (12, 6, 3),
  (13, 6, 3),
  (13, 7, 3),

  (5, 11, 3),
  (5, 12, 3),
  (6, 12, 3),
  (7, 12, 3),
  (8, 12, 3),
  (9, 12, 3),
  (10, 12, 3),
  (11, 12, 3),
  (12, 12, 3),
  (13, 12, 3),
  (13, 11, 3),
]

MAPS = [
  Map("2", "Mountain Wall", 19, 19, mountainWallStarts, mountainWallFeatures, mountainWallmap_data),
  Map("0", "Quadrant", 41, 21, quadrantplayer_starts, quadrantFeatures, []),
  Map("1", "4 Corners", 16, 16, fourCornersStarts, fourCornersFeatures, []),
]

def get_map_for_id(map_id):
  for map_instance in MAPS:
    if map_instance.map_id == map_id:
      return map_instance
  return None
