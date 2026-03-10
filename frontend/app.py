import streamlit as st
import pypandoc
from graphviz import Digraph


from backend.agents.architecture_agent import generate_architecture_diagrams

import tempfile

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Debug: check if API key loaded
st.write("API Loaded:", "OPENAI_API_KEY" in st.secrets)

# Fix import path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import internal modules
from services.document_loader import load_document
from services.transcription import transcribe_audio
from agents.brd_writer_agent import generate_brd


# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="BRD Generator AI", layout="wide")

st.title("BRD Generator AI")
st.write("Upload requirement documents or recordings to generate a BRD and architecture diagrams.")


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


# ---------------- SAFE GRAPHVIZ RENDER ----------------

def render_graphviz(mermaid_code):
    
    if not mermaid_code:
        return None

    try:

        nodes = set()
        edges = []

        lines = mermaid_code.split("\n")

        for line in lines:

            line = line.strip()

            if "-->" in line:

                parts = line.split("-->")

                if len(parts) != 2:
                    continue

                src = parts[0].strip().replace(" ", "_")
                dst = parts[1].strip().replace(" ", "_")

                nodes.add(src)
                nodes.add(dst)

                edges.append((src, dst))

        node_count = len(nodes)

        dot = Digraph(format="png")

        # Dynamic layout
        if node_count > 5:
            dot.attr(rankdir="LR")
            dot.attr(size="16,9!")
        else:
            dot.attr(rankdir="TB")
            dot.attr(size="9,16!")

        dot.attr(dpi="600")

        dot.attr(
            "node",
            shape="box",
            style="rounded,filled",
            color="#2c3e50",
            fillcolor="#ecf0f1",
            fontname="Helvetica",
            fontsize="16",
            width="2.5",
            height="1",
            fixedsize="false"
        )

        if not nodes:
            nodes.add("Architecture")

        for node in nodes:

            label = node.replace("_", " ")

            words = label.split()

            wrapped = "\n".join(
                [" ".join(words[i:i+2]) for i in range(0, len(words), 2)]
            )

            dot.node(node, label=wrapped)

        for src, dst in edges:
            dot.edge(src, dst)

        with tempfile.TemporaryDirectory() as tmpdir:

            file_path = os.path.join(tmpdir, "diagram")

            dot.render(file_path, format="png", cleanup=True)

            with open(file_path + ".png", "rb") as f:
                img_bytes = f.read()

        return img_bytes

    except Exception as e:

        st.error(f"Diagram generation error: {e}")

        return None


# ---------------- GENERATE BRD ----------------
if st.button("Generate BRD"):

    if not uploaded_files:
        st.warning("Please upload at least one file.")
        st.stop()

    extracted_text = ""
    for file in uploaded_files:
        files.append(("files", (file.name, file.getvalue(), file.type)))

    with st.spinner("Processing files..."):
        for file in uploaded_files:

            try:

                file_ext = file.name.split(".")[-1].lower()

                # Reset pointer (important for Streamlit uploads)
                file.seek(0)

                # ----- Document files -----
                if file_ext in ["pdf", "docx", "txt"]:

                    text = load_document(file)

                    if text:
                        extracted_text += "\n" + text


                # ----- Audio / Video files -----
                elif file_ext in ["mp3", "wav", "mp4"]:

                    text = transcribe_audio(file)

                    if text:
                        extracted_text += "\n" + text


                else:
                    st.warning(f"Unsupported file type: {file.name}")

            except Exception as e:
                st.error(f"Error processing {file.name}: {str(e)}")


    if not extracted_text.strip():
        st.error("Could not extract text from the uploaded files.")
        st.stop()


    # ---------- GENERATE BRD ----------
    with st.spinner("Generating BRD using AI..."):

        try:

            response = requests.post(API_URL, files=files)

            if response.status_code != 200:
                st.error(f"API Error: {response.text}")
                st.stop()

            data = response.json()

            if not isinstance(data, dict):
                st.error("Invalid API response format.")
                st.stop()

            if data.get("status") != "success":
                st.error(data.get("error", "Unknown error occurred"))
                st.stop()

            brd_text = data.get("brd", "")

            if not brd_text:
                st.error("BRD generation failed.")
                st.stop()

            st.success(data.get("message", "BRD generated successfully."))

            # ---------------- BRD DISPLAY ----------------

            st.subheader("Generated BRD")

            st.text_area(
                "BRD Output",
                value=brd_text,
                height=500
            )

            # ---------------- DIAGRAM GENERATION ----------------

            with st.spinner("Generating Architecture Diagrams..."):

                diagrams = {}

                try:
                    diagrams = generate_architecture_diagrams(brd_text)
                except Exception as e:
                    st.warning(f"Diagram generation failed: {e}")

            tab1, tab2, tab3 = st.tabs([
                "System Architecture",
                "Component Diagram",
                "Data Flow Diagram"
            ])

            diagram_map = [
                ("system_architecture", "System Architecture", tab1),
                ("component_diagram", "Component Diagram", tab2),
                ("data_flow_diagram", "Data Flow Diagram", tab3),
            ]

            for key, title, tab in diagram_map:

                with tab:

                    diagram_code = diagrams.get(key, "")

                    img = render_graphviz(diagram_code)

                    if img:

                        st.image(img)

                        st.download_button(
                            f"Download {title}",
                            img,
                            f"{key}.png",
                            "image/png"
                        )

                    else:
                        st.info(f"{title} diagram not available.")

            # ---------------- WORD EXPORT ----------------

            try:

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

                st.download_button(
                    "Download BRD as Word Document",
                    doc_bytes,
                    "Generated_BRD.docx",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            except Exception as e:
                st.warning(f"Word export failed: {e}")

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI server. Please start the backend.")

            brd_text = generate_brd(extracted_text)
        except Exception as e:
            st.error(f"BRD generation failed: {str(e)}")
            st.stop()


    st.success("BRD generated successfully!")


    # ---------- SHOW OUTPUT ----------
    st.subheader("Generated BRD")

    st.text_area(
        "BRD Output",
        value=brd_text,
        height=500
    )


    # ---------- ENSURE PANDOC ----------
    try:
        pypandoc.get_pandoc_version()
    except OSError:
        with st.spinner("Installing Pandoc..."):
            pypandoc.download_pandoc()


    # ---------- CONVERT TO WORD ----------
    try:

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

        os.remove(output_path)

    except Exception as e:
        st.error(f"Word conversion failed: {str(e)}")
        st.stop()


    # ---------- DOWNLOAD ----------
    st.download_button(
        label="Download BRD as Word Document",
        data=doc_bytes,
        file_name="Generated_BRD.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )












