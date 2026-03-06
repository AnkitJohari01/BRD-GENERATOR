import whisper

model = whisper.load_model("base")

def transcribe_audio(file):

    with open("temp_audio", "wb") as f:
        f.write(file.file.read())

    result = model.transcribe("temp_audio")

    return result["text"]