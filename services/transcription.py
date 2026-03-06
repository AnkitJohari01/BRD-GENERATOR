import whisper
import tempfile
import os

# Load whisper model once
model = whisper.load_model("base")

def transcribe_audio(file):

    # Get original extension
    file_extension = os.path.splitext(file.name)[1]

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_audio:
        temp_audio.write(file.read())
        temp_path = temp_audio.name

    # Transcribe audio/video
    result = model.transcribe(temp_path)

    return result["text"]
