import streamlit as st

def instructions_page():
    st.markdown("1. Use the **Upload** tab for giving input histology images for segmentation. It is also possible to input multiple images at once.")
    st.markdown("2. After uploading, you can optionally choose to **Edit/Enhance Images** to crop/rotate your input, or directly **Submit for Segmentation**.")
    st.markdown("3. The model will now generate the segmentation masks. To directly compare the masked images to your input, use the option **Visualize Better**.")

    st.markdown('''
        <style>
            [data-testid="stMarkdownContainer"] ol {
                list-style-position: inside;
            }
        </style>
    ''', unsafe_allow_html=True)

    message = (
    '''Explore the **Visualize Better** option: 
    
    This is a feature that facilitates side-by-side comparison of images, 
    by overlaying the masked image over the input image. Use this for an 
    intuitive way to discern subtle differences and similarities.''')
    st.success(message)
