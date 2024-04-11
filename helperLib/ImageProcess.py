from streamlit.runtime.uploaded_file_manager import UploadedFile
from streamlit.delta_generator import DeltaGenerator
from PIL import Image, ImageEnhance
from helperLib import config


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


def rotateClockImgIn(imgDict: dict[str, Image.Image], imgFileName: str) -> None:
    if imgFileName not in imgDict:
        return
    img: Image.Image = imgDict[imgFileName]
    imgDict[imgFileName] = img.rotate(angle=-90, expand=True)


def rotateAntiClockImgIn(imgDict: dict[str, Image.Image], imgFileName: str) -> None:
    if imgFileName not in imgDict:
        return
    img: Image.Image = imgDict[imgFileName]
    imgDict[imgFileName] = img.rotate(angle=90, expand=True)


def smallenImageIn(imageDict: dict[str, Image.Image], imageName: str) -> None:
    if imageName not in imageDict:
        return
    image: Image.Image = imageDict[imageName]
    imageDict[imageName] = image.resize(
        size=(config.MODEL_WIDTH, config.MODEL_HEIGHT),
    )


def greyingImageIn(imageDict: dict[str, Image.Image], imageName: str) -> None:
    if imageName not in imageDict:
        return
    image: Image.Image = imageDict[imageName]
    imageDict[imageName] = image.convert(mode="L")


def preprocessImage(image: Image.Image) -> Image.Image:
    image = image.convert(mode="L")
    image = image.resize(
        size=(config.MODEL_WIDTH, config.MODEL_HEIGHT),
    )
    return image


if __name__ == "__main__":
    img: Image.Image = Image.open("images/IMG_7863.jpeg")
    img.show()
    print(img.size, img.format, img.mode)
