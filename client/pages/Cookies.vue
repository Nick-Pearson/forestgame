<template>
  <MenuWrapper>
    <ReturnHomeButton/>
    
    <h1>Information about cookies</h1>

    <p>
      Cookies are stored files on your computer. They are usually used to uniquely identify a person (for the purpose of advertising). 
      This game requires cookies to uniquely identify players and plan match their actions within the game.
    </p>
  </MenuWrapper>
</template>

<script>
import MenuWrapper from '../components/MenuWrapper.vue'
import ReturnHomeButton from '../components/ReturnHomeButton.vue'

export default {
  components: {
    MenuWrapper,
    ReturnHomeButton,
  }
}
</script>