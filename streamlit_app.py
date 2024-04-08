from streamlit.runtime.uploaded_file_manager import UploadedFile
import streamlit as st
import pandas as pd
from PIL import Image
import config


def getImgByName(imgList: list[UploadedFile], fileName: str) -> UploadedFile:
    nameList = list(map(lambda imgFile: imgFile.name, imgList))
    idxFile = nameList.index(fileName)
    return imgList[idxFile]


if __name__ == "__main__":
    """
    # Colorizer

    ---
    """
    uploadedImgs = st.file_uploader(
        label="Please put your image here :frame_with_picture:",
        accept_multiple_files=True,
        type=config.ACCEPT_TYPE,
    )

    toolsBox, fileSelectBox = st.columns(2)
    colorPickBox, eraserBox, rotateClockBox, rotateAntiClockBox = toolsBox.columns(4)
    color = colorPickBox.color_picker(
        label="colorpicker",
        value=config.DEFAULT_COLOR_PICKER,
        label_visibility="collapsed",
    )
    eraser = eraserBox.checkbox(label="erase")
    rotateClock = rotateClockBox.button(label="Clock", use_container_width=True)
    rotateAntiClock = rotateAntiClockBox.button(label="Anti", use_container_width=True)
    fileSelect = fileSelectBox.selectbox(
        label="fileSelect",
        options=map(lambda x: x.name, uploadedImgs),
        label_visibility="collapsed",
    )

    st.image(image=getImgByName(uploadedImgs, fileSelect))
    """
    ---

    *in progress*
    """
