from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, MODEL_NAME

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model=MODEL_NAME,
    temperature=0.2
)


def generate_brd(validated_data):

    prompt = f"""
You are a Senior Business Analyst and Enterprise Documentation Specialist.

Your task is to generate a professional Business Requirements Document (BRD)
based on the validated project information provided.

Follow these instructions carefully:

1. Use clear, structured, and professional business language.
2. Follow the section headings EXACTLY as provided.
3. Expand each section with detailed and relevant content.
4. Ensure the document is suitable for stakeholders, project managers, and technical teams.
5. If specific information is missing, make reasonable professional assumptions.
6. Maintain logical flow from business context to technical requirements.

The BRD must contain the following sections in the same order.

BRD Structure:

1. Executive Summary
2. Business Problem / Current Pain Points
3. Business Objectives & Expected Outcomes
4. Solution Overview
5. Project Scope
   - In Scope
   - Out of Scope
6. Stakeholders
7. Functional Requirements
8. Non-Functional Requirements
9. Data Requirements
10. System Architecture Overview
11. Assumptions
12. Constraints
13. Implementation Roadmap / Project Timeline
14. Success Metrics & Acceptance Criteria
15. Glossary

Formatting Requirements:

- Use clear headings for each section.
- Use bullet points where appropriate.
- Ensure requirements are concise and structured.
- Functional requirements should be written as clear system capabilities.
- Non-functional requirements should cover performance, security, scalability, reliability, and usability.

Project Information:
{validated_data}

Generate the complete Business Requirements Document.
"""

    response = llm.invoke(prompt)

    return response.content
