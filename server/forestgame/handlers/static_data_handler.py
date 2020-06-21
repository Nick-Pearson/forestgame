from io import BytesIO

from flask import send_file
from PIL import Image

from forestgame.handlers.handler_exceptions import ResourceNotFoundException
from forestgame.data.building_data import BUILDINGS
from forestgame.data.map_data import MAPS, get_map_for_id

def generate_thumbnail_for_map(map_instance, max_players):
  img = Image.new('RGB', (map_instance.size_x, map_instance.size_y), color=(19, 122, 20))
  pixels = img.load()

  max_players = min(max_players, len(map_instance.player_starts))
  for i in range(0, max_players):
    player_start = map_instance.player_starts[i]
    pixels[player_start[0], player_start[1]] = (255, 255, 255)

  for k in map_instance.features:
    coords = map_instance.features[k]
    pixels[coords[0], coords[1]] = (255, 0, 0)

  for data in map_instance.map_data:
    pixels[data[0], data[1]] = (0, 0, 0)

  return img

class StaticDataHandler():
  def get_buildings(self):
    return {"buildings": BUILDINGS}

  def get_maps(self):
    maps = [{"name": map_inst.name, "id": map_inst.map_id, "max_players": map_inst.max_players} for map_inst in MAPS]
    return {"maps": maps}

  def get_map_thumbnail(self, request):
    map_id = request.path["map_id"]
    map_instance = get_map_for_id(map_id)
    if map_instance is None:
      raise ResourceNotFoundException("Map not found")
    
    max_players = int(request.query.get("max_players", "2"))
    image = generate_thumbnail_for_map(map_instance, max_players)

    output = BytesIO()
    image.save(output, format='PNG')
    output.seek(0, 0)

    return send_file(output, mimetype='image/png')

  def get_map(self, request):
    map_id = request.path["map_id"]
    map_instance = get_map_for_id(map_id)
    if map_instance is None:
      raise ResourceNotFoundException("Map not found")

    return {"name": map_instance.name, "id": map_instance.map_id, "max_players": map_instance.max_players}
