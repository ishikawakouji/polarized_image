import streamlit as st
import polanalyser as pa
import cv2
import numpy as np

st.markdown("# DoLP page")
st.sidebar.markdown("# DoLP page")


def adjust_gamma(image, gamma):
    image_u8 = np.clip(image, 0, 255).astype(np.uint8)
    table = (255.0 * (np.linspace(0, 1, 256) ** gamma)).astype(np.uint8)
    return cv2.LUT(image_u8, table)


def generate_colormap(color0, color1):
    colormap = np.zeros((256, 3), dtype=np.uint8)
    colormap[:128] = np.linspace(1, 0, 128)[..., None] * np.array(color0)
    colormap[128:] = np.linspace(0, 1, 128)[..., None] * np.array(color1)
    return np.clip(colormap, 0, 255)


if "org_image" in st.session_state:
    st.write(st.session_state["image_file"])

    # get image
    org_img = st.session_state["org_image"]

    # demosaic
    img_demosaiced_list = pa.demosaicing(org_img, pa.COLOR_PolarMono)

    # cal Stokes
    angles = np.deg2rad([0, 45, 90, 135])
    img_stokes = pa.calcStokes(img_demosaiced_list, angles)

    # stokes to parameters
    img_s0 = img_stokes[..., 0]
    img_s1 = img_stokes[..., 1]
    img_s2 = img_stokes[..., 2]
    img_intensity = pa.cvtStokesToIntensity(img_stokes)  # same as s0

    # convert to DoLP, AoLP
    img_dolp = pa.cvtStokesToDoLP(img_stokes)  # [0, 1]
    img_aolp = pa.cvtStokesToAoLP(img_stokes)  # [0, pi]

    # colormap (Positive -> Green, Negative -> Red)
    custom_colormap = generate_colormap((0, 0, 255), (0, 255, 0))

    # Apply colormap or adjust the brightness to export images
    img_s0_u8 = pa.applyColorMap(img_s0, "viridis", vmin=0, vmax=np.max(img_s0))
    img_s1_u8 = pa.applyColorMap(
        img_s1 / img_s0, custom_colormap, vmin=-1, vmax=1
    )  # normalized by s0
    img_s2_u8 = pa.applyColorMap(
        img_s2 / img_s0, custom_colormap, vmin=-1, vmax=1
    )  # normalized by s0
    img_intensity_u8 = adjust_gamma(img_intensity * 0.5, gamma=(1 / 2.2))
    img_dolp_u8 = np.clip(img_dolp * 255, 0, 255).astype(np.uint8)

    # convert BGR to RGB
    img_s0_u8 = cv2.cvtColor(img_s0_u8, cv2.COLOR_BGR2RGB)
    img_s1_u8 = cv2.cvtColor(img_s1_u8, cv2.COLOR_BGR2RGB)
    img_s2_u8 = cv2.cvtColor(img_s2_u8, cv2.COLOR_BGR2RGB)

    col1, col2 = st.columns(spec=[1, 1])

    with col1:
        st.image(img_dolp_u8, caption="DoLP")
        st.image(img_intensity_u8, caption="intensity (=s0)")

    with col2:
        st.image(img_s0_u8, caption="s0")
        st.image(img_s1_u8, caption="s1")
        st.image(img_s2_u8, caption="s2")
