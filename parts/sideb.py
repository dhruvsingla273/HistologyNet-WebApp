import streamlit as st

def sb():
    col1, col2, col3 = st.sidebar.columns([1,8,1])
    with col1:
        st.write("")
    with col2:
        st.image('statics/sample_image.png',  use_column_width=True)
    with col3:
        st.write("")

    st.sidebar.markdown(" ## About HistologyNet")    
    st.sidebar.markdown("We've trained a model that achieves binary segmentation of histology images. Our model is self-supervised and makes use of unlabelled images, without the need for extensive manual annotation. To see the custom results for your images, head over to the uploads section!")           
    st.sidebar.info("Our code for segmentation as well as webpage is available on [Github](https://github.com/dhruvsingla273/HistologyNet-WebApp.git).", icon="ℹ️")
