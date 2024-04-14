from streamlit.runtime.uploaded_file_manager import UploadedFile
from PIL import Image
from helperLib import ImageProcess


def getFilename(file: UploadedFile) -> str:
    return file.name


def getFilenames(files: list[UploadedFile]) -> list[str]:
    return list(map(getFilename, files))


def getFileByName(files: list[UploadedFile], filename: str) -> UploadedFile | None:
    filenames: list[str] = getFilenames(files)
    if filename not in filenames:
        return None
    filePosition: int = filenames.index(filename)
    return files[filePosition]


def addFileToImageDict(file: UploadedFile, imageDict: dict[str, Image.Image]) -> None:
    filename: str = getFilename(file)
    if filename not in imageDict:
        imageDict[filename] = Image.open(file)


def editImageInDict(
    imageName: str, newFile: UploadedFile, imageDict: dict[str, Image.Image]
) -> None:
    if imageName in imageDict:
        imageDict[imageName] = Image.open(newFile)


def deleteImageInDict(imageName: str, imageDict: dict[str, Image.Image]) -> None:
    if imageName in imageDict:
        imageDict.pop(imageName)


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


def recolorImageFrom(
    origImageDict: dict[str, Image.Image],
    newImageDict: dict[str, Image.Image],
    imageName: str,
) -> None:
    if imageName not in origImageDict or imageName not in newImageDict:
        return
    image: Image.Image = origImageDict[imageName]
    newImageDict[imageName] = ImageProcess.recolorImage(image)


def updateFiles(files: list[UploadedFile], referenceFiles: list[UploadedFile]) -> None:
    referenceNames: list[str] = getFilenames(referenceFiles)
    filenames: list[str] = getFilenames(files)
    for i in range(len(files) - 1, -1, -1):
        filename: str = filenames[i]
        if filename not in referenceNames:
            files.pop(i)

    for i in range(len(referenceFiles)):
        referenceName: str = referenceNames[i]
        if referenceName not in filenames:
            filenames.append(referenceName)
            files.append(referenceFiles[i])


def updateImageDict(
    imageDict: dict[str, Image.Image], referenceFiles: list[UploadedFile]
) -> None:
    referenceNames: list[str] = getFilenames(referenceFiles)
    for imageName in list(imageDict):
        if imageName not in referenceNames:
            deleteImageInDict(imageName, imageDict)
    for referenceName in referenceNames:
        if referenceName not in imageDict:
            file: UploadedFile | None = getFileByName(referenceFiles, referenceName)
            if file is not None:
                addFileToImageDict(file, imageDict)


def resetImageInDict(
    imageName: str,
    imageDict: dict[str, Image.Image],
    referenceFiles: list[UploadedFile],
) -> None:
    file: UploadedFile | None = getFileByName(referenceFiles, imageName)
    if file is not None:
        editImageInDict(imageName, file, imageDict)


if __name__ == "__main__":
    d = {
        "1": 1,
        "2": 2,
        "3": 3,
    }
    d.pop("1")
    print(d)
