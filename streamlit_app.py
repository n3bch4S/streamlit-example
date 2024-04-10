from streamlit.runtime.uploaded_file_manager import UploadedFile
import streamlit as st
import pandas as pd
from helperLib import ImageProcess, ImageStore
from PIL import Image
import helperLib.config as config


if __name__ == "__main__":
    print("Start")
    # Init page config and pre-define image storage
    st.set_page_config(page_title="Recolor ML", page_icon=":art:", layout="wide")
    if "origImageDict" not in st.session_state:
        st.session_state["origImageDict"] = {}
    origImageDict: dict[str, Image.Image] = st.session_state["origImageDict"]
    if "files" not in st.session_state:
        st.session_state["files"] = []
    files: list[UploadedFile] = st.session_state["files"]
    """
    # Colorizer

    ---
    """

    # Uploader
    uploadedFiles: list[UploadedFile] | None = st.file_uploader(
        label="Please put your image here :frame_with_picture:",
        accept_multiple_files=True,
        type=config.ACCEPT_TYPE,
    )
    if uploadedFiles is not None:
        ImageStore.updateFiles(files, uploadedFiles)
    hasSomeFile: bool = uploadedFiles is not None and len(uploadedFiles) > 0

    # Image menu
    toolsBox, fileSelectBox = st.columns(2)
    colorPicker, eraserButton, rotateLeftButton, rotateRightButton, resetButton = (
        toolsBox.columns(5)
    )

    selectedFilename: str | None = fileSelectBox.selectbox(
        label="Select the File",
        options=(
            map(ImageStore.getFilename, uploadedFiles)
            if uploadedFiles is not None
            else []
        ),
        disabled=not hasSomeFile,
        label_visibility="collapsed",
    )
    color: str = colorPicker.color_picker(
        label="Color Picker",
        value=config.DEFAULT_COLOR_PICKER,
        disabled=not hasSomeFile,
        label_visibility="collapsed",
    )
    isEraser: bool = eraserButton.checkbox(
        label="Eraser",
        disabled=not hasSomeFile,
    )
    rotateRightButton.button(
        label="Right",
        on_click=ImageProcess.rotateClockImgIn,
        args=(origImageDict, selectedFilename),
        disabled=not hasSomeFile,
        use_container_width=True,
    )
    rotateLeftButton.button(
        label="Left",
        on_click=ImageProcess.rotateAntiClockImgIn,
        args=(origImageDict, selectedFilename),
        disabled=not hasSomeFile,
        use_container_width=True,
    )
    resetButton.button(
        label="Reset",
        on_click=ImageStore.resetImageInDict,
        args=(selectedFilename, origImageDict, files),
        disabled=not hasSomeFile,
        use_container_width=True,
    )

    # Image showing
    processBox, originalBox = st.columns(2)
    ImageStore.updateImageDict(origImageDict, files)
    if selectedFilename is not None:
        processBox.image(
            image=origImageDict[selectedFilename],
            caption="Process",
            use_column_width=True,
        )
        originalBox.image(
            image=origImageDict[selectedFilename],
            caption="Original",
            use_column_width=True,
        )
    """
    ---

    *in progress*
    """
    print("done")
