<template>
  <div>
    <canvas ref="main-canvas" class="main-canvas"></canvas>
    <canvas ref="ui-canvas" class="ui-canvas"></canvas>
  </div>
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
  position: absolute;
  top: 0;
}

.main-canvas
{
  image-rendering: -moz-crisp-edges;
  image-rendering: -webkit-crisp-edges;
  image-rendering: pixelated;
  image-rendering: crisp-edges;
  z-index: 100;
}

.ui-canvas
{
  z-index: 200;
}
</style>

<script>
import {ForestGame} from "../src/forestgame.js";
import {WorldRenderer} from "../src/renderer/worldrenderer.js";
import {UIRenderer} from "../src/renderer/uirenderer.js";
import {World} from "../src/world/index.js";

export default 
{
  mounted () 
  {
    const gameId = this.$route.params.gameId;
    const mainCanvas = this.$refs['main-canvas'];
    const uiCanvas = this.$refs['ui-canvas'];

    const game = new ForestGame(gameId, mainCanvas);

    const UI_SCALE = 1;

    const worldRenderer = new WorldRenderer(mainCanvas.getContext('2d'), game.world);
    const uiRenderer = new UIRenderer(uiCanvas.getContext('2d'), game, UI_SCALE);

    const appContainer = mainCanvas.parentElement.parentElement;

    let setCanvasSize = () => {
      mainCanvas.width = appContainer.clientWidth;
      mainCanvas.height = appContainer.clientHeight;

      uiCanvas.width = appContainer.clientWidth;
      uiCanvas.height = appContainer.clientHeight;

      mainCanvas.style.width = mainCanvas.width * game.world.worldScale;
      worldRenderer.render();
      uiRenderer.render();
    };

    window.addEventListener("resize", setCanvasSize);
    setCanvasSize();
  }
}
</script>