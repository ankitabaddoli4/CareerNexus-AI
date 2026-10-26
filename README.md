# 🎯 CareerNexus AI — RAG-Based Resume & Job Assistant

An AI-powered career assistant that analyzes resumes against job descriptions, identifies relevant skills and skill gaps, and answers career-related questions using retrieved document context.

CareerNexus AI combines resume parsing, keyword-based skill matching, document retrieval, and Gemini-powered question answering in a Streamlit application.

## 📌 Overview

Job seekers often find it difficult to determine whether their resumes align with a particular job description. CareerNexus AI helps simplify this process by comparing resume content with job requirements and providing evidence-based guidance.

Users can upload a resume, provide a target job description, review matched and missing skills, and ask questions about their qualifications and projects.

The application is designed as an entry-level AI engineering portfolio project demonstrating practical applications of Python, document processing, information retrieval, and generative AI.

## ✨ Features

### 1. Resume Upload and Text Extraction
- Upload a resume in a supported document format, such as PDF or DOCX.
- Extract text for analysis and retrieval.
- Preview extracted resume content.
- Review the extracted text to check whether relevant information was captured correctly.

### 2. Job Description Analysis
- Paste a job description into the application.
- Select a target role, such as AI/ML Engineer, Python Developer, Backend Developer, or Entry-Level Software Engineer.
- Identify relevant skills and job requirements.

### 3. Resume–Job Skills Matching
- Compare recognized resume skills with required job skills.
- Calculate keyword-based skills coverage.
- Display matched skills and skills that need review.
- Generate recommendations for improving resume alignment.

### 4. RAG-Based Career Assistant
- Ask questions about your resume and target job.
- Retrieve relevant document sections as context for answering questions.
- Use Google's Gemini model for AI-powered question answering when configured.
- Provide answers grounded in the available resume and job description content.
- Include retrieved-source information to help users assess the answer.

### 5. Career Improvement Recommendations
- Identify job requirements that may need stronger evidence.
- Suggest relevant skills to review.
- Recommend ways to improve project descriptions and resume content.
- Encourage users to include only skills and experience they can demonstrate.

### 6. Downloadable Analysis Report
- Download the skills analysis as a JSON report.
- Review the target role, matched skills, skills to review, recommendations, and coverage estimate outside the application.

### 7. Privacy Awareness
- Process uploaded documents within the running application.
- When Gemini is configured, send the question and retrieved document text to Google's Gemini service.
- Inform users not to upload sensitive information unnecessarily.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and processing |
| Streamlit | Interactive web interface |
| Google Gemini API | Generative AI question answering |
| Google Gen AI SDK | Communication with Gemini |
| PyMuPDF | PDF text extraction |
| python-docx | DOCX text extraction |
| Sentence Transformers | Optional semantic embeddings for retrieval |
| NumPy | Numerical operations where required |
| JSON | Downloadable analysis reports |
| Git and GitHub | Version control and source code hosting |

The exact libraries and optional components depend on the installed project dependencies and current configuration.

## 🏗️ Application Workflow

1. **Upload:** The user uploads a resume.
2. **Extract:** The application extracts readable document text.
3. **Provide requirements:** The user selects a target role and enters a job description.
4. **Analyze:** The application identifies skills in the resume and job description.
5. **Compare:** It calculates keyword-based coverage and identifies skills to review.
6. **Retrieve:** Relevant resume and job-description sections are selected for a question.
7. **Generate:** Gemini produces an answer based on the retrieved context, when configured.
8. **Export:** The user downloads the analysis report.

## 📂 Project Structure

The main application files are organized as follows:

```text
CareerNexus-AI/
├── app/
│   ├── streamlit_app.py
│   └── core.py
├── README.md
├── requirements.txt
└── .gitignore
```

Additional configuration or support files may be present depending on your local project setup.

- `app/streamlit_app.py` — Streamlit user interface, resume upload, job analysis, assistant interaction, and report download.
- `app/core.py` — Resume processing, skill extraction, matching, document chunking, retrieval, and question-answering logic.
- `requirements.txt` — Python package dependencies.
- `.gitignore` — Excludes local environments, secrets, and private files from Git.

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or a compatible version supported by your dependencies.
- Git.
- A Google Gemini API key for Gemini-powered answers.
- Internet access when using the Gemini API or downloading model dependencies.

### 1. Clone the repository

