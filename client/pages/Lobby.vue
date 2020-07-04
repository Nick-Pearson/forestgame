<template>
  <MenuWrapper>
    <div class="invite-code">
      <p>Invite Code:</p>
      <h1>{{gameData.invite_code}}</h1>
    </div>

    <div class="row">
      <div class="column">
        <div class="player-panel" v-for="player in playerData" :key="player.id" v-bind:class="{me: player.me}" >
          <div class="colour-wrapper">
            <div class="player-colour" 
              v-bind:style="{'background-color': player.colour}"
            >
            </div>
          </div>
          <div class="name-wrapper">
            <p>{{player.name}}</p>
          </div>
        </div>
      </div>
      <div class="column">
        <table>
          <tr>
            <td>Map:</td>
            <td>{{mapData.name}}</td>
          </tr>
          <tr>
            <td>Players:</td>
            <td>{{gameData.num_players}} / {{gameData.max_players}}</td>
          </tr>
          <tr>
            <td>Game Mode:</td>
            <td>{{gameData.game_mode_name}}l</td>
          </tr>
        </table>

        <MapThumbnail v-bind:mapId="gameData.map_id" v-bind:maxPlayers="gameData.max_players"/>
      </div>
    </div>

    <ErrorBox v-bind:msg="errorMsg"/>
    <button class="main-button" v-if="gameData.is_host" v-on:click="startGame($event)">
      Start Game
    </button>
    <p v-else>The host will start the game</p>
  </MenuWrapper>
</template>

<style scoped>
.invite-code
{
  width: fit-content;
  margin: 0 auto 0 auto;
  padding: 10px 25px 10px 25px;
  background-color: #EEEEEE;
  box-shadow: inset -6px -6px 0px 0px #555555;
  border: 1px solid #000000;
}

.invite-code h1
{
  margin: 5px 0 5px 0;
  text-transform: uppercase;
  font-size: 3rem;
  letter-spacing: 1rem;
}

.invite-code p
{
  margin: 5px 0 5px 0;
}

.player-panel
{
  background-color: #AAAAAA;
  border: 1px solid #000000;
  display: flex;
}

.player-panel .name-wrapper
{
  flex: 80%;
}

.player-panel.me
{
  background-color: #FFFFFF;
  border: 2px solid #000000;
}

.player-panel p
{
  margin: 15px 0 15px 0;
}

.player-colour
{
  background-color: #FF0000;
  border: 1px solid #000000;
  padding: 13px;
  display: inline-block;
  margin: 2px;
  position: relative;
  top: 50%;
  transform: translateY(-50%);
}

table
{
  margin: auto;
}

table td
{
  padding-right: 32px;
  text-align: right;
}

table td:nth-child(1)
{
  color: #666666;
}

table td:nth-child(2)
{
  text-align: center;
}

.row 
{
  display: flex;
}

.column 
{
  flex: 50%;
}

.column > * 
{
  margin: 10px;
}
</style>

<script>
import MenuWrapper from '../components/MenuWrapper.vue'
import MapThumbnail from '../components/MapThumbnail.vue'
import ErrorBox from '../components/ErrorBox.vue'
import {restRequest} from "../src/io.js"

const model = {
  gameData: {},
  playerData: [],
  mapData: {},
  gameId: "",
  errorMsg: ""
};

function startGame(e)
{
  e.preventDefault();

  restRequest({method: "POST", path: "/game/" + model.gameId + "/start" }, (response) => {
    if (response.status === 200)
    {
      this.$router.push({name: "game", params: {gameId: model.gameId}});
    }
    else if (response.body != null && response.body.message !== undefined)
    {
      model.errorMsg = response.body.message;
    }
    else
    {
      model.errorMsg = "Unknown Error Occurred: HTTP " + response.status;
    }
  });
}

function loadMapData()
{
  restRequest({method: "GET", path: "/maps/" + model.gameData.map_id }, (response) => {
    if (response.status === 200)
    {
      model.mapData = response.body;
    }
    else if (response.body != null && response.body.message !== undefined)
    {
      model.errorMsg = response.body.message;
    }
    else
    {
      model.errorMsg = "Unknown Error Occurred: HTTP " + response.status;
    }
  });
}

function poll()
{
  restRequest({method: "GET", path: "/game/" + model.gameId + "/players"}, (response) => {
    model.creating = false;

    if (response.status === 200)
    {
      model.playerData = response.body.players;
    }
    else if (response.body != null && response.body.message !== undefined)
    {
      model.errorMsg = response.body.message;
    }
    else
    {
      model.errorMsg = "Unknown Error Occurred: HTTP " + response.status;
    }
  });
  restRequest({method: "GET", path: "/game/" + model.gameId }, (response) => {
    if (response.status === 200)
    {
      model.gameData = response.body;
      if (!model.gameData.is_lobby)
      {
        this.$router.push({name: "game", params: {gameId: model.gameId}});
      }
      else if (model.gameData.map_id !== model.mapData.id)
      {
        loadMapData();
      }
    }
    else if (response.body != null && response.body.message !== undefined)
    {
      model.errorMsg = response.body.message;
    }
    else
    {
      model.errorMsg = "Unknown Error Occurred: HTTP " + response.status;
    }
  });
}

export default 
{
  name: 'Lobby',
  data: () => model,
  methods: {
    startGame: startGame,
    poll: poll
  },
  mounted: function() {
    model.gameId = this.$route.params.gameId;
    setInterval(() => this.poll(), 4000);
    this.poll();
  },
  components: {
    MenuWrapper,
    MapThumbnail,
    ErrorBox
  },
}
</script>