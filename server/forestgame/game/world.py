

class World:
  def __init__(self, world_uuid, map_id, size_x, size_y, tile_data, building_data):
    self.__world_uuid = world_uuid
    self.map_id = map_id
    self.__size_x = size_x
    self.__size_y = size_y
    self.__tile_data = tile_data
    self.__building_data = building_data

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
    self.__tile_data[y][x] = tile_id

  def get_tile_at(self, x, y):
    return self.__tile_data[y][x]

  def set_building_at(self, x, y, building_id, owner_id):
    self.__building_data.append({
      "x": x,
      "y": y,
      "id": building_id,
      "owner_id": owner_id,
    })

  def get_size_x(self):
    return self.__size_x

  def get_size_y(self):
    return self.__size_y

  def get_tile_data(self):
    return self.__tile_data

  def get_building_data(self):
    return self.__building_data

  def insert_to_db(self, db, game_id):
    pass