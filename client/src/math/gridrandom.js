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
    return this.data[x + (y * this.sizeX)];
  }
}

export {GridRandom};
