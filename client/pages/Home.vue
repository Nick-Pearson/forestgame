<template>
  <MenuWrapper>
    <div class="title">
      <span class="subtitle">The</span>
      <h1>Forest Game</h1>
    </div>
    <div class="button-wrapper">
      <router-link to="/create-game">
        <button class="create-button">Create Game</button>
      </router-link>
      <hr>
      <router-link to="/join-game">
        <button class="join-button">Join Game</button>
      </router-link>
    </div>
  </MenuWrapper>
</template>

<style scoped>
.title 
{
  font-family: 'Arbutus Slab', serif;
}
.title h1
{
  margin-top: -5px;
}

.button-wrapper
{
  width: 50%;
  margin: 40px auto 20px auto;
}

.create-button
{
  background-color: #77bb66;
  box-shadow: inset -4px -4px 0px 0px #227722;
}
.create-button:hover
{
  background-color: #88cc77;
  text-indent: -2px;
  box-shadow: inset -6px -6px 0px 0px #227722;
}

.join-button
{
  background-color: #3399dd;
  box-shadow: inset -4px -4px 0px 0px #005566;
}
.join-button:hover
{
  background-color: #44aaee;
  text-indent: -2px;
  box-shadow: inset -6px -6px 0px 0px #005566;
}
</style>

<script>
import MenuWrapper from '../components/MenuWrapper.vue'

export default {
  name: 'Home',
  components: {
    MenuWrapper
  }
}
</script>