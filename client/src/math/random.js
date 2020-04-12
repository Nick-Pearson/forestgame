function evolveSeed(seed)
{
  return seed * 16807 % 2147483647;
}

class Random
{
  constructor(seed)
  {
    this.seed = seed;
  }

  nextInt(max)
  {
    this.seed = evolveSeed(this.seed);
    return this.seed % max;
  }
}

export {Random};
