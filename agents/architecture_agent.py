from langchain_openai import ChatOpenAI
from backend.config import OPENAI_API_KEY, MODEL_NAME


# Initialize LLM
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model=MODEL_NAME,
    temperature=0.1
)


def generate_architecture_diagrams(brd_text: str) -> dict:
    """
    Generates three architecture diagrams from the BRD:
    1. System Architecture
    2. Component Diagram
    3. Data Flow Diagram

    Returns a dictionary containing Mermaid diagrams.
    """

    prompt = f"""
You are a Senior Solution Architect.

Your task is to analyze a Business Requirement Document (BRD)
and generate THREE simple architecture diagrams.

The diagrams must be easy for both technical and non-technical
stakeholders to understand.

IMPORTANT RULES

1. Keep diagrams simple and minimal
   - Maximum 6 components per diagram.

2. Use descriptive component names only.
   Do NOT use abbreviations like:
   AI, AJ, DI, MA, VAMS, etc.

3. If the BRD lacks technical detail,
   use generic components such as:

   Web User Interface
   Application Server
   Processing Service
   External Service
   Output Document

4. All diagrams must follow top-to-bottom flow.

5. Avoid:
   - circular dependencies
   - excessive arrows
   - complex branching

6. Return ONLY Mermaid diagrams.

OUTPUT FORMAT

SYSTEM_ARCHITECTURE
flowchart TD
User --> Web_User_Interface
Web_User_Interface --> Application_Server
Application_Server --> Processing_Service
Processing_Service --> Report_Service
Report_Service --> Output_Document


COMPONENT_DIAGRAM
flowchart TD
User_Interface --> File_Upload_Module
File_Upload_Module --> Document_Processor
File_Upload_Module --> Audio_Transcription_Module
Document_Processor --> BRD_Generation_Module
Audio_Transcription_Module --> BRD_Generation_Module
BRD_Generation_Module --> Architecture_Diagram_Module


DATA_FLOW_DIAGRAM
flowchart TD
User_Input --> File_Upload_Service
File_Upload_Service --> Text_Extraction
Text_Extraction --> BRD_Generator
BRD_Generator --> Architecture_Diagram_Generator
Architecture_Diagram_Generator --> Final_Output


BRD:
{brd_text}
"""

    response = llm.invoke(prompt)
    content = response.content.strip()

    # Remove markdown code blocks if returned
    content = content.replace("```mermaid", "").replace("```", "").strip()

    diagrams = {
        "system_architecture": "",
        "component_diagram": "",
        "data_flow_diagram": ""
    }

    current = None
    buffer = []

    for line in content.splitlines():
        line = line.strip()

        if line == "SYSTEM_ARCHITECTURE":
            if current:
                diagrams[current] = "\n".join(buffer).strip()
            current = "system_architecture"
            buffer = []
            continue

        elif line == "COMPONENT_DIAGRAM":
            if current:
                diagrams[current] = "\n".join(buffer).strip()
            current = "component_diagram"
            buffer = []
            continue

        elif line == "DATA_FLOW_DIAGRAM":
            if current:
                diagrams[current] = "\n".join(buffer).strip()
            current = "data_flow_diagram"
            buffer = []
            continue

        if current:
            buffer.append(line)

    if current:
        diagrams[current] = "\n".join(buffer).strip()

    # Ensure Mermaid header exists
    for key in diagrams:
        if diagrams[key] and not diagrams[key].startswith("flowchart"):
            diagrams[key] = "flowchart TD\n" + diagrams[key]

    return diagrams