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

  nextInt()
  {
    this.seed = evolveSeed(this.seed);
    return this.seed;
  }
}

export {Random};
