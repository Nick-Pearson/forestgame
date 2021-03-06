import {restRequest} from "../io.js";
import {EventBroadcast} from "../eventbroadcast.js";
import {TILE_SIZE, MOUNTAIN_TILE_ID} from "../tile/index.js";

class World
{
  constructor(gameId)
  {
    this.gameId = gameId;
    this.onworldupdate = new EventBroadcast();
    this.onworldloaded = new EventBroadcast();
    this.tileData = [];
    this.buildings = [];
    this.sizeX = 0;
    this.sizeY = 0;
    this.worldScale = 1.0;
    this.worldPosition = {x: 0, y: 0};
    this.cameraPosition = {x: 0, y: -2};
    this.loaded = false;

    this.updateWorldData();

    socket.on("build", () =>
    {
      this.updateWorldData();
    });
    socket.on("deforest", () =>
    {
      this.updateWorldData();
    });
  }

  updateWorldData()
  {
    restRequest({method: "GET", path: "/game/" + this.gameId + "/world"}, (resp) =>
    {
      const data = resp.body;
      this.sizeX = data.tileData[0].length;
      this.sizeY = data.tileData.length;
      this.tileData = data.tileData;

      // make this generate fewer arrays
      this.buildings = [];
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

      // notify listeners
      if (this.loaded == false)
      {
        this.loaded = true;
        this.onworldloaded.broadcast();
      }
      this.onworldupdate.broadcast();
    });
  }

  moveCamera(x, y)
  {
    if (x == 0.0 && y == 0.0) return;

    this.cameraPosition.x += x;
    this.cameraPosition.y += y;
    this.onworldupdate.broadcast();
  }

  setWorldPosition(x, y)
  {
    this.worldPosition.x = x;
    this.worldPosition.y = y;
  }

  actionDeforest(x, y, oncomplete)
  {
    this.tileData[y][x] = 2;
    this.onworldupdate.broadcast();

    const req = {
      method: "POST",
      path: "/game/" + this.gameId + "/actions/deforest",
      body: {x: x, y: y},
    };
    restRequest(req, (resp) =>
    {
      this.updateWorldData();
      oncomplete();
    });
  }

  actionBuild(buildingId, x, y, playerId, oncomplete)
  {
    this.tileData[y][x] = 0;
    this.buildings[y][x] = {
      x: x,
      y: y,
      id: buildingId,
      owner_id: playerId,
    };
    this.onworldupdate.broadcast();

    const req = {
      method: "POST",
      path: "/game/" + this.gameId + "/actions/build",
      body: {x: x, y: y, building_id: buildingId},
    };
    restRequest(req, (resp) =>
    {
      this.updateWorldData();
      oncomplete();
    });
  }

  getTileFromCoords(clientX, clientY)
  {
    const scaledX = clientX / this.worldScale;
    const scaledY = clientY / this.worldScale;
    const tileX = Math.floor((scaledX - this.getOffsetX()) / TILE_SIZE);
    const tileY = Math.floor((scaledY - this.getOffsetY()) / TILE_SIZE);

    return {x: tileX, y: tileY};
  }

  getCoordsForTile(tileX, tileY)
  {
    const clientX = (tileX * TILE_SIZE) + this.getOffsetX();
    const clientY = (tileY * TILE_SIZE) + this.getOffsetY();
    return {x: clientX, y: clientY};
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

  getBuildingAt(x, y)
  {
    if (x < 0 || y < 0 || x >= this.sizeX || y >= this.sizeY)
    {
      return null;
    }
    {
      return this.buildings[y][x];
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

  getOffsetX()
  {
    return Math.round(this.cameraPosition.x + this.worldPosition.x);
  }

  getOffsetY()
  {
    return Math.round(this.cameraPosition.y + this.worldPosition.y);
  }
}

export {World};
