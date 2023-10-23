import streamlit as st
import cv2
import polanalyser as pa

st.markdown("# demosaic page")
st.sidebar.markdown("# demosaic page")

if "image_file" in st.session_state:
    st.write(st.session_state["image_file"])

    # Demosaicing
    img_000, img_045, img_090, img_135 = pa.demosaicing(
        st.session_state["org_image"], pa.COLOR_PolarMono
    )

    col1, col2 = st.columns(spec=[1, 1])

    with col1:
        st.image(img_000, caption="000")
        st.image(img_135, caption="135")

    with col2:
        st.image(img_045, caption="045")
        st.image(img_090, caption="090")
