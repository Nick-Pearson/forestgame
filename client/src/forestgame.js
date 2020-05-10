import {World} from "./world";
import {PlayerStats} from "./player/playerstats.js";
import {TILE_SIZE} from "./tile";
import {restRequest} from "./io.js";

class ForestGame
{
  constructor(gameId, div, domModel)
  {
    this.gameId = gameId;
    this.domModel = domModel;

    this.world = new World(gameId);
    this.playerStats = new PlayerStats(gameId);
    this.playerStats.refreshAll();
    this.selection = {x: 0, y: 0};
    this.buildingData = [];

    this.setupKeyBinds(div);
    this.loadStaticData();

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
    const CAMERA_MOVE_SPEED = 180.0 / this.world.worldScale;
    this.world.moveCamera(
        this.moveDirection.x * deltaTime * CAMERA_MOVE_SPEED,
        this.moveDirection.y * deltaTime * CAMERA_MOVE_SPEED,
    );
  }

  setupKeyBinds(div)
  {
    div.addEventListener("mousedown", (e) =>
    {
      this.updateSelectedTile(e.clientX, e.clientY);
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
    document.addEventListener("mousemove", (e) =>
    {
      if (!this.domModel.showMenu)
      {
        this.updateSelectedTile(e.clientX, e.clientY);
      }
    });
  }

  updateSelectedTile(x, y)
  {
    this.selection = this.world.getTileFromCoords(x, y);
  }

  onClick(x, y)
  {
    if (this.domModel.showMenu)
    {
      this.domModel.showMenu = false;
      return;
    }

    const coords = this.world.getCoordsForTile(x + 1, y);

    this.generateTileMenu();
    this.domModel.showMenu = true;
    this.domModel.menuX = coords.x * this.world.worldScale;
    this.domModel.menuY = coords.y * this.world.worldScale;
  }

  generateTileMenu()
  {
    const buildingMenu = [];

    this.buildingData.forEach((building) =>
    {
      if (!building.buildable) return;
      const menuItem = {
        "label": building["name"],
        "eventId": building["id"],
      };
      buildingMenu.push(menuItem);
    });

    this.domModel.menuItems = [
      {
        "label": "Clear Trees",
        "eventId": "deforest",
      },
      {
        "label": "Build",
        "eventId": "build",
        "children": buildingMenu,
      },
    ];
  }

  onMenuEvent(eventId)
  {
    console.log("Got menu event " + eventId);
    if (eventId[0] === "deforest")
    {
      this.actionDeforest();
    }
    else if (eventId[0] === "build" && eventId.length > 1)
    {
      console.log("building " + eventId[1]);
      this.actionBuild(eventId[1]);
    }
  }

  actionDeforest()
  {
    this.world.actionDeforest(this.selection.x, this.selection.y, () =>
    {
      this.playerStats.refreshStats();
    });
    this.domModel.showMenu = false;
  }

  actionBuild(buildingId)
  {
    this.world.actionBuild(buildingId, this.selection.x, this.selection.y, () =>
    {
      this.playerStats.refreshStats();
    });
    this.domModel.showMenu = false;
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

  loadStaticData()
  {
    restRequest({method: "GET", path: "/buildings"}, (resp) =>
    {
      this.buildingData = resp.body["buildings"];
    });
  }
}

export {ForestGame};
