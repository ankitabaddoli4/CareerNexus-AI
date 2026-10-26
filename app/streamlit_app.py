
"""CareerNexus AI — Career Intelligence Streamlit application."""

import json
from datetime import datetime

import streamlit as st

from app.core import (
    analyze_match,
    answer_question,
    build_documents,
    extract_text,
    load_embedding_model,
    load_generation_model,
)


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="CareerNexus AI | Career Intelligence",
    page_icon="🎯",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .hero {
        padding: 1.5rem 1.7rem;
        border: 1px solid #dbe2f0;
        border-radius: 18px;
        background: linear-gradient(120deg, #f5f7ff, #ffffff);
        margin-bottom: 1.5rem;
    }
    .hero h1 {
        color: #3730a3;
        margin-bottom: 0.35rem;
    }
    .muted {
        color: #64748b;
        font-size: 0.92rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Cached models
# --------------------------------------------------

@st.cache_resource(show_spinner=False)
def get_embedding_model():
    """Load the embedding model once when available."""
    return load_embedding_model()


@st.cache_resource(show_spinner=False)
def get_generation_model():
    """Create the Gemini client configuration."""
    return load_generation_model()


# --------------------------------------------------
# Session state
# --------------------------------------------------

DEFAULTS = {
    "resume_text": "",
    "job_description": "",
    "analysis": None,
    "documents": [],
    "chat_history": [],
    "resume_filename": "",
    "last_analyzed_resume": "",
    "last_analyzed_job": "",
}

for key, default in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = default


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <h1>🎯 CareerNexus AI</h1>
        <div><strong>Your personal career workspace</strong></div>
        <p class="muted">
            Understand job requirements, compare your skills, and get
            evidence-based guidance for improving your application.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("How it works"):
    st.markdown(
        """
        1. Upload your resume.
        2. Paste the target job description.
        3. Review matched and missing recognised skills.
        4. Ask the Career AI Assistant questions about your documents.
        5. Download your career match report.
        """
    )

st.info(
    "Privacy note: your documents are processed by the app you run. "
    "When Gemini is configured, the question and retrieved document text "
    "are sent to Google's Gemini service. Avoid uploading sensitive "
    "personal information unnecessarily."
)


# --------------------------------------------------
# Resume upload
# --------------------------------------------------

st.header("1. Upload your resume")

uploaded_file = st.file_uploader(
    "Choose a resume file",
    type=["pdf", "docx", "txt", "md", "csv"],
    help="Supported formats: PDF, DOCX, TXT, Markdown, and CSV.",
)

if uploaded_file is not None:
    if st.session_state.resume_filename != uploaded_file.name:
        try:
            extracted_text = extract_text(uploaded_file)

            st.session_state.resume_text = extracted_text
            st.session_state.resume_filename = uploaded_file.name
            st.session_state.analysis = None
            st.session_state.documents = []
            st.session_state.chat_history = []
            st.session_state.last_analyzed_resume = ""
            st.session_state.last_analyzed_job = ""

            st.success(f"Resume loaded: {uploaded_file.name}")

        except Exception as exc:
            st.error(f"Couldn't read this file: {exc}")

if st.session_state.resume_text:
    with st.expander("Preview extracted resume text"):
        resume_preview = st.session_state.resume_text

        st.caption(
            f"Extracted characters: {len(resume_preview):,}"
        )

        st.text_area(
            "Resume text",
            value=resume_preview,
            height=280,
            disabled=True,
            label_visibility="collapsed",
        )

        st.download_button(
            "Download extracted resume text",
            data=resume_preview,
            file_name="extracted_resume.txt",
            mime="text/plain",
        )


# --------------------------------------------------
# Target role and job description
# --------------------------------------------------

st.header("2. Choose your target role")

role = st.selectbox(
    "Target role",
    [
        "AI / Machine Learning Engineer",
        "Python Developer",
        "Backend Developer",
        "Entry-level Software Engineer",
        "Data Scientist",
        "Other / Custom role",
    ],
)

job_description = st.text_area(
    "Paste the full job description",
    value=st.session_state.job_description,
    height=260,
    placeholder=(
        "Paste the job responsibilities, required skills, qualifications, "
        "and preferred experience here..."
    ),
)

st.session_state.job_description = job_description


# --------------------------------------------------
# Match analysis
# --------------------------------------------------

if st.button(
    "Analyze Career Match",
    type="primary",
    use_container_width=True,
):
    if not st.session_state.resume_text.strip():
        st.error("Please upload a resume first.")

    elif not job_description.strip():
        st.error("Please paste a job description first.")

    else:
        try:
            with st.spinner("Analyzing your resume and job description..."):
                result = analyze_match(
                    st.session_state.resume_text,
                    job_description,
                )

                documents = build_documents(
                    st.session_state.resume_text,
                    job_description,
                )

                st.session_state.analysis = result
                st.session_state.documents = documents
                st.session_state.chat_history = []

                st.session_state.last_analyzed_resume = (
                    st.session_state.resume_text
                )
                st.session_state.last_analyzed_job = job_description

            st.success("Career match analysis is ready.")

        except Exception as exc:
            st.error(f"Analysis failed: {exc}")


# --------------------------------------------------
# Analysis results
# --------------------------------------------------

result = st.session_state.analysis

if result:
    st.divider()
    st.header("3. AI Career Match Analysis")

    # Notify the user if the inputs have changed since analysis.
    analysis_is_current = (
        st.session_state.last_analyzed_resume
        == st.session_state.resume_text
        and st.session_state.last_analyzed_job
        == job_description
    )

    if not analysis_is_current:
        st.warning(
            "Your resume or job description has changed since the last "
            "analysis. Click Analyze Career Match again to refresh the results."
        )

    score = result.get(
        "coverage_percentage",
        result.get("match_percentage", 0),
    )

    matched = result.get("matched_skills", [])
    missing = result.get("missing_skills", [])
    required = result.get("required_skills", [])
    resume_skills = result.get("resume_skills", [])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Recognised Skills Coverage", f"{score}%")

    with col2:
        st.metric("Matched Skills", len(matched))

    with col3:
        st.metric("Skills to Review", len(missing))

    if required:
        st.progress(max(0, min(100, int(score))) / 100)

    st.caption(
        result.get(
            "note",
            "This is a keyword-based estimate, not a validated ATS score.",
        )
    )

    left, right = st.columns(2)

    with left:
        st.subheader("✅ Matched skills")

        if matched:
            st.markdown(
                "\n".join(f"- {skill}" for skill in matched)
            )
        else:
            st.write("No recognised matching skills were detected.")

    with right:
        st.subheader("🔎 Skills to review")

        if missing:
            st.markdown(
                "\n".join(f"- {skill}" for skill in missing)
            )
        else:
            st.write("No missing recognised skills were detected.")

    with st.expander("Recognised skills in your resume"):
        st.write(
            ", ".join(resume_skills)
            if resume_skills
            else "No supported skills were recognised."
        )

    with st.expander("Recognised skills in the job description"):
        st.write(
            ", ".join(required)
            if required
            else "No supported skills were recognised."
        )

    st.subheader("💡 Recommendations")

    for recommendation in result.get("recommendations", []):
        st.markdown(f"- {recommendation}")

    report = {
        "application": "CareerNexus AI",
        "generated_at": datetime.now().astimezone().isoformat(
            timespec="seconds"
        ),
        "target_role": role,
        "resume_filename": st.session_state.resume_filename,
        "match_percentage": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "resume_skills": resume_skills,
        "required_skills": required,
        "recommendations": result.get("recommendations", []),
        "note": result.get("note", ""),
    }

    st.download_button(
        "⬇️ Download Career Match Report (JSON)",
        data=json.dumps(report, indent=2, ensure_ascii=False),
        file_name="careernexus_ai_match_report.json",
        mime="application/json",
        use_container_width=True,
    )


# --------------------------------------------------
# Career AI Assistant
# --------------------------------------------------

st.divider()
st.header("4. Career AI Assistant")

st.write(
    "Ask questions about your resume and target job. The assistant retrieves "
    "relevant document sections to help ground its answers."
)

if not st.session_state.resume_text.strip():
    st.caption("Upload your resume to ask resume-specific questions.")

if not job_description.strip():
    st.caption("Paste a job description for role-specific guidance.")

example_questions = [
    "Which of my skills best match this AI Engineer job?",
    "What skills are not demonstrated in my resume for this job?",
    "How can I improve my resume for this role?",
    "Which projects should I highlight for this position?",
    "Summarise my projects and education using only my resume.",
]

selected_question = st.selectbox(
    "Example questions",
    ["Choose a question..."] + example_questions,
)

with st.form("career_assistant_form", clear_on_submit=True):
    user_question = st.text_input(
        "Your question",
        placeholder="Ask about your resume or target role...",
    )

    submitted = st.form_submit_button(
        "Ask CareerNexus AI",
        type="primary",
    )

if submitted:
    question = user_question.strip()

    if not question and selected_question != "Choose a question...":
        question = selected_question

    if not question:
        st.warning("Please enter a question or choose an example.")

    elif not st.session_state.resume_text.strip():
        st.warning("Please upload your resume first.")

    else:
        try:
            with st.spinner(
                "Retrieving relevant text and preparing your answer..."
            ):
                # Always rebuild documents from the current inputs.
                # This prevents retrieval from using an old job description.
                current_documents = build_documents(
                    st.session_state.resume_text,
                    job_description,
                )

                st.session_state.documents = current_documents

                embedding_model = get_embedding_model()
                generation_model = get_generation_model()

                # Retrieve more chunks than the original top_k=4.
                response = answer_question(
                    question=question,
                    documents=current_documents,
                    top_k=8,
                    embedding_model=embedding_model,
                    generation_model=generation_model,
                )

            st.session_state.chat_history.append(
                {
                    "question": question,
                    "answer": response.get("answer", ""),
                    "sources": response.get("sources", []),
                }
            )

        except Exception as exc:
            st.error(f"The assistant encountered an error: {exc}")


# --------------------------------------------------
# Chat history
# --------------------------------------------------

if st.session_state.chat_history:
    st.subheader("Conversation")

    for item in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(item["question"])

        with st.chat_message("assistant"):
            st.write(item["answer"])

            if item.get("sources"):
                st.caption(
                    "Retrieved from: " + ", ".join(item["sources"])
                )

    if st.button("🗑️ Clear conversation"):
        st.session_state.chat_history = []
        st.rerun()


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "CareerNexus AI provides keyword-based skills coverage and document-grounded "
    "guidance. It does not guarantee hiring outcomes. Verify all recommendations "
    "and include only skills and experience you can genuinely demonstrate."
)
