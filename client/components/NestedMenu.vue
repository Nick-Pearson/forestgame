<template>
  <div class="nested-menu" :style="menuStyle">
    <ul>
      <div v-for="(item, index) in items"  :key="item.id" v-on:mouseover="updateHovered(index)">
        <a 
          v-bind:class="{disabled: item.disabled}"
          v-on:click="clicked(item.eventId)"
        >
          <li class="menu-option">{{item.label}}</li>
        </a>
        <NestedMenu 
          v-show="hoveredIndex === index" 
          v-bind:x="130"
          v-bind:y="15 + (index * 43)"
          v-bind:items="item.children"
          v-on:menu-select="(e) => onAnyEvent(item.eventId, e)"
        />
      </div>
    </ul>
  </div>
</template>

<style scoped>
.nested-menu
{
  z-index: 500;
  position: absolute;
  color: #ffffff;
  width: 130px;
}

.nested-menu ul
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
export default {
  name: "NestedMenu",
  props: ['x', 'y', 'items'],
  data: () => {
    return {
      hoveredIndex: -1,
    };
  },
  methods: {
    updateHovered: function (idx) {
      this.hoveredIndex = idx;
    },
    clicked: function(event) {
      if (event !== undefined)
      {
        this.$emit("menu-select", [event]);
      }
    },
    onAnyEvent: function(parentEvent, childEvent)
    {
      childEvent.unshift(parentEvent);
      this.$emit("menu-select", childEvent);
    }
  },
  computed: {
    menuStyle: function () {
      return "top: " + this.y + "px; left: " + this.x + "px;"
    }
  }
}
</script>