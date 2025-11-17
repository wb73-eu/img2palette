import streamlit as st
from palette_extractor import get_palette

st.title("img2palette")
st.header("by Walid Bouhedda")

st.write("A python-based program that returns a color palette from an image using clustering algorithms.")

uploaded_file = st.file_uploader(label="Upload an image", type=["jpg", "jpeg", "png"], accept_multiple_files=False)
if uploaded_file:
    st.image(uploaded_file)

num_colors_choice = st.slider(label="Number of output colors", min_value=5, max_value=20, value=8)

col1, col2 = st.columns(2)

with col1:
    color_space_choice = st.radio(label="Color space", options=["rgb", "hsv"], index=0)

with col2:
    model_choice = st.radio(label="Clustering model", options=["kmeans", "gmm"], index=0)

if st.button(label="Generate palette"):
    if uploaded_file is not None:
        try:
            with st.spinner("Generating color palette..."):
                results = get_palette(uploaded_file, num_colors=num_colors_choice, color_space=color_space_choice, model=model_choice)
                st.title("Palette")
                st.write("Click on any color to open it on ColorHexa.com")
                cols = st.columns(num_colors_choice)

                for i, color in enumerate(results):
                    color_tuple = tuple(color)
                    hex_color = '#%02x%02x%02x' % color_tuple
                    hex_code_url = '%02x%02x%02x' % color_tuple
                    target_url = f"https://www.colorhexa.com/{hex_code_url}"
                    color_box_html = f"""
                                        <a href="{target_url}" target="_blank" style="text-decoration: none;">
                                            <div style="
                                                background-color: {hex_color}; 
                                                border-radius: 5px;
                                                height: 80px; 
                                                width: 100%;
                                                margin: 5px 0;
                                                box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
                                                cursor: pointer; /* Change mouse cursor to indicate clickability */
                                            "></div>
                                            <p style="text-align: center; font-size: 14px; margin-top: 5px; margin-bottom: 20px;">
                                                <span style='font-weight: bold;'>{hex_color}</span><br>
                                                RGB: {color}
                                            </p>
                                        </a>
                                    """
                    with cols[i]:
                        st.markdown(color_box_html, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"An error occurred during palette gneration: {e}")
    else:
        st.warning("Please upload an image first!")