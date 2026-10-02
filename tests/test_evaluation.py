from src.ingestion.pdf_loader import extract_text_from_pdf
from src.preprocessing.chunker import create_chunks
from src.retrieval.retriever import Retriever


# ============================================================
# Evaluation Configuration
# ============================================================

PDF_PATH = "data/research_paper.pdf"

TOP_K = 5


# ============================================================
# Evaluation Questions
# ============================================================

evaluation_questions = [
    {
        "question": "What factors influence successful stem cell differentiation?",
        "expected_keywords": [
            "differentiation",
            "gene-expression",
            "biomarkers"
        ]
    },
    {
        "question": "Why are gene-expression biomarkers important?",
        "expected_keywords": [
            "gene-expression",
            "biomarkers",
            "molecular state"
        ]
    },
    {
        "question": "How are biomarkers used to predict differentiation success?",
        "expected_keywords": [
            "prediction",
            "biomarkers",
            "differentiation"
        ]
    },
    {
        "question": "What is the role of machine learning in the study?",
        "expected_keywords": [
            "machine learning",
            "prediction",
            "classification"
        ]
    },
    {
        "question": "How is model interpretability achieved?",
        "expected_keywords": [
            "SHAP",
            "interpretability"
        ]
    }
]


# ============================================================
# Load and Prepare Document
# ============================================================

print("\n========================================")
print("DOCUMIND AI — RAG EVALUATION")
print("========================================")


pages = extract_text_from_pdf(
    PDF_PATH
)


chunks = create_chunks(
    pages
)


print(f"\nPages loaded : {len(pages)}")
print(f"Chunks created: {len(chunks)}")


# ============================================================
# Build Retriever
# ============================================================

print("\nBuilding retrieval index...")

retriever = Retriever(
    chunks
)


print("Retrieval index ready.")


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

    expected_keywords = [
        keyword.lower()
        for keyword in test_case["expected_keywords"]
    ]


    print("\n----------------------------------------")

    print(
        f"Test {number}/{total}"
    )

    print(
        f"Question: {question}"
    )


    # Retrieve relevant chunks

    results = retriever.retrieve(
        question,
        top_k=TOP_K
    )


    # Combine retrieved text

    retrieved_text = " ".join(
        result["document"]["text"]
        for result in results
    ).lower()


    # Check expected keywords

    matched_keywords = [
        keyword
        for keyword in expected_keywords
        if keyword in retrieved_text
    ]


    # At least half of the expected keywords
    # should appear in the retrieved passages.

    required_matches = max(
        1,
        len(expected_keywords) // 2
    )


    test_passed = (
        len(matched_keywords)
        >= required_matches
    )


    if test_passed:

        passed += 1

        print("Result : PASS")

    else:

        print("Result : FAIL")


    print(
        f"Matched keywords: "
        f"{matched_keywords}"
    )


    # Display retrieved pages

    pages_found = sorted(
        set(
            result["document"]["page"]
            for result in results
        )
    )


    print(
        f"Retrieved pages: {pages_found}"
    )


# ============================================================
# Evaluation Summary
# ============================================================

accuracy = (
    passed / total
) * 100


print("\n========================================")
print("EVALUATION SUMMARY")
print("========================================")


print(
    f"Tests passed : {passed}/{total}"
)


print(
    f"Retrieval hit rate: {accuracy:.1f}%"
)


if accuracy >= 80:

    print(
        "Status: GOOD — retrieval is working well."
    )

elif accuracy >= 60:

    print(
        "Status: MODERATE — retrieval can be improved."
    )

else:

    print(
        "Status: NEEDS IMPROVEMENT — review retrieval."
    )


print("========================================")