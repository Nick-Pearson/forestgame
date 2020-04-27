import {World} from "./world";
import {PlayerStats} from "./player/playerstats.js";
import {FOREST_TILE_ID, TILE_SIZE} from "./tile";

class ForestGame
{
  constructor(gameId)
  {
    this.gameId = gameId;

    this.world = new World(gameId);
    this.playerStats = new PlayerStats(gameId);
    this.playerStats.refresh();

    this.setupKeyBinds();

    this.moveDirection = {x: 0, y: 0};

    let lastFrameTime = performance.now();
    const animationFrame = () =>
    {
      const now = performance.now();
      const deltaTime = now - lastFrameTime;

      this.update(deltaTime / 1000);

      lastFrameTime = now;
      requestAnimationFrame(animationFrame);
    };
    animationFrame();
  };

  update(deltaTime)
  {
    const CAMERA_MOVE_SPEED = 40.0;
    this.world.moveCamera(
        this.moveDirection.x * deltaTime * CAMERA_MOVE_SPEED,
        this.moveDirection.y * deltaTime * CAMERA_MOVE_SPEED,
    );
  }

  setupKeyBinds()
  {
    document.addEventListener("mousedown", (e) =>
    {
      const coords = this.world.getTileFromCoords(e.clientX, e.clientY);
      this.onClick(coords.x, coords.y);
    });

    document.addEventListener("keydown", (e) =>
    {
      if (e.repeat) return;

      if (e.key == "ArrowLeft")
      {
        this.moveDirection.x = 1;
      }
      else if (e.key == "ArrowRight")
      {
        this.moveDirection.x = -1;
      }
      else if (e.key == "ArrowUp")
      {
        this.moveDirection.y = 1;
      }
      else if (e.key == "ArrowDown")
      {
        this.moveDirection.y = -1;
      }
    });
    document.addEventListener("keyup", (e) =>
    {
      if (e.key == "ArrowLeft" || e.key == "ArrowRight")
      {
        this.moveDirection.x = 0;
      }
      else if (e.key == "ArrowUp" || e.key == "ArrowDown")
      {
        this.moveDirection.y = 0;
      }
    });
  }

  onClick(x, y)
  {
    const tileId = this.world.getTileAt(x, y);

    if (tileId == FOREST_TILE_ID)
    {
      this.world.actionDeforest(x, y, () =>
      {
        this.playerStats.refresh();
      });
    }
  }

  onCanvasSizeChanged(sizeX, sizeY)
  {
    const worldSizeX = this.world.getSizeX();
    const worldSizeY = this.world.getSizeY();
    const offsetX = this.calculateCameraOffset(sizeX, worldSizeX);
    const offsetY = this.calculateCameraOffset(sizeY, worldSizeY);

    this.world.setWorldPosition(offsetX, offsetY);
  }

  calculateCameraOffset(canvasSize, worldSize)
  {
    const halfCanvasWidth = Math.round(canvasSize / (2 * this.world.worldScale));
    const halfWorldWidth = TILE_SIZE * worldSize / 2;
    return halfCanvasWidth - halfWorldWidth;
  }
}

export {ForestGame};
