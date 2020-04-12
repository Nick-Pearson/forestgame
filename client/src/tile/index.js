import Base from "./sprites/base.png";

import Forest0 from "./sprites/forest0.png";
import Forest1 from "./sprites/forest1.png";

import Clearing0 from "./sprites/clearing0.png";
import Clearing1 from "./sprites/clearing1.png";
import Clearing2 from "./sprites/clearing2.png";

import Mountains0 from "./sprites/mountain0.png";

const tileFilepaths =
{
  base: [Base],
  forest: [Forest0, Forest1],
  clearing: [Clearing0, Clearing1, Clearing2],
  mountains: [Mountains0],
};

function loadAllTiles(onload)
{
  return {
    base: loadImgArray(tileFilepaths.base, onload),
    forest: loadImgArray(tileFilepaths.forest, onload),
    clearing: loadImgArray(tileFilepaths.clearing, onload),
    mountains: loadImgArray(tileFilepaths.mountains, onload),
  };
}

function loadImgArray(images, onload)
{
  const imgs = [];
  images.forEach((image) =>
  {
    const img = new Image();
    img.onload = onload;
    img.src = image;
    imgs.push(img);
  });
  return imgs;
}

const TILE_SIZE = 16;

export {tileFilepaths, loadAllTiles, TILE_SIZE};
