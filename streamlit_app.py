from streamlit.runtime.uploaded_file_manager import UploadedFile
from streamlit.delta_generator import DeltaGenerator
import streamlit as st
import pandas as pd
from helperLib import ImageProcess, ImageStore
from PIL import Image
import helperLib.config as config


if __name__ == "__main__":
    print("Start")
    # Init page config and pre-define image storage
    st.set_page_config(page_title="Recolor ML", page_icon=":art:", layout="wide")
    if "imageDict" not in st.session_state:
        st.session_state["imageDict"] = {}
    imgDict: dict[str, Image.Image] = st.session_state["imageDict"]
    if "files" not in st.session_state:
        st.session_state["files"] = []
    files: list[UploadedFile] = st.session_state["files"]
    if "fileSelectNow" not in st.session_state:
        st.session_state["fileSelectNow"] = ""
    """
    # Colorizer

    ---
    """

    # Uploader
    uploadedImgs: list[UploadedFile] | None = st.file_uploader(
        label="Please put your image here :frame_with_picture:",
        accept_multiple_files=True,
        on_change=ImageStore.updateImageDict,
        kwargs={"imgDict": imgDict, "listOfFile": files},
        type=config.ACCEPT_TYPE,
    )
    if uploadedImgs is not None:
        ImageStore.updateImageFileList(files=files, refFiles=uploadedImgs)

    # Image menu
    # toolsBox: DeltaGenerator
    # fileSelectBox: DeltaGenerator
    # colorPickBox: DeltaGenerator
    # eraserBox: DeltaGenerator
    # rotateClockBox: DeltaGenerator
    # rotateAntiClockBox: DeltaGenerator
    # resetBox: DeltaGenerator
    toolsBox, fileSelectBox = st.columns(2)
    colorPickBox, eraserBox, rotateAntiClockBox, rotateClockBox, resetBox = (
        toolsBox.columns(5)
    )

    fileSelect: str | None = fileSelectBox.selectbox(
        label="fileSelect",
        options=(
            map(ImageStore.getImgFileName, uploadedImgs)
            if uploadedImgs is not None
            else []
        ),
        label_visibility="collapsed",
    )
    if fileSelect is not None:
        st.session_state["fileSelectNow"] = fileSelect
    color: str = colorPickBox.color_picker(
        label="colorpicker",
        value=config.DEFAULT_COLOR_PICKER,
        label_visibility="collapsed",
    )
    eraser: bool = eraserBox.checkbox(label="erase")
    rotateClock: bool = rotateClockBox.button(
        label="Clock",
        on_click=ImageProcess.rotateClockImgIn,
        kwargs={"imgDict": imgDict, "imgFileName": st.session_state["fileSelectNow"]},
        use_container_width=True,
    )
    rotateAntiClock: bool = rotateAntiClockBox.button(
        label="Anti",
        on_click=ImageProcess.rotateAntiClockImgIn,
        kwargs={"imgDict": imgDict, "imgFileName": st.session_state["fileSelectNow"]},
        use_container_width=True,
    )
    resetBtn: bool = resetBox.button(
        label="reset",
        on_click=ImageStore.resetImageDict,
        kwargs={
            "imageDict": imgDict,
            "listOfFile": files,
            "imageName": st.session_state["fileSelectNow"],
        },
        use_container_width=True,
    )

    # Image showing
    if fileSelect is not None:
        imgFile: UploadedFile | None = ImageStore.getImgFileByName(
            uploadedImgs, fileSelect
        )
        if imgFile is not None:
            if fileSelect not in imgDict:
                imgDict[fileSelect] = Image.open(imgFile)
            img: Image.Image = imgDict[fileSelect]
            # img.show()
            st.image(image=st.session_state["imageDict"][fileSelect])
    """
    ---

    *in progress*
    """
    print("done")
