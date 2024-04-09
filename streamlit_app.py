from streamlit.runtime.uploaded_file_manager import UploadedFile
from streamlit.delta_generator import DeltaGenerator
import streamlit as st
import pandas as pd
from PIL import Image
import config


def getImgFileName(imgFile: UploadedFile) -> str:
    return imgFile.name


def getImgByName(
    imgList: list[UploadedFile] | None, fileName: str
) -> UploadedFile | None:
    if imgList is None:
        return imgList
    nameList = list(map(getImgFileName, imgList))
    idxFile = nameList.index(fileName)
    return imgList[idxFile]


if __name__ == "__main__":
    print("Start")
    """
    # Colorizer

    ---
    """

    # Uploader
    uploadedImgs: list[UploadedFile] | None = st.file_uploader(
        label="Please put your image here :frame_with_picture:",
        accept_multiple_files=True,
        type=config.ACCEPT_TYPE,
    )

    # Image menu
    toolsBox: DeltaGenerator
    fileSelectBox: DeltaGenerator
    toolsBox, fileSelectBox = st.columns(2)
    colorPickBox: DeltaGenerator
    eraserBox: DeltaGenerator
    rotateClockBox: DeltaGenerator
    rotateAntiClockBox: DeltaGenerator
    colorPickBox, eraserBox, rotateClockBox, rotateAntiClockBox = toolsBox.columns(4)
    color: str = colorPickBox.color_picker(
        label="colorpicker",
        value=config.DEFAULT_COLOR_PICKER,
        label_visibility="collapsed",
    )
    eraser: bool = eraserBox.checkbox(label="erase")
    rotateClock: bool = rotateClockBox.button(label="Clock", use_container_width=True)
    rotateAntiClock: bool = rotateAntiClockBox.button(
        label="Anti", use_container_width=True
    )
    fileSelect: str | None = fileSelectBox.selectbox(
        label="fileSelect",
        options=map(getImgFileName, uploadedImgs) if uploadedImgs is not None else [],
        label_visibility="collapsed",
    )

    # Image showing
    if fileSelect is not None:
        imgFile: UploadedFile | None = getImgByName(uploadedImgs, fileSelect)
        if imgFile is not None:
            st.image(image=imgFile)
    """
    ---

    *in progress*
    """
    print("done")
