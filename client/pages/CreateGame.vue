<template>
  <MenuWrapper>
    <ReturnHomeButton/>

    <h1>Create New Game</h1>

    <form>
      <p>{{errorMsg}}</p>
      <button v-on:click="createGame($event)">
        <span v-if="!creating">Create</span>
        <span v-else>Creating...</span>
      </button>
    </form>
  </MenuWrapper>
</template>

<style>
</style>

<script>
import MenuWrapper from '../components/MenuWrapper.vue'
import ReturnHomeButton from '../components/ReturnHomeButton.vue'
import {restRequest} from "../src/io.js"

const model = {
  creating: false,
  errorMsg: ""
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
      model.errorMsg = "Unknown Error Occured: HTTP " + response.status;
    }
  });
}

export default 
{
  name: 'CreateGame',
  data: () => model,
  methods: {
    createGame: createGame
  },
  components: {
    MenuWrapper,
    ReturnHomeButton
  }
}
</script>