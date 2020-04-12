import {loadAllTiles, TILE_SIZE} from "../tile/index.js";

class WorldRenderer
{
  constructor(context, world)
  {
    this.context = context;
    this.world = world;
    this.context.imageSmoothingEnabled = false;
    this.tiles = loadAllTiles(() => this.render());
    this.tileIdToTile = [
      this.tiles.base,
      this.tiles.forest,
      this.tiles.clearing,
      this.tiles.mountains,
    ];
  }

  render()
  {
    const maxX = this.world.getSizeX();
    const maxY = this.world.getSizeY();
    const tileData = this.world.getTileData();

    for (let x = maxX - 1; x >= 0; x--)
    {
      for (let y = 0; y < maxY; y++)
      {
        const tileId = tileData[x][y];
        const tile = this.tileIdToTile[tileId];
        this.context.drawImage(tile[0], TILE_SIZE * x, (TILE_SIZE * y) -2);
      }
    }
  }
}


export {WorldRenderer};
