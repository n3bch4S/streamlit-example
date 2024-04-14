from PIL import Image
from skimage import color
from numpy import ndarray
from torch import Tensor
from torchvision import transforms
from helperLib import config, model

import numpy as np
import torch

predict: model.vanilla_autoencoder = model.getTrainedModel()


def preserveResize(
    oldImage: Image.Image, newLongSide: int = config.LONG_SIDE
) -> Image.Image:
    oldSize: tuple[int, int] = oldImage.size
    oldLongSide: int = max(oldSize)
    scaling: float = newLongSide / oldLongSide
    newWidth: int = round(oldSize[0] * scaling)
    newHeight: int = round(oldSize[1] * scaling)
    newSize: tuple[int, int] = (newWidth, newHeight)
    newImage: Image.Image = oldImage.resize(newSize)
    return newImage


def preprocessImage(image: Image.Image) -> tuple[Tensor, Tensor]:
    image = image.convert("RGB")

    image = transforms.Resize((config.MODEL_WIDTH, config.MODEL_HEIGHT), Image.BICUBIC)(  # type: ignore
        image
    )
    resizeImage: ndarray = np.array(image)

    labImage: ndarray = color.rgb2lab(resizeImage).astype("float32")
    tensorImage: Tensor = transforms.ToTensor()(labImage)

    LImage: Tensor = tensorImage[[0], ...]
    allLImage: Tensor = torch.cat((LImage, LImage, LImage), dim=0).reshape(
        1, 3, config.MODEL_HEIGHT, config.MODEL_HEIGHT
    )
    return allLImage, LImage


def postProcessImage(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    newImage: Image.Image = image.resize(size)
    return newImage


def reconstructImage(ABImage, LImage: Tensor) -> Image.Image:
    labMatrix: ndarray = np.zeros((224, 224, 3))
    labMatrix[:, :, 0] = LImage[0, 0].numpy()
    labMatrix[:, :, 1] = ABImage[0, 0].detach().numpy() * 128
    labMatrix[:, :, 2] = ABImage[0, 1].detach().numpy() * 128
    rgbMatrix: ndarray = (color.lab2rgb(labMatrix) * 255).astype(np.uint8)
    completeImage: Image.Image = Image.fromarray(rgbMatrix)
    return completeImage


def recolorImage(image: Image.Image) -> Image.Image:
    imageSize = image.size
    allLImage, LImage = preprocessImage(image)
    ABImage = predict(allLImage)
    coloredImage: Image.Image = reconstructImage(ABImage, LImage)
    coloredImage = postProcessImage(coloredImage, imageSize)
    return coloredImage


if __name__ == "__main__":
    img: Image.Image = Image.open("helperLib/cat.jpg")
    img.show()
    predictedImage: Image.Image = recolorImage(img)
    predictedImage.show()
