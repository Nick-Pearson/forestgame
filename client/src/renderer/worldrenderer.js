import {loadAllTiles, TILE_SIZE, buildingMetadata} from "../tile/index.js";
import {GridRandom} from "../math/gridrandom.js";

const WORLD_PADDING = 4;

class WorldRenderer
{
  constructor(context, game)
  {
    this.context = context;
    this.game = game;
    this.world = game.world;

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
      this.tiles.flag,
      this.tiles.sawmill,
      this.tiles.windmill,
    ];
    const seed = Math.floor(Math.random() * 10000000);
    this.rand = new GridRandom(seed, 1, 1);

    game.world.onworldupdate.addListener(() =>
    {
      this.render();
    });
    game.world.onworldloaded.addListener(() =>
    {
      this.rand = new GridRandom(seed, game.world.getSizeX() + (WORLD_PADDING * 2), game.world.getSizeY() + (WORLD_PADDING * 2));
    });
  }

  render()
  {
    this.context.fillStyle = "black";
    this.context.fillRect(0, 0, this.context.canvas.width / this.world.worldScale, this.context.canvas.height / this.world.worldScale);

    const offsetX = this.world.getOffsetX();
    const offsetY = this.world.getOffsetY();

    const mapTopLeft = this.ensureInBound(this.world.getTileFromCoords(0, -4));
    const mapBottomRight = this.ensureInBound(this.world.getTileFromCoords(this.context.canvas.width, this.context.canvas.height));

    for (let x = mapBottomRight.x; x >= mapTopLeft.x; x--)
    {
      for (let y = mapTopLeft.y; y <= mapBottomRight.y; y++)
      {
        const tileId = this.world.getTileAt(x, y);
        const tiles = this.tileIdToTiles[tileId];
        const tileX = (TILE_SIZE * x) + offsetX;
        const tileY = (TILE_SIZE * y) + offsetY;

        const rand = this.rand.getRand(x + WORLD_PADDING, y + WORLD_PADDING);

        this.context.drawImage(tiles[rand % tiles.length], tileX, tileY);

        const building = this.world.getBuildingAt(x, y);
        if (building != null)
        {
          this.drawBuilding(tileX, tileY, building);
        }
      }
    }
  }

  drawBuilding(x, y, building)
  {
    this.context.drawImage(this.buildingIdToSprite[building.id], x, y);
    if (building.ownerId !== null)
    {
      this.context.fillStyle = this.game.playerData.getColourForPlayer(building.ownerId);

      const metaData = buildingMetadata[building.id];
      if (metaData.teamColour !== undefined)
      {
        metaData.teamColour.forEach((rect) =>
        {
          this.context.fillRect(x + rect.x, y + rect.y, rect.width, rect.height);
        });
      }
    }
  }

  ensureInBound(coords)
  {
    const minX = -WORLD_PADDING;
    const maxX = this.world.getSizeX() + WORLD_PADDING - 1;
    const minY = -WORLD_PADDING;
    const maxY = this.world.getSizeY() + WORLD_PADDING - 1;
    return {
      x: Math.max(minX, Math.min(coords.x, maxX)),
      y: Math.max(minY, Math.min(coords.y, maxY)),
    };
  }
}


export {WorldRenderer};
