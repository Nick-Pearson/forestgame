<template>
  <div>
    <h1>Change Name</h1>
    <input type="text" v-model="name" placeholder="Player Name"/>
    <p v-bind:class="{invalid: !isValid}">{{charactersUsed}} / {{maxCharacters}} characters</p>
      <p>{{errorMsg}}</p>
    <button v-on:click="changeName($event)">Submit</button>
  </div>
</template>

<style>
  .invalid
  {
    color: #dd0000;
  }
</style>

<script>
import {restRequest} from "../src/io.js"

const model = {
  name: '',
  maxCharacters: 20,
  minCharacters: 2,
  isValid: false,
  errorMsg: ""
};

function changeName(e)
{
  e.preventDefault();

  const gameId = this.$route.params.gameId;
  restRequest({method: "PUT", path: "/game/" + gameId + "/player-name", body: {name: this.name}}, (response) => {
    if (response.status === 200)
    {
      this.$router.push({name: "game", params: {gameId: gameId}});
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
  data: () => model,
  computed: {
    charactersUsed: function() {
      return this.name.length;
    }
  },
  watch: {
    name: function(val) {
      model.isValid = val.length <= this.maxCharacters && val.length >= this.minCharacters;
    }
  },
  methods: {
    changeName: changeName
  }
}
</script>