<template>
  <MenuWrapper>
    <ReturnHomeButton/>

    <h1>Create New Game</h1>

    <Spinner v-if="loading"/>
    <div v-else>
      <form>

        <div class="select-wrapper">
          <label for="maps">Map:</label>
          <select id="maps">
            <option v-for="map in maps" :key="map.id" :value="map.id">{{map.name}}</option>
          </select>
        </div>

        <img :src="mapThumbnailUrl"/>
        
        <div class="select-wrapper">
          <label for="player-count">Max. Players:</label>
          <select id="player-count">
            <option v-for="i in (selectedMap.maxPlayers - 1)" :key="i" :value="i + 1">{{i + 1}}</option>
          </select>
        </div>

        <p>{{errorMsg}}</p>
        <button v-on:click="createGame($event)">
          <span v-if="!creating">Create</span>
          <span v-else>Creating...</span>
        </button>
      </form>
    </div>
  </MenuWrapper>
</template>

<style scoped>
.select-wrapper
{
  text-align: left;
  width: 60%;
  margin: 15px auto 15px auto;
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
import {restRequest} from "../src/io.js"

const model = {
  creating: false,
  errorMsg: "",
  loading: true,
  maps: [],
  selectedMap: null
}

function createGame(e)
{
  e.preventDefault();

  if (model.creating)
  {
    return;
  }

  model.creating = true;
  restRequest({method: "POST", path: "/game"}, (response) => {
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
      model.selectedMap = model.maps[0];
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
    createGame: createGame
  },
  mounted: mounted,
  components: {
    MenuWrapper,
    ReturnHomeButton,
    Spinner
  },
  computed: {
    mapThumbnailUrl: function() {
      return this.selectedMap != null ? "/api/maps/" + this.selectedMap.id + "/thumbnail" : ""
    }
  }
}
</script>