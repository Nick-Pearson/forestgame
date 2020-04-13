import WorldData from "./world.json";

const TILES = [
  "base",
  "forest",
  "clearing",
  "mountains",
];

class World
{
  constructor()
  {
    this.tileData = WorldData.tileData;
    this.buildings = [];
    for (let x = 0; x < this.getSizeY(); ++x)
    {
      this.buildings.push(new Array(this.getSizeX()).fill(null));
    }
    WorldData.buildings.forEach((building) =>
    {
      const x = building.x;
      const y = building.y;
      building.x = undefined;
      building.y = undefined;
      this.buildings[y][x] = building;
    });
  }

  getSizeX()
  {
    return this.tileData[0].length;
  }

  getSizeY()
  {
    return this.tileData.length;
  }

  getTileData()
  {
    return this.tileData;
  }

  getBuildingData()
  {
    return this.buildings;
  }
}

export {World, TILES};
