function loadImgArray(images, onload)
{
  const imgs = [];
  images.forEach((image) =>
  {
    imgs.push(loadImg(image, onload));
  });
  return imgs;
}

function loadImg(image, onload)
{
  const img = new Image();
  img.onload = onload;
  img.src = image;
  return img;
}

export {loadImgArray, loadImg};
