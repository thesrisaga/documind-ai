from src.ingestion.pdf_loader import extract_text_from_pdf
from src.preprocessing.chunker import create_chunks
from src.retrieval.retriever import Retriever
from src.generation.llm import LLM


# ============================================================
# Configuration
# ============================================================

PDF_PATH = "data/research_paper.pdf"

TOP_K = 5


# ============================================================
# Evaluation Questions
# ============================================================

evaluation_questions = [
    {
        "question": "What factors influence successful stem cell differentiation?",
        "expected_concepts": [
            "differentiation",
            "gene expression",
            "biomarkers"
        ]
    },
    {
        "question": "Why are gene-expression biomarkers important?",
        "expected_concepts": [
            "molecular state",
            "biomarkers",
            "differentiation"
        ]
    },
    {
        "question": "How are biomarkers used to predict differentiation success?",
        "expected_concepts": [
            "prediction",
            "biomarkers",
            "differentiation"
        ]
    },
    {
        "question": "What is the role of machine learning in the study?",
        "expected_concepts": [
            "machine learning",
            "prediction",
            "classification"
        ]
    },
    {
        "question": "How is model interpretability achieved?",
        "expected_concepts": [
            "SHAP",
            "interpretability"
        ]
    }
]


# ============================================================
# Load Document
# ============================================================

print("\n========================================")
print("DOCUMIND AI — ANSWER EVALUATION")
print("========================================")


pages = extract_text_from_pdf(
    PDF_PATH
)


chunks = create_chunks(
    pages
)


print(
    f"\nPages loaded  : {len(pages)}"
)

print(
    f"Chunks created: {len(chunks)}"
)


# ============================================================
# Build Retriever
# ============================================================

print("\nBuilding retrieval index...")

retriever = Retriever(
    chunks
)


print("Retrieval index ready.")


# ============================================================
# Load LLM
# ============================================================

print("\nLoading LLM...")

llm = LLM()

print("LLM ready.")


# ============================================================
# Run Evaluation
# ============================================================

passed = 0

total = len(
    evaluation_questions
)


for number, test_case in enumerate(
    evaluation_questions,
    start=1
):

    question = test_case["question"]

    expected_concepts = [
        concept.lower()
        for concept in test_case["expected_concepts"]
    ]


    print("\n----------------------------------------")

    print(
        f"Test {number}/{total}"
    )

    print(
        f"Question: {question}"
    )


    # --------------------------------------------------------
    # Retrieve context
    # --------------------------------------------------------

    results = retriever.retrieve(
        question,
        top_k=TOP_K
    )


    context_parts = []


    for result in results:

        document = result["document"]

        context_parts.append(
            document["text"]
        )


    context = "\n\n".join(
        context_parts
    )


    # --------------------------------------------------------
    # Generate answer
    # --------------------------------------------------------

    answer = llm.generate_answer(
        question,
        context
    )


    answer_lower = answer.lower()


    # --------------------------------------------------------
    # Check expected concepts
    # --------------------------------------------------------

    matched_concepts = []

    for concept in expected_concepts:

        if concept in answer_lower:

            matched_concepts.append(
                concept
            )


    # --------------------------------------------------------
    # Determine result
    # --------------------------------------------------------

    required_matches = max(
        1,
        len(expected_concepts) // 2
    )


    test_passed = (
        len(matched_concepts)
        >= required_matches
    )


    if test_passed:

        passed += 1

        print(
            "Result : PASS"
        )

    else:

        print(
            "Result : FAIL"
        )


    # --------------------------------------------------------
    # Display evaluation details
    # --------------------------------------------------------

    print(
        f"Matched concepts: "
        f"{matched_concepts}"
    )


    print(
        "\nGenerated answer:"
    )

    print(
        answer
    )


# ============================================================
# Evaluation Summary
# ============================================================

accuracy = (
    passed / total
) * 100


print("\n========================================")
print("ANSWER EVALUATION SUMMARY")
print("========================================")


print(
    f"Tests passed : {passed}/{total}"
)


print(
    f"Grounded answer score: {accuracy:.1f}%"
)


if accuracy >= 80:

    print(
        "Status: GOOD — generated answers "
        "contain the expected concepts."
    )

elif accuracy >= 60:

    print(
        "Status: MODERATE — some answers "
        "may need improvement."
    )

else:

    print(
        "Status: NEEDS IMPROVEMENT — "
        "review the generation pipeline."
    )


print("========================================")