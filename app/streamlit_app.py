import sys
from pathlib import Path

import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# PROJECT IMPORTS
# ============================================================

from src.ingestion.pdf_loader import extract_text_from_pdf
from src.preprocessing.chunker import create_chunks
from src.retrieval.retriever import Retriever
from src.generation.llm import LLM


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

/* ==========================================================
   GLOBAL PAGE
   ========================================================== */

html,
body,
.stApp {

    background: #212121 !important;

    color: #ffffff !important;

    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Arial,
        sans-serif !important;
}


/* ==========================================================
   REMOVE STREAMLIT DEFAULT ELEMENTS
   ========================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: #212121 !important;
}


/* ==========================================================
   MAIN CONTENT
   ========================================================== */

.block-container {

    max-width: 1180px !important;

    padding-top: 65px !important;

    padding-bottom: 30px !important;

    padding-left: 45px !important;

    padding-right: 45px !important;

}


/* ==========================================================
   SIDEBAR
   ========================================================== */

section[data-testid="stSidebar"] {

    background: #171717 !important;

    border-right: 1px solid #333333 !important;

    min-width: 290px !important;

    max-width: 290px !important;

}


section[data-testid="stSidebar"] > div {

    background: #171717 !important;

    padding-top: 20px !important;

    padding-bottom: 15px !important;

}


section[data-testid="stSidebar"] * {

    color: #ffffff !important;

}


/* ==========================================================
   SIDEBAR BRAND
   ========================================================== */

.sidebar-brand {

    font-size: 20px;

    font-weight: 600;

    color: #ffffff;

    margin-bottom: 18px;

}


/* ==========================================================
   SIDEBAR SECTION HEADINGS
   ========================================================== */

.sidebar-section {

    color: #b0b0b0 !important;

    font-size: 12px !important;

    font-weight: 600 !important;

    letter-spacing: 0.08em;

    text-transform: uppercase;

    margin-top: 15px;

    margin-bottom: 7px;

}


/* ==========================================================
   SIDEBAR DESCRIPTION
   ========================================================== */

.sidebar-text {

    color: #d0d0d0 !important;

    font-size: 14px !important;

    line-height: 1.5 !important;

    margin-bottom: 5px;

}


/* ==========================================================
   SIDEBAR BUTTONS
   ========================================================== */

section[data-testid="stSidebar"] .stButton {

    margin-bottom: 3px !important;

}


section[data-testid="stSidebar"] .stButton button {

    background: #171717 !important;

    color: #ffffff !important;

    border: 1px solid #444444 !important;

    border-radius: 7px !important;

    min-height: 38px !important;

    height: 38px !important;

    font-size: 14px !important;

    font-weight: 400 !important;

}


section[data-testid="stSidebar"] .stButton button:hover {

    background: #292929 !important;

    border-color: #666666 !important;

}


/* ==========================================================
   FILE UPLOADER
   ========================================================== */

section[data-testid="stSidebar"]
[data-testid="stFileUploader"] {

    background: #212121 !important;

    border: 1px solid #444444 !important;

    border-radius: 8px !important;

    padding: 7px !important;

}


section[data-testid="stSidebar"]
[data-testid="stFileUploaderDropzone"] {

    background: #212121 !important;

    border: none !important;

    min-height: 82px !important;

}


section[data-testid="stSidebar"]
[data-testid="stFileUploaderDropzone"] * {

    color: #ffffff !important;

    font-size: 13px !important;

}


/* ==========================================================
   UPLOADED FILE NAME
   ========================================================== */

.uploaded-file {

    background: #212121;

    border: 1px solid #3d3d3d;

    border-radius: 6px;

    color: #ffffff;

    padding: 7px 9px;

    margin-top: 5px;

    font-size: 13px;

    overflow: hidden;

    text-overflow: ellipsis;

    white-space: nowrap;

}


/* ==========================================================
   MAIN TITLE
   ========================================================== */

