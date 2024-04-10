from streamlit.runtime.uploaded_file_manager import UploadedFile
from PIL import Image


def executeFunctions(functions: list, args: list[tuple]) -> None:
    funcNum = len(functions)
    argNum = len(args)
    if funcNum != argNum:
        return

    for i in range(funcNum):
        func = functions[i]
        arg: tuple = args[i]
        func(*arg)


def hasImageBothName(
    imageName: str,
    origImageDict: dict[str, Image.Image],
    editingImageDict: dict[str, Image.Image],
) -> bool:
    return imageName in origImageDict and imageName in editingImageDict


def rotateBothImage(
    imageName: str,
    origImageDict: dict[str, Image.Image],
    editingImageDict: dict[str, Image.Image],
    rotateFunction,
) -> None:
    if not hasImageBothName(imageName, origImageDict, editingImageDict):
        return
    rotateFunction(origImageDict, imageName)
    rotateFunction(editingImageDict, imageName)


def resetBothImage(
    imageName: str,
    origImageDict: dict[str, Image.Image],
    editingImageDict: dict[str, Image.Image],
    referenceFiles: list[UploadedFile],
    resetFunction,
) -> None:
    if not hasImageBothName(imageName, origImageDict, editingImageDict):
        return
    resetFunction(imageName, origImageDict, referenceFiles)
    resetFunction(imageName, editingImageDict, referenceFiles)


if __name__ == "__main__":

    def func():
        print("call func")

    def func2(x, y):
        print("call func2")

    executeFunctions([func, func2], [(), (1, 2)])
