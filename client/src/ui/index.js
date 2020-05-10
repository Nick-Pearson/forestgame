import {loadImg} from "../imagehelpers.js";

import BrownButton from "./sprites/buttonLong_brown.png";
import BlueButton from "./sprites/buttonLong_blue.png";

import Coin from "./sprites/coin.png";
import Food from "./sprites/food.png";
import Population from "./sprites/population.png";
import Wood from "./sprites/wood.png";

function loadAllSprites(onload)
{
  return {
    panelA: loadImg(BrownButton, onload),
    panelB: loadImg(BlueButton, onload),
    coin: loadImg(Coin, onload),
    food: loadImg(Food, onload),
    population: loadImg(Population, onload),
    wood: loadImg(Wood, onload),
  };
}

export {loadAllSprites};