.main-title {

    color: #ffffff;

    text-align: center;

    font-size: 30px;

    font-weight: 600;

    line-height: 1.4;

    margin-top: 5px;

    margin-bottom: 8px;

    padding-top: 5px;

    padding-bottom: 5px;

}


/* ==========================================================
   DOCUMENT INFORMATION
   ========================================================== */

.document-info {

    color: #a5a5a5;

    text-align: center;

    font-size: 14px;

    line-height: 1.5;

    margin-top: 5px;

    margin-bottom: 15px;

}


/* ==========================================================
   WELCOME SCREEN
   ========================================================== */

.welcome-area {

    text-align: center;

    margin-top: 90px;

    margin-bottom: 20px;

}


.welcome-title {

    color: #ffffff;

    font-size: 28px;

    font-weight: 500;

    line-height: 1.35;

    margin-bottom: 14px;

}


.welcome-text {

    color: #a5a5a5;

    font-size: 16px;

    line-height: 1.6;

}


/* ==========================================================
   CHAT MESSAGES
   ========================================================== */

[data-testid="stChatMessage"] {

    background: transparent !important;

    border: none !important;

    padding-top: 12px !important;

    padding-bottom: 12px !important;

}


/* ==========================================================
   CHAT MESSAGE TEXT
   ========================================================== */

[data-testid="stChatMessageContent"] {

    color: #ffffff !important;

    font-size: 17px !important;

    line-height: 1.65 !important;

}


[data-testid="stChatMessageContent"] p {

    color: #ffffff !important;

    font-size: 17px !important;

    line-height: 1.65 !important;

    margin-top: 0 !important;

    margin-bottom: 10px !important;

}


[data-testid="stChatMessageContent"] li {

    color: #ffffff !important;

    font-size: 17px !important;

    line-height: 1.65 !important;

    margin-bottom: 5px !important;

}


/* ==========================================================
   CHAT INPUT
   ========================================================== */

[data-testid="stChatInput"] {

    background: #212121 !important;

    border: none !important;

    padding-bottom: 15px !important;

}


[data-testid="stChatInput"] > div {

    background: #2f2f2f !important;

    border: 1px solid #505050 !important;

    border-radius: 16px !important;

    min-height: 58px !important;

    box-shadow: none !important;

}


[data-testid="stChatInput"] textarea {

    background: #2f2f2f !important;

    color: #ffffff !important;

    font-size: 17px !important;

    line-height: 1.5 !important;

    border: none !important;

    box-shadow: none !important;

}


[data-testid="stChatInput"] textarea::placeholder {

    color: #9a9a9a !important;

    font-size: 17px !important;

}


/* ==========================================================
   SOURCES
   ========================================================== */

.sources-title {

    color: #b5b5b5;

    font-size: 14px;

    font-weight: 600;

    margin-top: 15px;

    margin-bottom: 5px;

}


.source-item {

    color: #999999;

    font-size: 14px;

    line-height: 1.5;

    margin-bottom: 2px;

}


/* ==========================================================
   EXPANDER
   ========================================================== */

[data-testid="stExpander"] {

    background: #212121 !important;

    border: 1px solid #3d3d3d !important;

    border-radius: 7px !important;

}


[data-testid="stExpander"] * {

    color: #ffffff !important;

}


/* ==========================================================
   BOTTOM RAG PIPELINE
   ========================================================== */

.pipeline-bottom {

    width: 100%;

    text-align: center;

    margin-top: 115px;

    padding-top: 20px;

    padding-bottom: 12px;

    border-top: 1px solid #333333;

}


.pipeline-bottom-title {

    color: #a5a5a5;

    font-size: 12px;

    font-weight: 600;

    letter-spacing: 0.08em;

    margin-bottom: 7px;

}


.pipeline-flow {

    color: #b5b5b5;

    font-size: 14px;

    white-space: nowrap;

    line-height: 1.5;

}


/* ==========================================================
   FOOTER
   ========================================================== */

.footer-text {

    color: #707070;

    text-align: center;

    font-size: 12px;

    padding-top: 8px;

}


/* ==========================================================
   SCROLLBAR
   ========================================================== */

