import {TILE_SIZE} from "../tile/index.js";

const TARGET_FRAMERATE = 10;

class UIRenderer
{
  constructor(context, game, worldScale, uiScale)
  {
    this.context = context;
    this.game = game;
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
    this.drawStatsBox(this.game.playerStats);
  }

  drawTextShadowed(text, x, y, colour)
  {
    this.context.fillStyle = "black";
    this.context.fillText(text, x + 2, y + 2);
    this.context.fillStyle = colour;
    this.context.fillText(text, x, y);
  }

  drawTextShadowedRight(text, x, y, colour)
  {
    const textWidth = this.context.measureText(text).width;
    this.drawTextShadowed(text, x - textWidth, y, colour);
  }

  drawReticule(tileX, tileY)
  {
    const scaledTileSize = TILE_SIZE * this.worldScale;
    const x = tileX * scaledTileSize;
    const y = tileY * scaledTileSize;

    this.context.beginPath();
    this.context.moveTo(x, y);
    this.context.lineTo(x + scaledTileSize, y);
    this.context.lineTo(x + scaledTileSize - 1, y + scaledTileSize - 1);
    this.context.lineTo(x, y + scaledTileSize - 1);
    this.context.lineTo(x, y);
    this.context.strokeStyle = "red";
    this.context.lineJoin = "miter";
    this.context.lineWidth = 2;
    this.context.stroke();
  }

  setTextSize(size)
  {
    this.context.font = size + "px Arbutus Slab";
  }

  drawStatsBox(stats)
  {
    this.setTextSize(35);
    const textBoxSize = Math.max(140, 20 + this.context.measureText(stats.playerName).width);

    this.context.fillStyle = "#7c5542";
    this.context.fillRect(0, 0, textBoxSize, 50);
    this.context.fillRect(0, 50, 120, 110);

    this.drawTextShadowed(stats.playerName, 10, 35, "white");

    this.context.beginPath();
    this.context.moveTo(0, 50);
    this.context.lineTo(textBoxSize, 50);
    this.context.lineTo(textBoxSize, 0);
    this.context.strokeStyle = "#44200f";
    this.context.lineJoin = "round";
    this.context.lineWidth = 7;
    this.context.stroke();

    this.setTextSize(18);
    this.drawTextShadowed("Pop.", 8, 75, "white");
    this.drawTextShadowedRight(stats.population, 110, 75, "white");
    this.drawTextShadowed("Wood", 8, 100, "white");
    this.drawTextShadowedRight(stats.wood, 110, 100, "white");
    this.drawTextShadowed("Coin", 8, 125, "white");
    this.drawTextShadowedRight(stats.coin, 110, 125, "white");
    this.drawTextShadowed("Food", 8, 150, "white");
    this.drawTextShadowedRight(stats.food, 110, 150, "white");

    this.context.beginPath();
    this.context.moveTo(120, 50);
    this.context.lineTo(120, 160);
    this.context.lineTo(0, 160);
    this.context.strokeStyle = "#44200f";
    this.context.lineJoin = "round";
    this.context.lineWidth = 4;
    this.context.stroke();
  }
}

export {UIRenderer};
