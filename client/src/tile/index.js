import {loadImg, loadImgArray} from "../imagehelpers.js";

import Base0 from "./sprites/base0.png";
import Base1 from "./sprites/base1.png";

import Forest0 from "./sprites/forest0.png";
import Forest1 from "./sprites/forest1.png";

import Clearing0 from "./sprites/clearing0.png";
import Clearing1 from "./sprites/clearing1.png";
import Mountains0 from "./sprites/mountain0.png";

import TownHall from "./sprites/townhall.png";
import Farm from "./sprites/farm.png";
import Flag from "./sprites/flag.png";
import Windmill from "./sprites/windmill.png";
import Sawmill from "./sprites/sawmill.png";

const tileFilepaths =
{
  base: [Base0, Base1],
  forest: [Forest0, Forest1],
  clearing: [Base0, Base1, Clearing0, Clearing1],
  mountains: [Mountains0],
};

const buildingMetadata = [
  {
    "teamColour": [
      {"x": 22, "y": 45, "width": 4, "height": 14},
      {"x": 39, "y": 45, "width": 4, "height": 14},
      {"x": 22, "y": 22, "width": 4, "height": 13},
      {"x": 39, "y": 22, "width": 4, "height": 13},
    ],
  },
  {
    "teamColour": [
      {"x": 7, "y": 40, "width": 2, "height": 11},
      {"x": 11, "y": 40, "width": 2, "height": 11},
      {"x": 15, "y": 40, "width": 2, "height": 11},
      {"x": 19, "y": 40, "width": 2, "height": 11},
    ],
  },
  {},
  {},
  {},
];

function loadAllTiles(onload)
{
  return {
    base: loadImgArray(tileFilepaths.base, onload),
    forest: loadImgArray(tileFilepaths.forest, onload),
    clearing: loadImgArray(tileFilepaths.clearing, onload),
    mountains: loadImgArray(tileFilepaths.mountains, onload),
    townhall: loadImg(TownHall, onload),
    farm: loadImg(Farm, onload),
    flag: loadImg(Flag, onload),
    windmill: loadImg(Windmill, onload),
    sawmill: loadImg(Sawmill, onload),
  };
}

function loadForestTiles(onload)
{
  return loadImgArray(tileFilepaths.forest, onload);
}

const TILE_SIZE = 64;

const BASE_TILE_ID = 0;
const FOREST_TILE_ID = 1;
const CLEARING_TILE_ID = 2;
const MOUNTAIN_TILE_ID = 3;

export {tileFilepaths, loadAllTiles, loadForestTiles, buildingMetadata, TILE_SIZE, BASE_TILE_ID, FOREST_TILE_ID, CLEARING_TILE_ID, MOUNTAIN_TILE_ID};
