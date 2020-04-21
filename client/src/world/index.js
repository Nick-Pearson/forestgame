import {restRequest} from "../io.js";
import {TILE_SIZE, MOUNTAIN_TILE_ID} from "../tile/index.js";

const TILES = [
  "base",
  "forest",
  "clearing",
  "mountains",
];

class World
{
  constructor(gameId)
  {
    this.gameId = gameId;
    this.onworldupdate = null;
    this.tileData = [];
    this.buildings = [];
    this.sizeX = 0;
    this.sizeY = 0;
    this.worldScale = 3.4;

    this.updateWorldData();
  }

  updateWorldData()
  {
    restRequest({method: "GET", path: "/game/" + this.gameId + "/world"}, (resp) =>
    {
      const data = resp.body;
      this.sizeX = data.tileData[0].length;
      this.sizeY = data.tileData.length;
      this.tileData = data.tileData;

      for (let x = 0; x < this.sizeY; ++x)
      {
        this.buildings.push(new Array(this.getSizeX()).fill(null));
      }
      data.buildings.forEach((building) =>
      {
        const x = building.x;
        const y = building.y;
        this.buildings[y][x] = building;
      });

      if (this.onworldupdate != null)
      {
        this.onworldupdate();
      }
    });
  }

  actionDeforest(x, y)
  {
    const req = {
      method: "POST",
      path: "/game/" + this.gameId + "/actions/deforest",
      body: {x: x, y: y},
    };
    restRequest(req, (resp) =>
    {
      this.updateWorldData();
    });
  }

  getTileCoords(clientX, clientY)
  {
    const tileX = Math.floor(clientX / (TILE_SIZE * this.worldScale));
    const tileY = Math.floor(clientY / (TILE_SIZE * this.worldScale));

    return {x: tileX, y: tileY};
  }
  getTileAt(x, y)
  {
    if (x < 0 || y < 0 || x >= this.sizeX || y >= this.sizeY)
    {
      return MOUNTAIN_TILE_ID;
    }
    {
      return this.tileData[y][x];
    }
  }

  getSizeX()
  {
    return this.sizeX;
  }

  getSizeY()
  {
    return this.sizeY;
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
