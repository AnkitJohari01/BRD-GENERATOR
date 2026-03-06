# import os
# os.environ["PATH"] += r";C:\Program Files\Pandoc"
# import streamlit as st
# import requests
# import pypandoc
# from io import BytesIO
# import tempfile
# import pypandoc

# API_URL = "http://127.0.0.1:8000/generate-brd/"

# st.set_page_config(page_title="BRD Generator AI", layout="wide")

# st.title("BRD Generator AI")
# st.write("Upload meeting recordings or requirement documents to generate a BRD.")

# uploaded_files = st.file_uploader(
#     "Upload files",
#     type=["pdf", "docx", "txt", "mp3", "wav", "mp4"],
#     accept_multiple_files=True
# )

# if uploaded_files:
#     st.subheader("Uploaded Files")
#     for file in uploaded_files:
#         st.write(f"• {file.name}")

# if st.button("Generate BRD"):

#     if not uploaded_files:
#         st.warning("Please upload at least one file.")
#         st.stop()

#     files = []

#     for file in uploaded_files:
#         files.append(
#             ("files", (file.name, file.getvalue(), file.type))
#         )

#     with st.spinner("Processing files and generating BRD..."):

#         try:
#             response = requests.post(API_URL, files=files)

#             if response.status_code != 200:
#                 st.error(f"API Error: {response.text}")
#                 st.stop()

#             data = response.json()

#             if data.get("status") == "success":

#                 brd_text = data.get("brd")

#                 st.success(data.get("message"))

#                 st.subheader("Generated BRD")

#                 st.text_area(
#                     "BRD Output",
#                     value=brd_text,
#                     height=500
#                 )

#                 # -------- Convert Markdown → Word --------
#                 with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmpfile:
#                     output_path = tmpfile.name

#                 pypandoc.convert_text(
#                     brd_text,
#                     'docx',
#                     format='md',
#                     outputfile=output_path
#                 )

#                 with open(output_path, "rb") as f:
#                     doc_bytes = f.read()

#                 # -------- Download Button --------
#                 st.download_button(
#                     label="Download BRD as Word Document",
#                     data=doc_bytes,
#                     file_name="Generated_BRD.docx",
#                     mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
#                 )

#             else:
#                 st.error(data.get("error", "Unknown error occurred"))

#         except requests.exceptions.ConnectionError:
#             st.error("Could not connect to FastAPI server. Make sure it is running.")

#         except Exception as e:
#             st.error(f"Unexpected error: {str(e)}")









import streamlit as st
import pypandoc
import tempfile
from io import BytesIO

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import your internal logic
from services.document_loader import load_document
from services.transcription import transcribe_audio
from agents.brd_writer_agent import generate_brd

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="BRD Generator AI", layout="wide")

st.title("BRD Generator AI")
st.write("Upload meeting recordings or requirement documents to generate a BRD.")

# ---------- FILE UPLOAD ----------
uploaded_files = st.file_uploader(
    "Upload files",
    type=["pdf", "docx", "txt", "mp3", "wav", "mp4"],
    accept_multiple_files=True
)

# ---------- SHOW FILES ----------
if uploaded_files:
    st.subheader("Uploaded Files")

    for file in uploaded_files:
        st.write(f"• {file.name}")

# ---------- GENERATE BRD ----------
if st.button("Generate BRD"):

    if not uploaded_files:
        st.warning("Please upload at least one file.")
        st.stop()

    extracted_text = ""

    with st.spinner("Processing files..."):

        for file in uploaded_files:

            file_ext = file.name.split(".")[-1].lower()

            # ----- Document files -----
            if file_ext in ["pdf", "docx", "txt"]:
                text = load_document(file)
                extracted_text += "\n" + text

            # ----- Audio / Video files -----
            elif file_ext in ["mp3", "wav", "mp4"]:
                text = transcribe_audio(file)
                extracted_text += "\n" + text

    if not extracted_text:
        st.error("Could not extract text from files.")
        st.stop()

    # ---------- GENERATE BRD ----------
    with st.spinner("Generating BRD using AI..."):

        brd_text = generate_brd(extracted_text)

    st.success("BRD generated successfully!")

    # ---------- SHOW OUTPUT ----------
    st.subheader("Generated BRD")

    st.text_area(
        "BRD Output",
        value=brd_text,
        height=500
    )

    # ---------- INSTALL PANDOC ----------
    try:
        pypandoc.get_pandoc_version()
    except:
        pypandoc.download_pandoc()

    # ---------- CONVERT TO WORD ----------
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmpfile:
        output_path = tmpfile.name

    pypandoc.convert_text(
        brd_text,
        "docx",
        format="md",
        outputfile=output_path
    )

    with open(output_path, "rb") as f:
        doc_bytes = f.read()

    # ---------- DOWNLOAD ----------
    st.download_button(
        label="Download BRD as Word Document",
        data=doc_bytes,
        file_name="Generated_BRD.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )












