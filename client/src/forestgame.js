import {World} from "./world";
import {PlayerStats} from "./player/playerstats.js";
import {FOREST_TILE_ID} from "./tile";

class ForestGame
{
  constructor(gameId, container)
  {
    this.gameId = gameId;
    this.container = container;

    this.world = new World(gameId);
    this.playerStats = new PlayerStats(gameId);
    this.playerStats.refresh();

    this.setupKeyBinds(container);
  };

  setupKeyBinds(container)
  {
    document.addEventListener("mousedown", (e) =>
    {
      const coords = this.world.getTileCoords(e.clientX, e.clientY);
      this.onClick(coords.x, coords.y);
    });
  }

  onClick(x, y)
  {
    const tileId = this.world.getTileAt(x, y);

    if (tileId == FOREST_TILE_ID)
    {
      this.world.actionDeforest(x, y, () =>
      {
        this.playerStats.refresh();
      });
    }
  }
}

export {ForestGame};
