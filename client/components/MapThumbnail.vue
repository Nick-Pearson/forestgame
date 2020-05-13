<template>
  <div class="thumb-wrapper">
    <div class="spinner-container">
      <Spinner v-if="loadingThumb"/>
    </div>
    <img v-if="mapId != undefined" class="map-thumbnail" :src="mapThumbnailUrl" v-on:startload="onThumbStartLoad" v-on:load="onThumbLoaded"/>
  </div>
</template>

<style scoped>
.map-thumbnail
{
  border: 2px solid #000000;
  height: 150px;
  image-rendering: pixelated;
}

.thumb-wrapper
{
  position: relative;
}

.thumb-wrapper svg
{
  position: absolute;
  left: 50%;
  margin-left: -25px;
  top: 50%;
  margin-top: -25px;
}
</style>

<script>
import Spinner from '../components/Spinner.vue'

const model = {
  loadingThumb: true,
}

export default 
{  
  name: 'MapThumbnail',
  props: ['mapId', 'maxPlayers'],
  data: () => model,
  components: {
    Spinner
  },
  methods: {
    onThumbStartLoad: function() {
      this.loadingThumb = true
    },
    onThumbLoaded: function() {
      this.loadingThumb = false
    }
  },
  computed: {
    mapThumbnailUrl: function() {
      this.onThumbStartLoad();
      let url = "/api/maps/" + this.mapId + "/thumbnail";
      if (this.maxPlayers !== undefined)
      {
        url += "?maxPlayers=" + this.maxPlayers
      }
      return url;
    }
  }
}
</script>