<template>
  <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <circle cx="50" cy="50" r="45"/>
  </svg>
</template>

<style scoped>
svg
{
  width: 50px;
  animation: 2s linear infinite svg-animation;
}
@keyframes svg-animation 
{
  0% {
    transform: rotateZ(0deg);
  }
  100% {
    transform: rotateZ(360deg)
  }
}


circle
{
  max-width: 100px;
  fill: transparent;
  stroke: #2f3d4c;
  stroke-width: 10;
  stroke-dasharray: 283;
  stroke-linecap: round;
  transform-origin: 50% 50%;

  animation-duration: 1.4s;
  animation-timing-function: ease-in-out;
  animation-iteration-count: infinite;
  animation-fill-mode: both;
  animation-name: spinner-animation;
}
@keyframes spinner-animation 
{
  0%,
  25% {
    stroke-dashoffset: 280;
    transform: rotate(0);
  }
  
  50%,
  75% {
    stroke-dashoffset: 75;
    transform: rotate(45deg);
  }
  
  100% {
    stroke-dashoffset: 280;
    transform: rotate(360deg);
  }
}
</style>