Replace `YOUR_GITHUB_USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/CareerNexus-AI.git
cd CareerNexus-AI
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the virtual environment's Python executable directly.

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

If `requirements.txt` is missing, create it using the dependencies actually imported by your project before running the application.

### 4. Configure the Gemini API key

Obtain an API key through Google AI Studio and set it as an environment variable.

**Windows PowerShell:**

```powershell
$env:GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
$env:GEMINI_MODEL = "gemini-3.5-flash-lite"
```

Replace the placeholder with your own API key. Keep the key private.

These commands configure the variables for the current PowerShell session. Set them again in a new session if necessary.

### 5. Run the application

From the project root directory:

```powershell
python -m streamlit run app/streamlit_app.py
```

Open the local URL displayed by Streamlit, usually:

```text
http://localhost:8501
```

## 🚀 How to Use

1. Launch CareerNexus AI.
2. Upload your resume.
3. Preview the extracted resume text.
4. Select your target career role.
5. Paste the full job description.
6. Run the AI Career Match Analysis.
7. Review the coverage estimate, matched skills, and skills to review.
8. Ask the Career AI Assistant questions about your resume and job requirements.
9. Download the analysis report and verify its contents.

### Example Questions

- What technical skills are mentioned in my resume?
- Which skills match this job description?
- Which required skills should I improve?
- What technologies did I use in my system monitoring project?
- Quote the resume evidence supporting your answer.
- Which projects are most relevant to this job?

## 📊 Example Analysis

For one test using an entry-level AI Engineer job description, the application displayed:

- **Recognized skills coverage:** 83%
- **Matched skills:** 15
- **Skills to review:** 3

The skills identified for review were model evaluation, object-oriented programming, and RAG.

These are example results from a particular resume and job description, not fixed application outputs.

## 🔍 Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation combines document retrieval with language-model generation.

In CareerNexus AI, the intended workflow is to retrieve relevant resume and job-description text before generating an answer. This helps the assistant use the supplied documents rather than relying entirely on general model knowledge.

The quality of the response depends on:
- How accurately the document text is extracted.
- How relevant the retrieved chunks are to the question.
- Whether the retrieved text contains the requested evidence.
- How faithfully the language model uses that context.

The assistant may not find every relevant detail in a document. Important answers should be checked against the original resume.

## ⚠️ Limitations

- The skills coverage percentage is a keyword-based estimate, not a validated ATS score.
- Skills not detected by the application may still be present in the resume.
- Retrieval may omit relevant sections or return incomplete context.
- AI-generated answers may contain errors and should be verified.
- The application does not predict hiring outcomes or guarantee interviews.
- Gemini-powered answers require valid API access and may be affected by service availability or usage limits.
- The actual supported file formats and retrieval behavior depend on the installed implementation.

## 🔐 Security and Privacy

- Never commit API keys, passwords, or tokens to GitHub.
- Keep `.env` and Streamlit secrets files out of version control.
- Do not upload private resumes or personal documents to a public repository.
- Do not commit virtual environments or generated reports containing personal data.
- Review `.gitignore` and `git status` before committing.
- When Gemini is enabled, retrieved document text and questions are sent to Google's Gemini service for answer generation.

## 🧪 Testing Checklist

- [ ] Resume uploads successfully.
- [ ] Extracted text is readable and complete enough for analysis.
- [ ] Job description input works.
- [ ] Skills coverage is calculated correctly for the recognized skills.
- [ ] Matched skills and skills to review are displayed.
- [ ] The assistant answers questions using relevant resume evidence.
- [ ] The JSON analysis report downloads and opens correctly.
- [ ] No API keys or private documents are committed to GitHub.

## 🔮 Future Improvements

- Improve retrieval ranking and relevance evaluation.
- Add automated tests for text extraction, skill matching, and retrieval.
- Provide more precise source citations for generated answers.
- Support additional resume formats where appropriate.
- Add a comparison view for multiple job descriptions.
- Improve error handling for API failures and unsupported documents.
- Add a reproducible evaluation dataset for testing retrieval quality.

## 👩‍💻 Author

**Ankita Baddoli**

AI Engineer | Python | Machine Learning | Generative AI & LLMs

- **GitHub:** https://github.com/ankitabaddoli4
- **LinkedIn:** https://linkedin.com/in/ankita-baddoli-62816027a

## 📄 Disclaimer

CareerNexus AI is a career-support and resume-analysis project intended for educational and informational purposes. Its skills coverage estimate is not a validated ATS score, a hiring prediction, or a guarantee of employment.
