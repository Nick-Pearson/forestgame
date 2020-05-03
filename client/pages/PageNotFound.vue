<template>
  <MenuWrapper>
    <h1>404</h1>
    <p>Error: Page not found</p>
    <ReturnHomeButton/>
  </MenuWrapper>
</template>

<style scoped>
h1
{
  font-family: 'Press Start 2P', cursive;
}
</style>

<script>
import MenuWrapper from '../components/MenuWrapper.vue'
import ReturnHomeButton from '../components/ReturnHomeButton.vue'

export default {
  name: 'PageNotFound',
  components: {
    MenuWrapper,
    ReturnHomeButton
  }
}
</script>