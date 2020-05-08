from forestgame.data.building_data import BUILDINGS;
from forestgame.data.map_data import MAPS;

class StaticDataHandler():
  def get_buildings(self):
    return {"buildings": BUILDINGS};

  def get_maps(self):
    maps = [{"name": m.name, "id": m.id, "maxPlayers": m.maxPlayers} for m in MAPS];
    return {"maps": maps};

  def get_map_thumbnail(self):
    return 