import {restRequest} from "../io.js";

class PlayerData
{
  constructor(gameId)
  {
    this.gameId = gameId;
    this.players = {};
    this.myPlayerId = undefined;
  }

  refresh()
  {
    restRequest({method: "GET", path: "/game/" + this.gameId + "/players"}, (response) =>
    {
      response.body.players.forEach((player) =>
      {
        this.players[player.id] = player;
        if (player.me == true)
        {
          this.myPlayerId = player.id;
        }
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
