import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.markdown("# import image page")
st.sidebar.markdown("# import image page")

uploaded_file = st.sidebar.file_uploader("upload image")

if uploaded_file:
    st.session_state["image_file"] = uploaded_file.name
    st.write(st.session_state.image_file)
    image = Image.open(uploaded_file)
    org_img = np.array(image)
    st.session_state["org_image"] = org_img
    st.image(org_img)
else:
    if "image_file" in st.session_state:
        st.image(st.session_state["org_image"])
