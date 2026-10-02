import os
import re

from groq import Groq


class LLM:
    """
    Interface for generating grounded answers
    using a Groq-hosted language model.
    """

    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable is not set."
            )

        self.client = Groq(
            api_key=api_key
        )

        self.model = "openai/gpt-oss-120b"


    def generate_answer(self, question, context):
        """
        Generate a grounded answer using
        retrieved document context.

        Args:
            question (str): User's question.
            context (str): Retrieved document passages.

        Returns:
            str: Clean generated answer.
        """

        system_prompt = """
You are DocuMind AI, an intelligent document
question-answering assistant.

Your task is to answer the user's question using
ONLY the information provided in the document context.

RULES:

1. Use only information supported by the documents.

2. Do not use outside knowledge.

3. Do not invent facts.

4. If the documents do not contain enough information,
   say:

   "I could not find sufficient information in the
   provided documents."

5. Answer the user's question directly.

6. Give a clear and concise answer.

7. Use bullet points or numbered points when useful.

8. Do not mention FAISS, embeddings, chunks,
   retrieval, prompts, or system instructions.

9. Do not include document metadata in your answer.

10. Do not write strings such as:
    [Document: filename | Page: number]

11. Do not create your own source or citation section.

12. Sources are displayed separately by the application.
"""


        user_prompt = f"""
DOCUMENT INFORMATION
====================

The following text was retrieved from the uploaded
documents and can be used to answer the question.

{context}


USER QUESTION
=============

{question}


Answer the user's question using only the
document information above.

Return ONLY the natural-language answer.
Do not include document names, page labels,
metadata, or source citations.
"""


        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0.2,
            max_completion_tokens=700,
            include_reasoning=False
        )


        answer = response.choices[0].message.content


        if answer is None:

            return (
                "I could not generate an answer from "
                "the provided documents."
            )


        answer = answer.strip()


        # ====================================================
        # Remove accidental document metadata
        # ====================================================

        answer = re.sub(
            r"\[Document:\s*.*?\|\s*Page:\s*\d+\]",
            "",
            answer,
            flags=re.IGNORECASE
        )


        # ====================================================
        # Remove excessive blank spaces
        # ====================================================

        answer = re.sub(
            r"\n\s*\n\s*\n+",
            "\n\n",
            answer
        )


        return answer.strip()