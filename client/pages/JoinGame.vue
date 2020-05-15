<template>
  <MenuWrapper>    
    <ReturnHomeButton/>
    <h1>Join Game</h1>
    <input type="text" spellcheck="false" v-bind:class="{'code-input': code.length != 0}" v-model="code" placeholder="Invite Code" maxlength="4"/>
    <input type="text" spellcheck="false" v-model="name" placeholder="Player Name"/>
    <p v-bind:class="{invalid: !isValid}" class="char-count">{{charactersUsed}} / {{maxCharacters}} characters</p>
    <br/>
    <ErrorBox v-bind:msg="errorMsg"/>
    <button v-on:click="joinGame($event)">Join Game</button>
  </MenuWrapper>
</template>

<style>
  .code-input
  {
    text-transform: uppercase;
  }

  .invalid
  {
    color: #dd0000;
  }

  .char-count
  {
    margin: 5px;
    font-size: 0.8rem;
  }
</style>

<script>
import MenuWrapper from '../components/MenuWrapper.vue'
import ReturnHomeButton from '../components/ReturnHomeButton.vue'
import ErrorBox from '../components/ErrorBox.vue'
import {restRequest} from "../src/io.js"

function joinGame(e)
{
  e.preventDefault();

  restRequest({method: "POST", path: "/invite/" + this.code + "/players", body: {name: this.name}}, (response) => {
    if (response.status === 200)
    {
      this.$router.push({name: "lobby", params: {gameId: response.body.game_id}});
    }
    else if (response.body != null && response.body.message !== undefined)
    {
      this.errorMsg = response.body.message;
    }
    else
    {
      this.errorMsg = "Unknown Error Occurred: HTTP " + response.status;
    }
  });
}

export default 
{
  data: () => {
    return {
      errorMsg: "",
      code: "",
      name: "",
      maxCharacters: 20,
      minCharacters: 2,
      isValid: false,
    }
  },
  computed: {
    charactersUsed: function() {
      return this.name.length;
    }
  },
  watch: {
    name: function(val) {
      this.isValid = val.length <= this.maxCharacters && val.length >= this.minCharacters;
    }
  },
  methods: {
    joinGame: joinGame
  },
  components: {
    MenuWrapper,
    ReturnHomeButton,
    ErrorBox
  }
}
</script>