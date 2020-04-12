import {loadAllTiles, TILE_SIZE} from "../tile/index.js";
import {Random} from "../math/random.js";

class WorldRenderer
{
  constructor(context, world)
  {
    this.context = context;
    this.world = world;
    this.context.imageSmoothingEnabled = false;
    this.tiles = loadAllTiles(() => this.render());
    this.tileIdToTiles = [
      this.tiles.base,
      this.tiles.forest,
      this.tiles.clearing,
      this.tiles.mountains,
    ];
    this.seed = Math.floor(Math.random() * 10000000);
  }

  render()
  {
    const maxX = this.world.getSizeX();
    const maxY = this.world.getSizeY();
    const tileData = this.world.getTileData();
    const rand = new Random(this.seed);

    for (let x = maxX - 1; x >= 0; x--)
    {
      for (let y = 0; y < maxY; y++)
      {
        const tileId = tileData[x][y];
        const tiles = this.tileIdToTiles[tileId];
        this.context.drawImage(tiles[rand.nextInt(tiles.length)], TILE_SIZE * x, (TILE_SIZE * y) -2);
      }
    }
  }
}


export {WorldRenderer};
