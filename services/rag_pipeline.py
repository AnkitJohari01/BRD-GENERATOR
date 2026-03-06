from agents.extractor_agent import extract_requirements
from agents.validator_agent import validate_requirements
from agents.brd_writer_agent import generate_brd

def process_text(text):

    extracted = extract_requirements(text)

    validated = validate_requirements(extracted)

    brd = generate_brd(validated)

    return brd