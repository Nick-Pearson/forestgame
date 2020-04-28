import {Random} from "./random.js";

class GridRandom
{
  constructor(seed, sizeX, sizeY)
  {
    const rand = new Random(seed);
    const size = sizeX * sizeY;
    this.sizeX = sizeX;
    this.data = new Array(size);
    for (let i = 0; i < size; ++i)
    {
      this.data[i] = rand.nextInt();
    }
  }

  getRand(x, y)
  {
    const val = this.data[x + (y * this.sizeX)];
    if (val === undefined)
    {
      return 0;
    }
    else
    {
      return val;
    }
  }
}

export {GridRandom};
