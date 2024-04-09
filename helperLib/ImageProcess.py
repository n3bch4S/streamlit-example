from streamlit.runtime.uploaded_file_manager import UploadedFile
from streamlit.delta_generator import DeltaGenerator
from PIL import Image, ImageEnhance


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


if __name__ == "__main__":
    img: Image.Image = Image.open("images/IMG_7863.jpeg")
    img.show()
    print(img.size, img.format, img.mode)
