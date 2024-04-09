from inspect import getfile
from streamlit.runtime.uploaded_file_manager import UploadedFile
from PIL import Image


def getImgFileName(imgFile: UploadedFile) -> str:
    return imgFile.name


def getFileNameList(imageFiles: list[UploadedFile]) -> list[str]:
    return list(map(getImgFileName, imageFiles))


def getImgFileByName(
    imgList: list[UploadedFile] | None, fileName: str
) -> UploadedFile | None:
    if imgList is None:
        return imgList
    nameList = list(map(getImgFileName, imgList))
    idxFile = nameList.index(fileName)
    return imgList[idxFile]


def updateImageFileList(
    files: list[UploadedFile], refFiles: list[UploadedFile]
) -> None:
    refNames = getFileNameList(refFiles)
    filesName = getFileNameList(files)
    for i in range(len(files) - 1, -1, -1):
        filename = filesName[i]
        if filename not in refNames:
            files.pop(i)

    filesName = getFileNameList(files)
    for i in range(len(refFiles)):
        refname = refNames[i]
        if refname not in filesName:
            files.append(refFiles[i])
            filesName.append(getImgFileName(refFiles[i]))


def updateImageDict(
    imgDict: dict[str, Image.Image], listOfFile: list[UploadedFile] | None
) -> None:
    if listOfFile is None:
        imgDict.clear()
        return

    fileNames: list[str] = getFileNameList(listOfFile)
    for imageName in list(imgDict.keys()):
        if imageName not in fileNames:
            # print(f"delete {imageName}")
            del imgDict[imageName]
    for fileName in fileNames:
        if fileName not in imgDict:
            imageFile: UploadedFile | None = getImgFileByName(listOfFile, fileName)
            if imageFile is not None:
                # print(f"add {fileName}")
                imgDict[fileName] = Image.open(imageFile)


def resetImageDict(
    imageDict: dict[str, Image.Image], listOfFile: list[UploadedFile], imageName: str
) -> None:
    imageFile: UploadedFile | None = getImgFileByName(
        imgList=listOfFile, fileName=imageName
    )
    if imageFile is not None:
        imageDict[imageName] = Image.open(imageFile)


if __name__ == "__main__":
    d = {
        "1": Image.open("images/IMG_7863.jpeg"),
        "2": Image.open("images/pitcher1_660cdc9fa0014.jpeg"),
        "3": Image.open("images/pitcher2_660cdcb4f0774.jpeg"),
    }
