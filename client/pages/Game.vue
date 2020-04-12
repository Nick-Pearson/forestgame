<template>
  <canvas ref="main-canvas"></canvas>
</template>

<style>
html, body
{
  margin: 0;
  overflow: hidden;
}

#app
{
  margin: 0;
  height: 100%;
}

canvas
{
  image-rendering: -moz-crisp-edges;
  image-rendering: -webkit-crisp-edges;
  image-rendering: pixelated;
  image-rendering: crisp-edges;
}
</style>

<script>
import {WorldRenderer} from "../src/renderer/index.js";
import {World} from "../src/world/index.js";

export default 
{
  mounted () 
  {
    const canvas = this.$refs['main-canvas'];
    this.renderer = new WorldRenderer(canvas.getContext('2d'), new World());

    let setCanvasSize = () => {
      canvas.width = canvas.parentElement.clientWidth;
      canvas.height = canvas.parentElement.clientHeight;
      canvas.style.width = canvas.width * 3;
    };

    window.addEventListener("resize", setCanvasSize);
    setCanvasSize();
  }
}
</script>