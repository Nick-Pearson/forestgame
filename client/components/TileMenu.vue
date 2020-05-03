<template>
  <div class="tile-menu" :style="menuStyle">
    <ul>
      <a v-on:click="deforest"><li class="menu-option">Clear Trees</li></a>
      <a href="#" class="disabled"><li class="menu-option">Build</li></a>
    </ul>
  </div>
</template>

<style scoped>
.tile-menu
{
  z-index: 500;
  position: absolute;
  color: #ffffff;
}

.tile-menu ul
{
  padding-left: 0;
}

.menu-option
{
  background-color: #333333;
  list-style-type: none;
  padding: 10px 30px 10px 10px;
  display: box;
}
.menu-option:hover
{
  background-color: #444444;
}

a
{
  color: #dddddd;
  text-decoration: none;
  user-select: none;
  cursor: pointer;
}

a:hover
{
  color: #ffffff;
}

a.disabled
{
  color: #aaaaaa;
  cursor: default;
}
a.disabled .menu-option:hover
{
  background-color: #333333;
}
</style>

<script>

function deforest()
{
  console.log("deforest");
  this.game.actionDeforest();
}

export default {
  props: ['x', 'y', 'game'],
  methods: {
    deforest: deforest
  },
  computed: {
    menuStyle: function () {
      return "top: " + this.y + "px; left: " + this.x + "px;"
    }
  }
}
</script>