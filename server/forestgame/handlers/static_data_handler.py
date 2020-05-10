from forestgame.data.building_data import BUILDINGS;
from forestgame.data.map_data import MAPS, get_map_for_id;

from flask import send_file;
from io import BytesIO;
from PIL import Image, ImageDraw

def generate_thumbnail_for_map(mapI, maxPlayers):
  img = Image.new('RGB', (mapI.sizeX, mapI.sizeY), color = (19, 122, 20));
  pixels = img.load();

  maxPlayers = min(maxPlayers, len(mapI.playerStarts));
  for i in range(0, maxPlayers):
    playerStart = mapI.playerStarts[i]
    pixels[playerStart[0],playerStart[1]] = (255, 255, 255)

  for k in mapI.features:
    coords = mapI.features[k];
    pixels[coords[0], coords[1]] = (255, 0, 0)

  for (x, y, tid) in mapI.mapData:
    pixels[x, y] = (0, 0, 0)

  return img;

class StaticDataHandler():
  def get_buildings(self):
    return {"buildings": BUILDINGS};

  def get_maps(self):
    maps = [{"name": m.name, "id": m.id, "maxPlayers": m.maxPlayers} for m in MAPS];
    return {"maps": maps};

  def get_map_thumbnail(self, request):
    mapId = request.path["map_id"];
    mapI = get_map_for_id(mapId);
    maxPlayers = int(request.query.get("maxPlayers", "2"));
    image = generate_thumbnail_for_map(mapI, maxPlayers);

    output = BytesIO()
    image.save(output, format='PNG')
    output.seek(0, 0)

    return send_file(output, mimetype='image/png');

  