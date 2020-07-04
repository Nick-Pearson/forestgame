<template>
  <MenuWrapper>
    <ReturnHomeButton/>

    <h1>Create New Game</h1>

    <Spinner v-if="loading"/>
    <div v-else>
      <form>

        <div class="select-wrapper">
          <label for="maps">Map:</label>
          <select id="maps" v-model="selectedMapVal">
            <option v-for="map in maps" :key="map.id" :value="map.id">{{map.name}} (2-{{map.max_players}} Players)</option>
          </select>
        </div>
        
        <div class="select-wrapper">
          <label for="player-count">Max. Players:</label>
          <select id="player-count" v-model="selectedMaxPlayers">
            <option v-for="i in (selectedMap.max_players - 1)" :key="i" :value="i + 1">{{i + 1}}</option>
          </select>
        </div>

        <MapThumbnail v-bind:mapId="selectedMapVal" v-bind:maxPlayers="selectedMaxPlayers"/>

        <ErrorBox v-bind:msg="errorMsg"/>
        <button class="main-button" v-on:click="createGame($event)">
          <span v-if="!creating">Create</span>
          <span v-else>Creating...</span>
        </button>
      </form>
    </div>
  </MenuWrapper>
</template>

<style scoped>
form
{
  width: 60%;
  margin: auto;
}

.select-wrapper
{
  text-align: left;
  width: 100%;
  margin: 15px 0 15px 0;
}

.select-wrapper select
{
  width: 100%;
  margin-top: 3px;
}
</style>

<script>
import MenuWrapper from '../components/MenuWrapper.vue'
import ReturnHomeButton from '../components/ReturnHomeButton.vue'
import Spinner from '../components/Spinner.vue'
import MapThumbnail from '../components/MapThumbnail.vue'
import ErrorBox from '../components/ErrorBox.vue'
import {restRequest} from "../src/io.js"

const model = {
  creating: false,
  errorMsg: "",
  loading: true,
  maps: [],
  selectedMapVal: null,
  selectedMaxPlayers: "2"
}

function createGame(e)
{
  e.preventDefault();

  if (model.creating)
  {
    return;
  }

  model.creating = true;
  const body = {
    "map_id": this.selectedMapVal,
    "max_players": parseInt(this.selectedMaxPlayers)
  }
  restRequest({method: "POST", path: "/game", body: body}, (response) => {
    model.creating = false;

    if (response.status === 200)
    {
      this.$router.push({name: "change-name", params: {gameId: response.body.game_id}});
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

function mounted()
{
  restRequest({method: "GET", path: "/maps"}, (response) => 
  {
    if (response.status === 200)
    {
      model.maps = response.body.maps;
      model.selectedMapVal = model.maps[0].id;
    }
    else if (response.body != null && response.body.message !== undefined)
    {
      model.errorMsg = response.body.message;
    }
    else
    {
      model.errorMsg = "Unknown Error Occurred: HTTP " + response.status;
    }
    model.loading = false;
  });
}

export default 
{
  name: 'CreateGame',
  data: () => model,
  methods: {
    createGame: createGame,
  },
  mounted: mounted,
  components: {
    MenuWrapper,
    ReturnHomeButton,
    Spinner,
    MapThumbnail,
    ErrorBox
  },
  computed: {
    selectedMap: function() 
    {
      return this .maps.find((map) => {
        return map.id == this.selectedMapVal;
      });
    }
  }
}
</script>