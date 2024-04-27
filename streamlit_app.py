import streamlit as st
from streamlit_cropper import st_cropper
from PIL import Image
import io
from parts.instructions import instructions_page
from parts.sideb import sb
from parts.submitted import submitted_uploads_page
from parts.compare import compare_images
import copy

# Page Config
st.set_page_config(page_title="HistologyNet", page_icon="📋", initial_sidebar_state="expanded")

# Session-State Variables
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = None
    st.rerun()
if 'edited' not in st.session_state:
    st.session_state.edited = False
    st.rerun()
if 'names' not in st.session_state:
    st.session_state.names = []
    st.rerun()

# Some Functions
def basic_uploads_page():
    uploaded_files = st.file_uploader("Upload image(s) for segmentation here:", type=["jpg", "png"], accept_multiple_files=True)
    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files
        st.session_state.names = [image.name for image in st.session_state.uploaded_files]
    st.text("")

    _, _, btn1, btn2 = st.columns(4)

    if btn1.button("Enhance/Edit Images", help = "Crop/Rotate the input images before segmentation"):
        if st.session_state.uploaded_files is None:
            st.warning("Please select at least one image file to proceed.")
        else:
            st.session_state.page = "enhance_uploads"
            st.rerun()
    if btn2.button("Submit for Segmentation", help = "Directly submit the images to segmentation model"):
        if st.session_state.uploaded_files is None:
            st.warning("Please select at least one image file to proceed.")
        else:
            st.session_state.page = "submitted_uploads"
            st.rerun()

    st.markdown("***")
    st.write("Uploaded Images:")
    cols=st.columns(4)

    if (st.session_state.uploaded_files):
        for i,uploaded_file in enumerate(st.session_state.uploaded_files):
                try:
                    image_data = uploaded_file.read()
                    img = Image.open(io.BytesIO(image_data))
                    cols[i%4].image(img,caption=uploaded_file.name, use_column_width=True)
                    # st.image(img, caption=uploaded_file.name, use_column_width=False)
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}:{e}")

def enhance_uploads_page():
    # st.write("That will come from Shashank's code :) But for now just displaying the images as it is")
    images_uploaded = st.session_state.uploaded_files
    # images_uploaded=images_uploaded.copy()
    print(type(images_uploaded))
    # print(images_uploaded)
    image_enhance(images_uploaded)

    _, _, btn1, btn2 = st.columns(4)
    if btn1.button("Go Back", help = "Click to go back to file uploads page"):
        st.session_state.page = 'basic_uploads'
        st.rerun()
    if btn2.button("Submit", help = "Click here to submit these images to the model"):  
        if (st.session_state.edited == True):
            uploaded_files_copy = [copy.copy(uploaded_file) for uploaded_file in st.session_state.uploaded_files]
            for i in range(len(uploaded_files_copy)):
                if uploaded_files_copy[i].name in st.session_state.edited_images:
                    st.session_state.uploaded_files[i] = st.session_state.edited_images[uploaded_files_copy[i].name]
                else:
                    image_data = uploaded_files_copy[i].read()
                    st.session_state.uploaded_files[i] = Image.open(io.BytesIO(image_data))
        st.session_state.page = 'submitted_uploads'
        st.rerun()

def image_enhance(images_uploaded):
    img_map={img.name:copy.copy(img) for img in images_uploaded}

    if images_uploaded:
        # if 'rotation_angles' not in st.session_state:
        #     st.session_state.rotation_angles = {name: 0 for name in img_map.keys()}
        if 'edited_images' not in st.session_state:
            st.session_state.edited_images = {name: 0 for name in img_map.keys()}
        
        rotation_angles = {name: 0 for name in img_map.keys()}
        img_selected=st.selectbox("Chcekbox is here ", options=img_map.keys())
        
        image = Image.open(io.BytesIO(img_map[img_selected].read()))
        # print(type(image))


        # if 'rotation_angle' not in st.session_state or st.session_state.selected_image != img_selected:
        #     st.session_state.rotation_angle = 0
        #     st.session_state.selected_image = img_selected
        cropped_image = st_cropper(image)
        angle = st.slider('Select rotation angle:', -180, 180, rotation_angles[img_selected])

        rotation_angles[img_selected] = angle
        # print("angle saved to session state")
        rotated_image = cropped_image.rotate(angle, expand=False)
        # print("image rotated")
        st.image(rotated_image, caption="Rotated Image", use_column_width=True)

        # Button to apply edits and store the edited image
        if st.button('Apply Edits'):
            # Store the edited image in the session state
            st.session_state.edited_images[img_selected] = rotated_image
            st.success("Edits applied and image stored.")
            st.session_state.edited = True

# Side Bar
sb()

# Main Content Begins
st.title("HistologyNet")
st.markdown('''##### <span style="color:gray">Self-Supervised Segmentation Masking for Histology Images</span>
            ''', unsafe_allow_html=True)

tab_instr, tab_upload = st.tabs(["Instructions", "Upload"])

#-----------------
# Instructions Tab
#-----------------

with tab_instr:
    instructions_page()
    
#-----------------
# Upload Tab
#-----------------

with tab_upload:
    if 'page' not in st.session_state:
        st.session_state.page = "basic_uploads"
        st.rerun()

    if st.session_state.page == "basic_uploads":
        basic_uploads_page()

    elif st.session_state.page == "enhance_uploads":
        enhance_uploads_page()

    elif st.session_state.page == "submitted_uploads":
        submitted_uploads_page()

    elif st.session_state.page == "compare_uploads":
        compare_images()

    