::-webkit-scrollbar {

    width: 7px;

}


::-webkit-scrollbar-track {

    background: #171717;

}


::-webkit-scrollbar-thumb {

    background: #444444;

    border-radius: 10px;

}


/* ==========================================================
   MOBILE / SMALL SCREEN
   ========================================================== */

@media (max-width: 900px) {

    .block-container {

        padding-left: 25px !important;

        padding-right: 25px !important;

        padding-top: 50px !important;

    }

    .main-title {

        font-size: 27px !important;

    }

    .welcome-area {

        margin-top: 70px;

        margin-bottom: 40px;

    }

    .welcome-title {

        font-size: 25px !important;

    }

    .welcome-text {

        font-size: 15px !important;

    }

    [data-testid="stChatMessageContent"] p,
    [data-testid="stChatMessageContent"] li {

        font-size: 16px !important;

    }

    .pipeline-bottom {

        margin-top: 70px;

    }

    .pipeline-flow {

        font-size: 12px;

    }

}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# BUILD RETRIEVER
# ============================================================

@st.cache_resource(show_spinner=False)
def build_retriever(file_data):

    all_chunks = []

    total_pages = 0

    for filename, pdf_bytes in file_data:

        safe_filename = Path(filename).name

        upload_directory = (
            PROJECT_ROOT / "data" / "uploads"
        )

        upload_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        pdf_path = (
            upload_directory / safe_filename
        )

        with open(
            pdf_path,
            "wb"
        ) as file:

            file.write(pdf_bytes)

        pages = extract_text_from_pdf(
            str(pdf_path)
        )

        if not pages:
            continue

        total_pages += len(pages)

        chunks = create_chunks(
            pages
        )

        for chunk in chunks:

            chunk["source"] = safe_filename

        all_chunks.extend(chunks)

    if not all_chunks:

        return None, 0, 0

    retriever = Retriever(
        all_chunks
    )

    return (
        retriever,
        total_pages,
        len(all_chunks)
    )


# ============================================================
# LOAD LLM
# ============================================================

