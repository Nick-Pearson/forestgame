

class World:
  def __init__(self, db, world_uuid, map_id, size_x, size_y, tile_changes, building_data):
    self.db = db
    self.__world_uuid = world_uuid
    self.map_id = map_id
    self.__size_x = 0
    self.__size_y = 0
    self.__tile_data = []
    self.__tile_changes = []
    self.__building_data = building_data
    self.set_size(size_x, size_y)

    for tile in tile_changes:
      self.__tile_data[tile[1]][tile[0]] = tile[2]

  def set_size(self, x, y):
    if y > self.__size_y:
      diff = y - self.__size_y
      self.__tile_data = self.__tile_data + [[1] * self.__size_x] * diff
    elif y < self.__size_y:
      self.__tile_data = self.__tile_data[:y]

    if x > self.__size_x:
      diff = x - self.__size_x
      for i in range(0, len(self.__tile_data)):
        self.__tile_data[i] = self.__tile_data[i] + [1] * diff
    elif x < self.__size_x:
      for i in range(0, len(self.__tile_data)):
        self.__tile_data[i] = self.__tile_data[i][:x]

    self.__size_x = x
    self.__size_y = y

  def set_tile_at(self, x, y, tile_id):
    old = self.__tile_data[y][x]
    if tile_id == old:
      return

    self.__tile_data[y][x] = tile_id

    if old == 1:
      self.__tile_changes.append((False, x, y))
    else:
      self.__tile_changes.append((True, x, y))

  def get_tile_at(self, x, y):
    return self.__tile_data[y][x]

  def set_building_at(self, x, y, building_id, owner_id):
    self.__building_data.append({
      "in_db": False,
      "x": x,
      "y": y,
      "id": building_id,
      "owner_id": owner_id,
    })

  def get_building_at(self, x, y):
    for building in self.__building_data:
      if building["x"] == x and building["y"] == y:
        return building

    return None

  def get_size_x(self):
    return self.__size_x

  def get_size_y(self):
    return self.__size_y

  def get_tile_data(self):
    return self.__tile_data

  def get_building_data(self):
    return self.__building_data

  def insert_to_db(self):
    self.db.execute("""
      INSERT INTO world (uuid,
                        map_id,
                        size_x,
                        size_y)
                    VALUES (%s, %s, %s, %s)""",
                    (self.__world_uuid,
                     self.map_id,
                     self.__size_x,
                     self.__size_y))

  def persist(self):
    self.db.execute("""
      UPDATE world SET map_id=%s,
                        size_x=%s,
                        size_y=%s
                    WHERE uuid=%s""",
                    (self.map_id,
                     self.__size_x,
                     self.__size_y,
                     self.__world_uuid))
    self.__persist_tiles()
    self.__persist_buildings()

  def __persist_tiles(self):
    for change in self.__tile_changes:
      exists = change[0]
      x = change[1]
      y = change[2]

      if exists:
        self.db.execute("""
          UPDATE world_tile SET tile_id=%s 
                            WHERE world_uuid=%s AND x=%s AND y=%s""",
                        (self.__tile_data[y][x],
                         self.__world_uuid,
                         x,
                         y))
      else:
        self.db.execute("""
          INSERT INTO world_tile (world_uuid, x, y, tile_id) 
                            VALUES (%s, %s, %s, %s)""",
                        (self.__world_uuid,
                         x,
                         y,
                         self.__tile_data[y][x]))

  def __persist_buildings(self):
    for building in self.__building_data:
      if not building["in_db"]:
        self.db.execute("""
          INSERT INTO world_building (world_uuid, x, y, building_id, owner_id) 
                            VALUES (%s, %s, %s, %s, %s)""",
                        (self.__world_uuid,
                         building["x"],
                         building["y"],
                         building["id"],
                         building["owner_id"]))
        building["in_db"] = True
