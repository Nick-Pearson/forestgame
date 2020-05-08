

class World:
  def __init__(self):
    self.__tileData = [];
    self.__buildingData = [];
    self.__sizeX = 0;
    self.__sizeY = 0;
    
  def set_size(self, x, y):
    if y > self.__sizeY:
      diff = y - self.__sizeY;
      self.__tileData = self.__tileData + [[1] * self.__sizeX] * diff;
    elif y < self.__sizeY:
      self.__tileData = self.__tileData[:y];

    if x > self.__sizeX:
      diff = x - self.__sizeX;
      for i in range(0, len(self.__tileData)):
        self.__tileData[i] = self.__tileData[i] + [1] * diff
    elif x < self.__sizeX:
      for i in range(0, len(self.__tileData)):
        self.__tileData[i] = self.__tileData[i][:x]

    self.__sizeX = x;
    self.__sizeY = y;

  def set_tile_at(self, x, y, tileId):
    self.__tileData[y][x] = tileId;

  def get_tile_at(self, x, y):
    return self.__tileData[y][x];

  def set_building_at(self, x, y, buildingId):
    self.__buildingData.append({
      "x": x,
      "y": y,
      "id": buildingId,
    });
  
  def get_size_x(self):
    return self.__sizeX;
  
  def get_size_y(self):
    return self.__sizeY;
  
  def get_tile_data(self):
    return self.__tileData;

  def get_building_data(self):
    return self.__buildingData;