from app.agents.intake_agent import IntakeAgent
from app.agents.retrieval_agent import RetrievalAgent


def test_retrieval_finds_cooling_manual():
    text = "Vehicle overheating with coolant leak and high temperature."
    intake = IntakeAgent().run(case_text=text, source_file="test.txt")

    retrieval = RetrievalAgent().run(intake=intake)

    document_names = [
        document.document_name
        for document in retrieval.retrieved_documents
    ]

    assert "cooling_system_manual.txt" in document_names