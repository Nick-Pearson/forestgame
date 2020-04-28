import {restRequest} from "../io.js";

class PlayerStats
{
  constructor(gameId)
  {
    this.gameId = gameId;

    this.playerName = "";
    this.population = 0;
    this.wood = 0;
    this.coin = 0;
    this.food = 0;
  }

  refreshAll()
  {
    this.refreshName();
    this.refreshStats();
  }

  refreshName()
  {
    restRequest({method: "GET", path: "/game/" + this.gameId + "/player-name"}, (response) =>
    {
      this.playerName = response.body.name;
    });
  }

  refreshStats()
  {
    restRequest({method: "GET", path: "/game/" + this.gameId + "/player-stats"}, (response) =>
    {
      const stats = response.body.stats;
      this.population = stats.population;
      this.wood = stats.wood;
      this.coin = stats.coin;
      this.food = stats.food;
    });
  }
};

export {PlayerStats};