@st.cache_resource(show_spinner=False)
def get_llm():

    return LLM()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-brand">DocuMind AI</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # NEW CHAT
    # --------------------------------------------------------

    if st.button(
        "＋ New chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


    # --------------------------------------------------------
    # DOCUMENTS
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-section">Documents</div>',
        unsafe_allow_html=True
    )


    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )


    if uploaded_files:

        for uploaded_file in uploaded_files:

            st.markdown(
                f'<div class="uploaded-file">'
                f'{Path(uploaded_file.name).name}'
                f'</div>',
                unsafe_allow_html=True
            )


    # --------------------------------------------------------
    # CONVERSATION
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-section">Conversation</div>',
        unsafe_allow_html=True
    )


    if st.button(
        "Clear conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


    # --------------------------------------------------------
    # ABOUT
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-section">About</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="sidebar-text">'
        'DocuMind AI is a document question-answering '
        'assistant powered by Retrieval-Augmented Generation.'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# MAIN TITLE
# ============================================================

st.markdown(
    '<div class="main-title">DocuMind AI</div>',
    unsafe_allow_html=True
)


# ============================================================
# DOCUMENT PROCESSING
# ============================================================

if uploaded_files:

    file_data = tuple(
        (
            Path(uploaded_file.name).name,
            uploaded_file.getvalue()
        )
        for uploaded_file in uploaded_files
    )


    with st.spinner(
        "Preparing your documents..."
    ):

        retriever, total_pages, total_chunks = (
            build_retriever(file_data)
        )


    if retriever is None:

        st.markdown(
            '<div class="document-info">'
            'No readable text was found in the uploaded documents.'
            '</div>',
            unsafe_allow_html=True
        )

        st.stop()


    st.markdown(
        f'<div class="document-info">'
        f'{len(uploaded_files)} document(s)'
        f' &nbsp;·&nbsp; '
        f'{total_pages} pages'
        f' &nbsp;·&nbsp; '
        f'{total_chunks} text chunks'
        f'</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # CHAT HISTORY
    # ========================================================

    for message in st.session_state.messages:

        role = message["role"]

        content = message["content"]


        with st.chat_message(role):

            st.markdown(content)


            if (
                role == "assistant"
                and message.get("sources")
            ):

                st.markdown(
                    '<div class="sources-title">'
                    'Sources'
                    '</div>',
                    unsafe_allow_html=True
                )


                for source, page in message["sources"]:

                    st.markdown(
                        f'<div class="source-item">'
                        f'{source} — Page {page}'
                        f'</div>',
                        unsafe_allow_html=True
                    )


    # ========================================================
    # CHAT INPUT
    # ========================================================

    question = st.chat_input(
        "Ask a question about your documents..."
    )


    if question:

        # ----------------------------------------------------
        # USER MESSAGE
        # ----------------------------------------------------

        with st.chat_message("user"):

            st.markdown(question)


        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )


        # ----------------------------------------------------
        # RETRIEVE RELEVANT DOCUMENTS
        # ----------------------------------------------------

        with st.spinner(
            "Searching your documents..."
        ):

            results = retriever.retrieve(
                question,
                top_k=5
            )


        # ----------------------------------------------------
        # BUILD CONTEXT
        # ----------------------------------------------------

        context_parts = []


        for result in results:

            document = result["document"]

            source = document.get(
                "source",
                "Unknown document"
            )

            page = document.get(
                "page",
                "Unknown"
            )

            text = document.get(
                "text",
                ""
            )


            context_parts.append(
                f"[Document: {source} | Page: {page}]\n"
                f"{text}"
            )


        context = "\n\n".join(
            context_parts
        )


        # ----------------------------------------------------
        # GENERATE ANSWER
        # ----------------------------------------------------

        with st.spinner(
            "Generating answer..."
        ):

            llm = get_llm()

            answer = llm.generate_answer(
                question,
                context
            )


        # ----------------------------------------------------
        # COLLECT SOURCES
        # ----------------------------------------------------

        sources = set()


        for result in results:

            document = result["document"]

            source = document.get(
                "source",
                "Unknown document"
            )

            page = document.get(
                "page",
                "Unknown"
            )

            sources.add(
                (
                    source,
                    page
                )
            )


        sources = sorted(
            sources,
            key=lambda item: (
                item[0],
                item[1]
            )
        )


        # ----------------------------------------------------
        # ASSISTANT MESSAGE
        # ----------------------------------------------------

        with st.chat_message("assistant"):

            st.markdown(answer)


            st.markdown(
                '<div class="sources-title">'
                'Sources'
                '</div>',
                unsafe_allow_html=True
            )


            for source, page in sources:

                st.markdown(
                    f'<div class="source-item">'
                    f'{source} — Page {page}'
                    f'</div>',
                    unsafe_allow_html=True
                )


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": sources
            }
        )


# ============================================================
# WELCOME SCREEN
# ============================================================

else:

    st.markdown(
        '<div class="welcome-area">'

        '<div class="welcome-title">'
        'How can I help with your documents?'
        '</div>'

        '<div class="welcome-text">'
        'Upload a PDF from the sidebar and ask questions about its contents.'
        '</div>'

        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# BOTTOM RAG PIPELINE
# ============================================================

st.markdown(
    '<div class="pipeline-bottom">'

    '<div class="pipeline-bottom-title">'
    'RAG PIPELINE'
    '</div>'

    '<div class="pipeline-flow">'
    'PDF&nbsp;&nbsp;→&nbsp;&nbsp;'
    'Text Extraction&nbsp;&nbsp;→&nbsp;&nbsp;'
    'Chunking&nbsp;&nbsp;→&nbsp;&nbsp;'
    'Embeddings&nbsp;&nbsp;→&nbsp;&nbsp;'
    'FAISS Retrieval&nbsp;&nbsp;→&nbsp;&nbsp;'
    'LLM Generation'
    '</div>'

    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer-text">'
    'DocuMind AI'
    '</div>',
    unsafe_allow_html=True
)