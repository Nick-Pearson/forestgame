<template>
  <canvas ref="main-canvas"></canvas>
</template>

<style>
html, body
{
  margin: 0;
  overflow: hidden;
}

#app
{
  margin: 0;
  height: 100%;
}
</style>

<script>
export default 
{
  mounted () {
    const canvas = this.$refs['main-canvas'];
    this.context = canvas.getContext('gl')

    let setCanvasSize = () => {
      canvas.width = canvas.parentElement.clientWidth;
      canvas.height = canvas.parentElement.clientHeight;
    };

    window.addEventListener("resize", setCanvasSize);
    setCanvasSize();
  }
}
</script>