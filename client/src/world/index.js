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
  }

  getSizeX()
  {
    return this.tileData.length;
  }

  getSizeY()
  {
    return this.tileData[0].length;
  }

  getTileData()
  {
    return this.tileData;
  }
}

export {World, TILES};
