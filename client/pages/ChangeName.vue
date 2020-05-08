<template>
  <MenuWrapper>    
    <h1>Change Name</h1>
    <input type="text" v-model="name" placeholder="Player Name"/>
    <p v-bind:class="{invalid: !isValid}" class="char-count">{{charactersUsed}} / {{maxCharacters}} characters</p>
    <ErrorBox v-if="errorMsg.length != 0">{{errorMsg}}</ErrorBox>
    <button v-on:click="changeName($event)">Submit</button>
  </MenuWrapper>
</template>

<style>
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
      model.errorMsg = "Unknown Error Occurred: HTTP " + response.status;
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
  },
  components: {
    MenuWrapper,
    ReturnHomeButton,
    ErrorBox
  }
}
</script>