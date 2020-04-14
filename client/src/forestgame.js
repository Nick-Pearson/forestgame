import {World} from "./world";
import {PlayerStats} from "./player/playerstats.js";

class ForestGame
{
  constructor()
  {
    this.world = new World();
    this.playerStats = new PlayerStats();
    this.playerStats.refresh();
  };
}

export {ForestGame};
