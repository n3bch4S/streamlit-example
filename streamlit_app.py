from streamlit.runtime.uploaded_file_manager import UploadedFile
import streamlit as st
import pandas as pd
from helperLib import ImageProcess, ImageStore, ComponentControl
from PIL import Image
from helperLib import config


if __name__ == "__main__":
    print("Start")
    # Init page config and pre-define image storage
    st.set_page_config(page_title="Recolor ML", page_icon=":art:", layout="wide")
    if "origImageDict" not in st.session_state:
        st.session_state["origImageDict"] = {}
    origImageDict: dict[str, Image.Image] = st.session_state["origImageDict"]
    if "editingImageDict" not in st.session_state:
        st.session_state["editingImageDict"] = {}
    editingImageDict: dict[str, Image.Image] = st.session_state["editingImageDict"]
    if "files" not in st.session_state:
        st.session_state["files"] = []
    files: list[UploadedFile] = st.session_state["files"]
    """
    # Colorizer

    ---
    ## 1. Upload your image :frame_with_picture:
    Before we start, upload your image below! You can also drag & drop the file into this area to upload it.
    """

    # Uploader
    uploadedFiles: list[UploadedFile] | None = st.file_uploader(
        label="Please put your image here.",
        accept_multiple_files=True,
        type=config.ACCEPT_TYPE,
        label_visibility="collapsed",
    )
    if uploadedFiles is not None:
        ImageStore.updateFiles(files, uploadedFiles)
    hasSomeFile: bool = uploadedFiles is not None and len(uploadedFiles) > 0

    # Image menu
    """
    ## 2. Edit your image :wrench:
    After you have uploaded an image, click on one of these options to edit your image.
    """
    toolsBox, fileSelectBox = st.columns(2)
    colorPicker, eraserButton, rotateLeftButton, rotateRightButton, resetButton = (
        toolsBox.columns(5)
    )

    selectedFilename: str | None = fileSelectBox.selectbox(
        label="Select the desire image to edit.",
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
        on_click=ComponentControl.rotateBothImage,
        args=(
            selectedFilename,
            origImageDict,
            editingImageDict,
            ImageProcess.rotateClockImgIn,
        ),
        disabled=not hasSomeFile,
        use_container_width=True,
    )
    rotateLeftButton.button(
        label="Left",
        on_click=ComponentControl.rotateBothImage,
        args=(
            selectedFilename,
            origImageDict,
            editingImageDict,
            ImageProcess.rotateAntiClockImgIn,
        ),
        disabled=not hasSomeFile,
        use_container_width=True,
    )
    resetButton.button(
        label="Reset",
        on_click=ComponentControl.resetBothImage,
        args=(
            selectedFilename,
            origImageDict,
            editingImageDict,
            files,
            ImageStore.resetImageInDict,
        ),
        disabled=not hasSomeFile,
        use_container_width=True,
    )

    # Image showing
    processBox, originalBox = st.columns(2)
    ImageStore.updateImageDict(origImageDict, files)
    ImageStore.updateImageDict(editingImageDict, files)
    if selectedFilename is not None:
        processBox.image(
            image=editingImageDict[selectedFilename],
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
