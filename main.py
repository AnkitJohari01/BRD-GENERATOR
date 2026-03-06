# from fastapi import FastAPI, UploadFile, File
# from services.document_loader import load_document
# from services.transcription import transcribe_audio
# from services.rag_pipeline import process_text

# app = FastAPI(title="BRD Generator AI")

# @app.post("/generate-brd/")
# async def generate_brd(file: UploadFile = File(...)):

#     file_type = file.filename.split(".")[-1]

#     if file_type in ["pdf", "docx", "txt"]:
#         text = load_document(file)

#     elif file_type in ["mp3", "wav", "mp4"]:
#         text = transcribe_audio(file)

#     else:
#         return {"error": "Unsupported file type"}

#     brd = process_text(text)

#     return {"brd": brd}


































from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List, Annotated
import logging

from services.document_loader import load_document
from services.transcription import transcribe_audio
from services.rag_pipeline import process_text

app = FastAPI(title="BRD Generator AI")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Supported formats
SUPPORTED_DOCS = {"pdf", "docx", "txt"}
SUPPORTED_MEDIA = {"mp3", "wav", "mp4"}


@app.get("/")
def root():
    return {"message": "BRD Generator AI API is running"}


@app.post("/generate-brd/")
async def generate_brd(
    files: Annotated[List[UploadFile], File(description="Upload multiple files")]
):

    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    combined_text = []

    for file in files:

        try:
            if not file.filename:
                logger.warning("File with empty filename skipped")
                continue

            file_extension = file.filename.split(".")[-1].lower()

            logger.info(f"Processing file: {file.filename}")

            # Document processing
            if file_extension in SUPPORTED_DOCS:
                text = load_document(file)

            # Audio / Video transcription
            elif file_extension in SUPPORTED_MEDIA:
                text = transcribe_audio(file)

            else:
                logger.warning(f"Unsupported file skipped: {file.filename}")
                continue

            if text and text.strip():
                combined_text.append(text)
            else:
                logger.warning(f"No text extracted from {file.filename}")

        except Exception as e:
            logger.error(f"Error processing {file.filename}: {str(e)}")
            continue

    # If nothing processed
    if not combined_text:
        return {
            "status": "failed",
            "error": "No valid files were processed"
        }

    try:
        final_text = "\n\n".join(combined_text)

        logger.info("Generating BRD from extracted content")

        brd = process_text(final_text)

        return {
            "status": "success",
            "message": "BRD generated successfully",
            "brd": brd
        }

    except Exception as e:
        logger.error(f"BRD generation failed: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="BRD generation failed"
        )