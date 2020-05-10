import {restRequest} from "../io.js";

class PlayerData
{
  constructor(gameId)
  {
    this.gameId = gameId;
    this.players = {};
  }

  refresh()
  {
    restRequest({method: "GET", path: "/game/" + this.gameId + "/players"}, (response) =>
    {
      response.body.players.forEach((player) =>
      {
        this.players[player.id] = player;
      });
    });
  }

  getColourForPlayer(playerId)
  {
    const player = this.players[playerId];
    if (player != null)
    {
      return player.colour;
    }
    return "#000000";
  }
}

export {PlayerData};
