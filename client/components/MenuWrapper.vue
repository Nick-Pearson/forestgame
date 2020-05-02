<template name="MenuWrapper">
  <div class="wrapper">
    <div class="menu-wrapper">
      <slot></slot>
    </div>
    <div class="bg-wrapper">
      <canvas class="bg" ref="bg-canvas" ></canvas>
    </div>
  </div>
</template>


<style scoped>
.wrapper
{
  height: 100%;
  width: 100%;
  text-align: center;
}

.bg-wrapper
{
  position: absolute;
  top: 0;
  left: 0;
  background-color: #00aa00;
  z-index: -100;
  filter: blur(2px);
}

.bg
{
  image-rendering: -moz-crisp-edges;
  image-rendering: -webkit-crisp-edges;
  image-rendering: pixelated;
  image-rendering: crisp-edges;
}

.menu-wrapper
{
  background-color: #cccccc;
  margin: auto;
  padding: 20px;
  z-index: 100;
  box-shadow: 5px 5px 15px;
}

@media screen and (min-width: 1000px)
{
  .menu-wrapper
  {
    width: 50%;
    position: relative;
    top: 10%;
  }
}

@media screen and (min-width: 1400px)
{
  .menu-wrapper
  {
    width: 700px;
  }
}
</style>

<script>
import {loadForestTiles, TILE_SIZE} from "../src/tile/index.js";
import {Random} from "../src/math/random.js";

export default 
{
  mounted () 
  {
    const bgCanvas = this.$refs['bg-canvas'];
    const context = bgCanvas.getContext('2d');

    const appContainer = bgCanvas.parentElement.parentElement;

    const BG_SCALE = 3;
    const rand = new Random(7210701702);
    const forestTiles = loadForestTiles(() => renderCanvas());

    let renderCanvas = () => {
      bgCanvas.width = appContainer.clientWidth;
      bgCanvas.height = appContainer.clientHeight;
      bgCanvas.style.width = bgCanvas.width * BG_SCALE;

      const scaledTileSize = TILE_SIZE * BG_SCALE;
      const maxX = Math.ceil(bgCanvas.width / scaledTileSize);
      const maxY = Math.ceil(bgCanvas.height / scaledTileSize);
      for (let x = maxX; x >= 0; x--)
      {
        for (let y = 0; y <= maxY; y++)
        {
          context.drawImage(forestTiles[rand.nextInt() % forestTiles.length], (TILE_SIZE * x) - 2, (TILE_SIZE * y) - 2);
        }
      }
    };

    window.addEventListener("resize", renderCanvas);
    renderCanvas();
  }
}
</script>