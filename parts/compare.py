import streamlit as st
from PIL import Image
import io
from streamlit_image_comparison import image_comparison

def compare_images():
    for i in range(len(st.session_state.uploaded_files)):
        if st.session_state.edited == True:
            input_image = st.session_state.uploaded_files[i]
        else:
            image_data = st.session_state.uploaded_files[i].read()
            input_image = Image.open(io.BytesIO(image_data))
        image_comparison(
            input_image,
            st.session_state.segmented_files[i],
            label1 = "Original",
            label2 = "Masked"
        )