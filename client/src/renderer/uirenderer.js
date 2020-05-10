import {TILE_SIZE} from "../tile/index.js";
import {loadAllSprites} from "../ui/index.js";

const TARGET_FRAMERATE = 10;

class UIRenderer
{
  constructor(context, game, uiScale)
  {
    this.context = context;
    this.game = game;
    this.uiScale = uiScale;
    this.sprites = loadAllSprites();

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

    this.drawReticule(this.game.selection.x, this.game.selection.y);
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
    const coords = this.game.world.getCoordsForTile(tileX, tileY);
    coords.x *= this.game.world.worldScale;
    coords.y += 2;
    coords.y *= this.game.world.worldScale;
    const scaledTileSize = TILE_SIZE * this.game.world.worldScale;

    this.context.beginPath();
    this.context.moveTo(coords.x, coords.y);
    this.context.lineTo(coords.x + scaledTileSize, coords.y);
    this.context.lineTo(coords.x + scaledTileSize - 1, coords.y + scaledTileSize - 1);
    this.context.lineTo(coords.x, coords.y + scaledTileSize - 1);
    this.context.lineTo(coords.x, coords.y);
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
    /*
    this.setTextSize(35);
    const textBoxSize = Math.max(140, 20 + this.context.measureText(stats.playerName).width);

    const namePanelHeight = this.sprites.panelB.height * 1.1;
    this.context.drawImage(this.sprites.panelB, 0, 0, textBoxSize, namePanelHeight);

    this.drawTextShadowed(stats.playerName, 10, 38, "white");
    */

    this.setTextSize(22);
    const statPanelHeight = this.sprites.panelA.height * 0.9;
    this.drawStatPanel(0, 0, stats.population, this.sprites.population);
    this.drawStatPanel(0, statPanelHeight, stats.wood, this.sprites.wood);
    this.drawStatPanel(0, statPanelHeight * 2, stats.food, this.sprites.food);
    this.drawStatPanel(0, statPanelHeight * 3, stats.coin, this.sprites.coin);
  }

  drawStatPanel(x, y, stat, icon)
  {
    const statPanelWidth = this.sprites.panelA.width * 0.8;
    const statPanelHeight = this.sprites.panelA.height * 0.9;
    this.context.drawImage(this.sprites.panelA, x - 5, y, statPanelWidth, statPanelHeight);
    this.context.drawImage(icon, x + 5, y + 8, 26, 26);
    this.drawTextShadowed(this.formatStat(stat), x + 40, y + 28, "white");
  }

  formatStat(stat)
  {
    if (stat < 1000)
    {
      return stat;
    }
    else if (stat < 10000)
    {
      return stat.toLocaleString();
    }
    else
    {
      return (stat / 1000).toFixed(1) + "k";
    }
  }
}

export {UIRenderer};
