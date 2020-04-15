import {World} from "./world";
import {PlayerStats} from "./player/playerstats.js";

class ForestGame
{
  constructor(gameId)
  {
    this.gameId = gameId;

    this.world = new World();
    this.playerStats = new PlayerStats(gameId);
    this.playerStats.refresh();
  };
}

export {ForestGame};
