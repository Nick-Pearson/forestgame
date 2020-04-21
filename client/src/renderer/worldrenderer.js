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
    this.buildingIdToSprite = [
      this.tiles.townhall,
      this.tiles.farm,
    ];
    this.seed = Math.floor(Math.random() * 10000000);
    world.onworldupdate = () =>
    {
      this.render();
    };
  }

  render()
  {
    this.context.clearRect(0, 0, this.context.canvas.width, this.context.canvas.height);

    const maxX = this.world.getSizeX();
    const maxY = this.world.getSizeY();
    const tileData = this.world.getTileData();
    const buildings = this.world.getBuildingData();

    const rand = new Random(this.seed);

    for (let x = maxX - 1; x >= 0; x--)
    {
      for (let y = 0; y < maxY; y++)
      {
        const tileId = tileData[y][x];
        const tiles = this.tileIdToTiles[tileId];
        const tileX = TILE_SIZE * x;
        const tileY = (TILE_SIZE * y) - 2;

        this.context.drawImage(tiles[rand.nextInt(tiles.length)], tileX, tileY);

        const building = buildings[y][x];
        if (building != null)
        {
          this.context.drawImage(this.buildingIdToSprite[building.type], tileX, tileY);
        }
      }
    }
  }
}


export {WorldRenderer};
