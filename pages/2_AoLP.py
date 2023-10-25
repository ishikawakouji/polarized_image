import streamlit as st
import polanalyser as pa
import cv2
import numpy as np

st.markdown("# AoLP page")
st.sidebar.markdown("# AoLP page")


@st.cache_data
def draw_aolp_images(org_img):
    # demosaic
    img_demosaiced_list = pa.demosaicing(org_img, pa.COLOR_PolarMono)

    # cal Stokes
    angles = np.deg2rad([0, 45, 90, 135])
    img_stokes = pa.calcStokes(img_demosaiced_list, angles)

    # convert to AoLP
    img_dolp = pa.cvtStokesToDoLP(img_stokes)  # [0, 1]
    img_aolp = pa.cvtStokesToAoLP(img_stokes)  # [0, pi]

    # apply colormap, adjust brightness
    img_aolp_u8 = pa.applyColorToAoLP(img_aolp)  # Hue = AoLP, Saturation = 1, Value = 1
    img_aolp_s_u8 = pa.applyColorToAoLP(
        img_aolp, saturation=img_dolp
    )  # Hue = AoLP, Saturation = DoLP, Value = 1
    img_aolp_v_u8 = pa.applyColorToAoLP(
        img_aolp, value=img_dolp
    )  # Hue = AoLP, Saturation = 1, Value = DoLP

    # convert BGR to RGB
    img_aolp_u8 = cv2.cvtColor(img_aolp_u8, cv2.COLOR_BGR2RGB)
    img_aolp_s_u8 = cv2.cvtColor(img_aolp_s_u8, cv2.COLOR_BGR2RGB)
    img_aolp_v_u8 = cv2.cvtColor(img_aolp_v_u8, cv2.COLOR_BGR2RGB)

    col1, col2 = st.columns(spec=[1, 1])

    with col1:
        st.image(img_aolp_u8, caption="AoLP")

    with col2:
        st.image(img_aolp_s_u8, caption="AoLP_s")
        st.image(img_aolp_v_u8, caption="AoLP_v")


if "org_image" in st.session_state:
    st.write(st.session_state["image_file"])

    # get image
    org_img = st.session_state["org_image"]

    draw_aolp_images(org_img)
