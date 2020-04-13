import {TILE_SIZE} from "../tile/index.js";

const TARGET_FRAMERATE = 10;

class UIRenderer
{
  constructor(context, worldScale, uiScale)
  {
    this.context = context;
    this.worldScale = worldScale;
    this.uiScale = uiScale;

    this.selection = {x: 0, y: 0};
    this.context.canvas.addEventListener("mousemove", (e) =>
    {
      const tileX = Math.floor(e.clientX / (TILE_SIZE * this.worldScale));
      const tileY = Math.floor(e.clientY / (TILE_SIZE * this.worldScale));

      this.selection = {x: tileX, y: tileY};
    });

    const renderFrameCount = 60 / TARGET_FRAMERATE;
    let frameCount = 0;
    const renderLoop = () =>
    {
      frameCount++;
      if (frameCount > renderFrameCount)
      {
        this.render();
        frameCount = 0;
      }
      requestAnimationFrame(renderLoop);
    };
    requestAnimationFrame(renderLoop);
  }

  render()
  {
    this.context.clearRect(0, 0, this.context.canvas.width, this.context.canvas.height);

    this.drawReticule(this.selection.x, this.selection.y);
  }

  drawReticule(tileX, tileY)
  {
    const scaledTileSize = TILE_SIZE * this.worldScale;
    const x = tileX * scaledTileSize;
    const y = tileY * scaledTileSize;

    this.context.beginPath();
    this.context.moveTo(x, y);
    this.context.lineTo(x + scaledTileSize, y);
    this.context.lineTo(x + scaledTileSize, y + scaledTileSize);
    this.context.lineTo(x, y + scaledTileSize);
    this.context.lineTo(x, y);
    this.context.strokeStyle = "red";
    this.context.lineWidth = 2;
    this.context.stroke();
  }
}

export {UIRenderer};
