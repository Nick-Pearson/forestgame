class Map:
  def __init__(self, id, name, sizeX, sizeY, playerStarts, features):
    self.id = id;
    self.name = name;
    self.maxPlayers = len(playerStarts);
    self.sizeX = sizeX;
    self.sizeY = sizeY;
    self.playerStarts = playerStarts;
    self.features = features

quadrantPlayerStarts = [
  (10, 5),
  (30, 15),
  (10, 15),
  (30, 5),
];
quadrantFeatures = {
  "hill": (20, 10)
}

fourCornersStarts = [
  (0, 0),
  (29, 29),
  (0, 29),
  (29, 0),
];
fourCornersFeatures = {
  "hill": (15, 15)
}


MAPS = [
  Map("0",  "Quadrant", 41, 21, quadrantPlayerStarts, quadrantFeatures),
  Map("1", "4 Corners", 30, 30, fourCornersStarts, fourCornersFeatures)
];

def get_map_for_id(id):
  for m in MAPS:
    if m.id == id:
      return m;
  return None;