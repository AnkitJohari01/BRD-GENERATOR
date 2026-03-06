import os
os.environ["PATH"] += r";C:\Program Files\Pandoc"
import streamlit as st
import requests
import pypandoc
from io import BytesIO
import tempfile
import pypandoc

API_URL = "http://127.0.0.1:8000/generate-brd/"

st.set_page_config(page_title="BRD Generator AI", layout="wide")

st.title("BRD Generator AI")
st.write("Upload meeting recordings or requirement documents to generate a BRD.")

uploaded_files = st.file_uploader(
    "Upload files",
    type=["pdf", "docx", "txt", "mp3", "wav", "mp4"],
    accept_multiple_files=True
)

if uploaded_files:
    st.subheader("Uploaded Files")
    for file in uploaded_files:
        st.write(f"• {file.name}")

if st.button("Generate BRD"):

    if not uploaded_files:
        st.warning("Please upload at least one file.")
        st.stop()

    files = []

    for file in uploaded_files:
        files.append(
            ("files", (file.name, file.getvalue(), file.type))
        )

    with st.spinner("Processing files and generating BRD..."):

        try:
            response = requests.post(API_URL, files=files)

            if response.status_code != 200:
                st.error(f"API Error: {response.text}")
                st.stop()

            data = response.json()

            if data.get("status") == "success":

                brd_text = data.get("brd")

                st.success(data.get("message"))

                st.subheader("Generated BRD")

                st.text_area(
                    "BRD Output",
                    value=brd_text,
                    height=500
                )

                # -------- Convert Markdown → Word --------
                with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmpfile:
                    output_path = tmpfile.name

                pypandoc.convert_text(
                    brd_text,
                    'docx',
                    format='md',
                    outputfile=output_path
                )

                with open(output_path, "rb") as f:
                    doc_bytes = f.read()

                # -------- Download Button --------
                st.download_button(
                    label="Download BRD as Word Document",
                    data=doc_bytes,
                    file_name="Generated_BRD.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            else:
                st.error(data.get("error", "Unknown error occurred"))

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI server. Make sure it is running.")

        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
