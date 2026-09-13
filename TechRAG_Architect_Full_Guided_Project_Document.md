# TechRAG + Project Architect
## Full Guided Project Document

**Project Type:** RAG-Powered Technology Knowledge Assistant + AI Software Project Planner  
**Primary Stack:** Python, FastAPI, Streamlit, Ollama, Chroma/FAISS, Sentence Transformers, SQLite/PostgreSQL  
**Target Domain:** Software, AI, Data, Cloud, DevOps, Networking, Cybersecurity, GPU Computing, and related technology fields  
**Project Style:** Local-first, modular, production-oriented, explainable, testable, GitHub-ready

---

# 1. Project Vision

The goal of this project is to build a complete AI-powered software platform with two major capabilities:

1. **Technology Knowledge Assistant**
   - The user asks questions about software, AI, machine learning, networking, cybersecurity, cloud, databases, GPU computing, and other technology topics.
   - The system retrieves information from a curated collection of documents.
   - It generates grounded answers using a local Ollama LLM.
   - It shows the sources used to produce each answer.

2. **Project Architect**
   - The user provides a software/project idea.
   - The system starts an interactive requirements interview.
   - It asks one question at a time and waits for the user's answer.
   - Each next question is selected based on previous answers.
   - When enough requirements are gathered, the system generates professional software documentation such as:
     - Project specification
     - Software Requirements Specification
     - Architecture design
     - API design
     - Database design
     - Folder structure
     - Development roadmap
     - Testing plan
     - Deployment plan
     - README
     - GitHub task list

The final product should behave like a combination of:

- A private technology-focused AI knowledge assistant
- A document/PDF question-answering system
- A software requirements engineer
- A solution architect
- A technical project planner

---

# 2. Original Graduation Project Requirements

The uploaded project specification requires a complete RAG product with the following core components:

- Choose a domain and collect source documents.
- Clean and chunk the data.
- Generate embeddings.
- Store embeddings in a vector database.
- Build and evaluate a RAG pipeline.
- Use a local Ollama LLM.
- Build a FastAPI backend.
- Build a Streamlit or Gradio frontend.
- Return grounded answers with citations.
- Persist the vector store.
- Test the system.
- Publish the project to GitHub.
- Include a professional README.
- Deliver a live demonstration and recorded walkthrough.

The project will preserve all of those requirements while extending the system with the Project Architect and other advanced features.

---

# 3. Final Project Scope

## 3.1 Knowledge Domains

The knowledge base will focus on Technology & Computing.

### Core Categories

- Software Engineering
- Programming
- Artificial Intelligence
- Machine Learning
- Deep Learning
- Data Science
- Data Engineering
- Cloud Computing
- DevOps
- MLOps
- Web Development
- Embedded Systems
- IoT
- Robotics
- Computer Vision
- Natural Language Processing
- Databases
- Database Administration
- Operating Systems
- Distributed Systems
- System Design
- Software Architecture
- Algorithms & Data Structures
- Parallel & High-Performance Computing
- UI/UX Engineering
- Software Testing / QA
- Site Reliability Engineering
- Networking
- Cybersecurity
- Ethical Hacking / Penetration Testing
- Cryptography
- Reverse Engineering
- Malware Analysis
- Cloud Security
- Application Security
- Network Security
- GPU Computing

## 3.2 GPU Computing Topics

The GPU category may include:

- GPU architecture
- CUDA
- CUDA kernels
- CUDA memory hierarchy
- GPU acceleration
- Tensor Cores
- GPU programming
- Parallel algorithms
- AI inference acceleration
- AI training acceleration
- Multi-GPU computing
- Distributed GPU computing
- VRAM management
- Performance profiling
- GPU optimization
- CPU vs GPU workloads

---

# 4. Main Product Modes

The application should have two main modes.

## Mode A — Technology Knowledge Assistant

Purpose:

- Ask questions about the indexed technology documents.
- Get grounded answers.
- View the exact sources used.
- Filter by category or document.
- Upload additional supported documents.
- Continue conversations using chat context.

Example questions:

- Explain OSPF simply.
- What is backpropagation?
- Compare Docker and virtual machines.
- What is SQL injection?
- Explain CUDA memory hierarchy.
- What does this PDF say about distributed systems?
- Compare two documents on microservice architecture.

---

## Mode B — Project Architect

Purpose:

- Turn a rough software idea into professional software documentation.

Example:

User:

> I want to build an AI cybersecurity learning platform.

The system starts a guided interview.

Question 1:

> Who are the primary users?

The system waits for the user.

Question 2:

> What should users be able to do inside the platform?

It continues one question at a time until the requirements are sufficiently clear.

At the end, it generates a professional project package.

---

# 5. Project Architect Requirements Interview

## 5.1 Important Behavior

The Project Architect must:

- Ask one question at a time.
- Wait for the answer.
- Store each response.
- Use previous answers to decide the next question.
- Avoid asking irrelevant questions.
- Avoid repeating already answered questions.
- Allow the user to edit previous answers.
- Periodically summarize its understanding.
- Ask for confirmation before final generation.
- Generate documentation only when enough information is available.

---

## 5.2 Requirements Categories

The interview engine should try to understand:

### Project Identity

- Project name
- One-sentence idea
- Problem being solved
- Why the project matters
- Main objectives

### Users

- Target users
- User roles
- Admin roles
- User permissions
- Expected technical level of users

### Functional Requirements

- Main features
- Secondary features
- User workflows
- Admin workflows
- Search
- Uploads
- Notifications
- Reports
- Export features

### Frontend

- Web, desktop, mobile, CLI, or multiple interfaces
- Preferred framework
- Main screens
- Dashboard requirements
- Accessibility
- Responsive design

### Backend

- Preferred framework
- REST API / GraphQL
- Background tasks
- Real-time communication
- Authentication
- Authorization

### Database

- Whether a database is needed
- SQL or NoSQL
- Main entities
- Relationships
- Data retention
- Backups

### AI / ML

Only ask these if the project needs AI.

Possible branches:

- Machine learning
- Deep learning
- LLM
- RAG
- NLP
- Computer vision
- Recommendation systems
- Forecasting
- Generative AI

### RAG

Only ask these if RAG is needed.

Questions may include:

- What documents are used?
- Who uploads the documents?
- What formats?
- How should documents be categorized?
- What embedding model?
- What vector database?
- Should citations be displayed?
- Should users filter sources?
- Should conversation context affect retrieval?

### Computer Vision

Only ask if vision is required.

Questions may include:

- Classification or object detection?
- Images or videos?
- Dataset available?
- Real-time requirements?
- GPU available?
- Target model?

### Infrastructure

- Local or cloud
- Operating system
- Docker
- Kubernetes
- CI/CD
- Cloud provider
- GPU requirements
- Expected scale

### Security

- User authentication
- Role-based access
- Encryption
- Sensitive data
- Rate limiting
- Audit logging
- Secure secrets handling
- API protection

### Testing

- Unit testing
- Integration testing
- API testing
- UI testing
- Performance testing
- Security testing

### Project Constraints

- Deadline
- Team size
- Budget
- Hardware
- Existing technologies
- Required tools
- Restrictions

---

# 6. Adaptive Questioning Logic

The Project Architect should not use a fixed questionnaire blindly.

Instead:

```text
User Idea
   ↓
Intent / Project Type Detection
   ↓
Build Requirement State
   ↓
Find Missing Critical Information
   ↓
Select Best Next Question
   ↓
Wait for User
   ↓
Update Requirement State
   ↓
Repeat
```

Example logic:

```text
IF project_has_ai == false:
    skip AI questions

IF project_has_database == false:
    skip database engine questions

IF project_has_rag == true:
    ask document + embedding + retrieval questions

IF deployment == "local":
    skip cloud provider questions

IF user_already_specified_frontend == true:
    do not ask again
```

---

# 7. Requirement State Model

Store the interview as structured data.

Example:

```json
{
  "project_name": null,
  "idea": "",
  "problem_statement": "",
  "target_users": [],
  "user_roles": [],
  "core_features": [],
  "optional_features": [],
  "frontend": {
    "platform": null,
    "framework": null
  },
  "backend": {
    "framework": null,
    "api_style": "REST"
  },
  "database": {
    "required": null,
    "type": null,
    "technology": null
  },
  "ai": {
    "required": null,
    "types": []
  },
  "rag": {
    "required": false,
    "document_types": [],
    "vector_store": null,
    "citations": true
  },
  "deployment": {
    "target": null,
    "docker": null,
    "gpu": null
  },
  "security": {
    "authentication": null,
    "authorization": null
  },
  "testing": [],
  "deadline": null,
  "team_size": null
}
```

This makes the planner reliable and prevents important information from being lost.

---

# 8. Documentation Generated by Project Architect

The system should be able to generate:

```text
generated_docs/
├── PROJECT_SPECIFICATION.md
├── SRS.md
├── ARCHITECTURE.md
├── API_SPECIFICATION.md
├── DATABASE_DESIGN.md
├── SECURITY_PLAN.md
├── TESTING_PLAN.md
├── DEPLOYMENT_PLAN.md
├── ROADMAP.md
├── PROJECT_STRUCTURE.md
├── README.md
└── TASKS.md
```

---

# 9. Recommended Documentation Contents

## 9.1 PROJECT_SPECIFICATION.md

Include:

1. Project title
2. Executive summary
3. Problem statement
4. Proposed solution
5. Objectives
6. Target audience
7. Scope
8. Core features
9. Optional features
10. Functional requirements
11. Non-functional requirements
12. Assumptions
13. Constraints
14. Risks
15. Deliverables

---

## 9.2 SRS.md

Recommended structure:

1. Introduction
2. Purpose
3. Scope
4. Definitions
5. Product overview
6. User classes
7. Functional requirements
8. External interface requirements
9. Performance requirements
10. Security requirements
11. Reliability requirements
12. Maintainability
13. Scalability
14. Constraints

---

## 9.3 ARCHITECTURE.md

Include:

- Architecture overview
- Main services
- Data flow
- Frontend
- Backend
- Database
- Vector database
- LLM service
- Document processing pipeline
- Authentication
- Deployment
- Logging
- Monitoring

---

## 9.4 API_SPECIFICATION.md

For every endpoint include:

- Method
- Path
- Purpose
- Request body
- Query parameters
- Response format
- Error responses
- Authentication requirements
- Example request
- Example response

---

## 9.5 DATABASE_DESIGN.md

Include:

- Database choice
- Entity list
- Relationships
- Tables
- Columns
- Primary keys
- Foreign keys
- Indexes
- Data retention

---

## 9.6 ROADMAP.md

Include:

- Development phases
- Milestones
- Task dependencies
- Definition of done
- Testing checkpoints
- Release stages

---

# 10. Technology Knowledge Assistant — RAG Pipeline

The core RAG pipeline is:

```text
Documents
   ↓
Document Loader
   ↓
Text Extraction
   ↓
Cleaning
   ↓
Chunking
   ↓
Metadata Creation
   ↓
Embeddings
   ↓
Vector Database
   ↓
Retrieval
   ↓
Optional Reranking
   ↓
Prompt Construction
   ↓
Ollama LLM
   ↓
Grounded Answer + Citations
```

---

# 11. Document Ingestion

## Supported Initial Formats

Start with:

- PDF
- TXT
- Markdown

Later optionally add:

- DOCX
- HTML
- CSV
- PPTX

For the first version, PDF is sufficient to satisfy the core project.

---

# 12. PDF Processing

For each PDF:

1. Open file.
2. Extract text.
3. Detect page boundaries.
4. Detect empty or failed pages.
5. Normalize text.
6. Remove obvious repeated headers/footers if needed.
7. Preserve code blocks where possible.
8. Preserve page metadata.
9. Create chunks.
10. Save metadata.

Metadata example:

```json
{
  "document": "network_security.pdf",
  "page": 42,
  "category": "cybersecurity",
  "subcategory": "network_security",
  "section": "Firewalls",
  "chunk_id": "network_security_p42_c3"
}
```

---

# 13. Chunking Strategy

Avoid blindly splitting technical documents at arbitrary positions.

Recommended starting approach:

- Chunk size: 700–1200 tokens
- Overlap: 100–200 tokens
- Preserve page number
- Preserve document name
- Preserve heading where possible

For code-heavy documents:

- Do not split in the middle of functions/classes if avoidable.
- Preserve code fences.
- Keep code with its explanation.

Later improvement:

- Section-aware chunking
- Semantic chunking

---

# 14. Embeddings

Use a Sentence Transformers embedding model.

Requirements:

- Good semantic search performance
- Local execution
- Reasonable memory consumption
- Fast enough for the dataset

Store:

```text
chunk text
embedding vector
metadata
```

---

# 15. Vector Database

Recommended for the first implementation:

**ChromaDB**

Advantages:

- Simple Python API
- Local persistence
- Metadata support
- Appropriate for the graduation project

FAISS is also valid, but Chroma provides easier metadata filtering.

Example collections:

```text
technology_all
software_engineering
ai_ml
data_science
networking
cybersecurity
cloud
devops
gpu_computing
```

A single collection with metadata filters is also acceptable and may be easier to maintain.

---

# 16. Retrieval

Basic retrieval:

```text
User Question
   ↓
Question Embedding
   ↓
Vector Similarity Search
   ↓
Top K Chunks
```

Start with:

```text
top_k = 5
```

Then evaluate.

---

# 17. Advanced Retrieval Improvements

After the basic RAG works, add:

## Hybrid Search

Combine:

- Semantic vector retrieval
- Keyword/BM25 retrieval

## Reranking

Retrieve a larger candidate set:

```text
Top 10–20
```

Then rerank and keep:

```text
Best 3–5
```

## Metadata Filtering

Allow filtering by:

- Category
- Document
- Author
- Topic
- Page range
- Upload session

---

# 18. Citation System

Every answer should return sources.

Example:

```text
Sources:
1. network_security.pdf — page 42
2. ccna_routing.pdf — page 117
```

Backend response:

```json
{
  "answer": "...",
  "sources": [
    {
      "document": "network_security.pdf",
      "page": 42,
      "chunk_id": "network_security_p42_c3"
    }
  ]
}
```

---

# 19. Hallucination Protection

The prompt should explicitly instruct the model:

- Answer from supplied context.
- Do not invent unsupported facts.
- If the answer is not present, say so.
- Cite the supporting sources.

Example behavior:

> I could not find enough information in the indexed documents to answer this reliably.

This is better than guessing.

---

# 20. Conversation Memory

The system should support follow-up questions.

Example:

User:

> Explain TCP congestion control.

Then:

> Explain the second mechanism more simply.

To support this, maintain recent conversation messages and rewrite ambiguous follow-up queries before retrieval.

Do not rely on unlimited history.

Use a bounded window or conversation summary.

---

# 21. Category Routing

The system may automatically classify a question.

Example:

```text
"What is OSPF?"
       ↓
Networking
```

```text
"Explain CUDA shared memory"
       ↓
GPU Computing
```

```text
"What is SQL injection?"
       ↓
Application Security
```

The router can search the most likely category first, while still allowing global retrieval if confidence is low.

---

# 22. User Upload Feature

A strong improvement is allowing users to upload PDFs.

Workflow:

```text
Upload PDF
   ↓
Validate
   ↓
Extract
   ↓
Chunk
   ↓
Embed
   ↓
Store
   ↓
Ready for Chat
```

The UI should display:

- Filename
- Number of pages
- Number of chunks
- Category
- Processing status
- Errors

---

# 23. OCR Support

The original project expects documents to be checked for extractable text.

An advanced improvement is OCR for scanned PDFs.

Recommended approach:

1. Try normal text extraction.
2. Detect pages with little/no extracted text.
3. Mark them as OCR-required.
4. Run OCR only on those pages.
5. Store OCR output with the same page metadata.

OCR should be treated as an optional advanced phase, not a requirement for the first working version.

---

# 24. Project Architecture

Recommended high-level architecture:

```text
                    ┌──────────────────────┐
                    │      Streamlit       │
                    │      Frontend        │
                    └─────────┬────────────┘
                              │ REST
                              ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │       Backend        │
                    └─────────┬────────────┘
                              │
              ┌───────────────┼─────────────────┐
              │               │                 │
              ▼               ▼                 ▼
       RAG Service      Planner Service    User/Session
              │               │              Service
              │               │
       ┌──────┴───────┐       │
       │              │       │
       ▼              ▼       ▼
 Vector Store      Ollama   Planner State
   ChromaDB          LLM       Database
       │              │
       └──────┬───────┘
              ▼
      Grounded Response
```

---

# 25. Recommended Project Folder Structure

```text
techrag-project/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   │
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── health.py
│   │   │       ├── query.py
│   │   │       ├── documents.py
│   │   │       ├── categories.py
│   │   │       └── planner.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── constants.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── query.py
│   │   │   ├── document.py
│   │   │   └── planner.py
│   │   │
│   │   ├── services/
│   │   │   ├── rag/
│   │   │   │   ├── embeddings.py
│   │   │   │   ├── retrieval.py
│   │   │   │   ├── reranker.py
│   │   │   │   ├── prompting.py
│   │   │   │   └── generation.py
│   │   │   │
│   │   │   ├── ingestion/
│   │   │   │   ├── loader.py
│   │   │   │   ├── parser.py
│   │   │   │   ├── cleaner.py
│   │   │   │   ├── chunker.py
│   │   │   │   └── indexer.py
│   │   │   │
│   │   │   └── planner/
│   │   │       ├── interview.py
│   │   │       ├── question_selector.py
│   │   │       ├── requirement_state.py
│   │   │       ├── validator.py
│   │   │       └── document_generator.py
│   │   │
│   │   ├── database/
│   │   │   ├── models.py
│   │   │   ├── session.py
│   │   │   └── repositories/
│   │   │
│   │   └── utils/
│   │       ├── logging_config.py
│   │       └── file_utils.py
│   │
│   ├── tests/
│   │   ├── test_health.py
│   │   ├── test_query.py
│   │   ├── test_ingestion.py
│   │   └── test_planner.py
│   │
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
├── frontend/
│   ├── app.py
│   ├── pages/
│   │   ├── chat.py
│   │   ├── documents.py
│   │   ├── project_architect.py
│   │   └── settings.py
│   ├── components/
│   │   ├── chat_message.py
│   │   ├── source_card.py
│   │   └── upload_panel.py
│   ├── api_client.py
│   ├── requirements.txt
│   └── .env.example
│
├── notebooks/
│   ├── rag_pipeline.ipynb
│   └── evaluation.ipynb
│
├── data/
│   ├── raw/
│   │   ├── software_engineering/
│   │   ├── programming/
│   │   ├── ai_ml/
│   │   ├── data_science/
│   │   ├── data_engineering/
│   │   ├── cloud/
│   │   ├── devops/
│   │   ├── networking/
│   │   ├── cybersecurity/
│   │   ├── databases/
│   │   ├── operating_systems/
│   │   └── gpu_computing/
│   │
│   ├── processed/
│   └── vector_store/
│
├── generated_docs/
├── docs/
│   ├── architecture/
│   ├── screenshots/
│   └── api/
│
├── scripts/
│   ├── ingest_documents.py
│   ├── rebuild_index.py
│   └── evaluate_rag.py
│
├── .gitignore
├── README.md
├── docker-compose.yml
└── LICENSE
```

---

# 26. Backend API Design

## Required Core Endpoints

### Health

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

### Ask RAG Question

```http
POST /query
```

Request:

```json
{
  "question": "Explain OSPF",
  "category": "networking"
}
```

Response:

```json
{
  "answer": "...",
  "sources": []
}
```

---

# 27. Extended API Endpoints

## Documents

```http
POST /documents/upload
GET /documents
DELETE /documents/{document_id}
POST /documents/{document_id}/reindex
```

## Categories

```http
GET /categories
```

## Planner

```http
POST /planner/session
POST /planner/{session_id}/answer
GET /planner/{session_id}/state
POST /planner/{session_id}/generate
```

---

# 28. Planner API Flow

Create session:

```http
POST /planner/session
```

Request:

```json
{
  "idea": "I want to build an AI cybersecurity learning platform."
}
```

Response:

```json
{
  "session_id": "abc123",
  "question": "Who are the primary users of the platform?"
}
```

Submit answer:

```http
POST /planner/abc123/answer
```

Request:

```json
{
  "answer": "University students and beginners."
}
```

Response:

```json
{
  "next_question": "What should users be able to do inside the platform?",
  "progress": 0.15
}
```

---

# 29. Frontend Design

Recommended main navigation:

```text
TechRAG
├── Chat
├── Documents
├── Project Architect
├── Generated Documentation
└── Settings
```

---

# 30. Chat Page

Should include:

- Chat history
- Question input
- Category filter
- Document filter
- Answer
- Citations
- Source preview
- Loading indicator
- Error messages

Optional:

- Simple / Detailed / Technical answer mode
- Copy response
- Export conversation

---

# 31. Documents Page

Display:

- Uploaded files
- Category
- Number of pages
- Number of chunks
- Status
- Upload time

Actions:

- Upload
- Delete
- Re-index
- Change category

---

# 32. Project Architect Page

The page should show:

- Project idea
- Current question
- User answer input
- Progress indicator
- Requirement summary
- Previous answers
- Edit previous answer
- Generate documentation when ready

Important:

Only one active question should be presented at a time.

---

# 33. Ollama

Ollama will provide the local LLM.

The backend should:

- Check that Ollama is available.
- Load configuration once.
- Avoid repeatedly initializing resources.
- Handle model errors cleanly.

Configuration example:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=<selected_model>
```

Do not hard-code the model name in multiple files.

---

# 34. GPU Support

GPU support should be treated as infrastructure acceleration.

Features:

- Detect available GPU.
- Use GPU-supported local inference where available.
- Display selected model.
- Optionally display:
  - VRAM
  - GPU utilization
  - inference time
  - tokens/second

GPU monitoring is optional and should not block the core project.

---

# 35. Database

For the first professional version:

**SQLite** is enough for:

- Chat sessions
- Planner sessions
- Requirement answers
- Generated documentation metadata
- Uploaded document metadata

For a larger deployment:

**PostgreSQL** is recommended.

The vector database remains separate.

---

# 36. Suggested Database Entities

```text
User
Conversation
Message
Document
DocumentChunk
Category
PlannerSession
PlannerAnswer
GeneratedDocument
```

Possible relationships:

```text
User
 ├── Conversations
 ├── Documents
 └── PlannerSessions

Conversation
 └── Messages

PlannerSession
 ├── PlannerAnswers
 └── GeneratedDocuments
```

Authentication can be postponed until after the main project works.

---

# 37. Security

Minimum security requirements:

- Keep secrets in `.env`.
- Never commit `.env`.
- Validate uploaded file types.
- Limit upload size.
- Sanitize filenames.
- Do not execute uploaded files.
- Validate API input using Pydantic.
- Configure CORS properly.
- Use safe error messages.
- Add rate limiting later if public.

For cybersecurity documents, make clear that the knowledge assistant is educational and defensive in purpose.

---

# 38. Logging

Log:

- Startup
- Vector store loading
- Document processing
- Query requests
- Retrieval timing
- LLM timing
- Errors
- Planner state transitions

Do not log sensitive secrets.

---

# 39. Testing Strategy

## Unit Tests

Test:

- Text cleaning
- Chunking
- Metadata creation
- Question routing
- Planner state updates
- Requirement validation

## API Tests

Test:

- `/health`
- `/query`
- invalid query
- planner session creation
- planner answer flow

## Integration Tests

Test:

```text
Question
→ Retrieval
→ Prompt
→ LLM
→ Answer
```

Also:

```text
Project Idea
→ Interview
→ Stored Requirements
→ Generated Documentation
```

---

# 40. Required RAG Evaluation

Prepare at least 10 test questions.

Evaluation table:

| # | Question | Expected Topic | Retrieved Source | Grounded? | Correct? |
|---|---|---|---|---|---|
| 1 | What is OSPF? | Networking | ... | Yes | Yes |
| 2 | Explain CNN pooling | AI | ... | Yes | Yes |

Also record:

- Retrieval relevance
- Citation correctness
- Hallucination
- Response latency

---

# 41. Advanced Evaluation

Later calculate:

- Recall@K
- Precision@K
- MRR
- Answer faithfulness
- Context relevance
- Answer relevance

These are optional improvements after the required evaluation works.

---

# 42. Phase-by-Phase Development Roadmap

## Phase 0 — Planning

Tasks:

- Finalize project name.
- Finalize scope.
- Decide Core vs Extended track.
- Decide first document categories.
- Decide Ollama model.
- Decide Chroma vs FAISS.
- Create GitHub repository.

Deliverable:

```text
docs/project_scope.md
```

---

## Phase 1 — Environment Setup

Install and verify:

- Python 3.10+
- Git
- Ollama
- VS Code
- Virtual environment

Create:

```text
.venv
```

Install first dependencies.

Checkpoint:

```text
python --version
git --version
ollama --version
```

---

## Phase 2 — Project Structure

Create the repository structure.

Add:

- `.gitignore`
- `.env.example`
- `README.md`

Make first commit.

---

## Phase 3 — Document Collection

Start small.

Recommended first categories:

1. Software Engineering
2. AI / ML
3. Networking
4. Cybersecurity
5. Cloud
6. Databases
7. Operating Systems
8. GPU Computing

Do not begin with hundreds of PDFs.

Start with a manageable set that can be evaluated.

---

## Phase 4 — RAG Notebook

Build:

```text
notebooks/rag_pipeline.ipynb
```

Sections:

1. Imports
2. Configuration
3. Load documents
4. Inspect documents
5. Clean text
6. Chunk text
7. Create embeddings
8. Store in Chroma
9. Retrieve
10. Build prompt
11. Call Ollama
12. Generate answer
13. Show citations
14. Evaluate
15. Persist vector store

Checkpoint:

Notebook must run top-to-bottom after kernel restart.

---

## Phase 5 — RAG Evaluation

Prepare 10+ questions.

Document:

- successes
- failures
- bad retrieval
- hallucinations
- improvements

Do not move to advanced retrieval before basic retrieval is measured.

---

## Phase 6 — Backend

Create FastAPI.

Implement:

- configuration
- startup/lifespan
- health endpoint
- query endpoint
- retrieval service
- generation service
- schemas
- error handling

Checkpoint:

Open:

```text
http://localhost:8000/docs
```

Test both endpoints.

---

## Phase 7 — Frontend

Build Streamlit frontend.

Initial features:

- Question input
- Chat display
- Source display
- API calls
- Loading state
- Error message

Checkpoint:

User asks real question and receives a grounded answer.

---

## Phase 8 — Document Upload

Add:

- Upload form
- Category selection
- Validation
- Ingestion
- Incremental indexing

Checkpoint:

Upload a new PDF without rebuilding all existing documents.

---

## Phase 9 — Metadata & Category Routing

Add:

- Categories
- Filtering
- Question classification
- Metadata-aware retrieval

Checkpoint:

Networking questions preferentially retrieve networking documents.

---

## Phase 10 — Advanced Retrieval

Add one improvement at a time:

1. Hybrid search
2. Reranking
3. Query rewriting
4. Conversation-aware retrieval

Evaluate after every change.

---

## Phase 11 — Project Architect MVP

Implement:

- Start planner session
- Store idea
- Ask first question
- Submit answer
- Store answer
- Ask next question
- Finish when minimum fields are complete

Do not generate all documentation yet.

Checkpoint:

A complete interview can be completed without losing state.

---

## Phase 12 — Adaptive Planner

Add:

- Branching questions
- Skip irrelevant sections
- Requirement completeness scoring
- Summary checkpoints
- User confirmation

Example:

```text
Requirements Complete: 78%
Missing:
- Deployment target
- Authentication decision
- Deadline
```

---

## Phase 13 — Documentation Generator

Generate:

- Project specification
- SRS
- Architecture
- Roadmap

Then add:

- API specification
- Database design
- Testing plan
- README

Checkpoint:

Generated files match the user's interview answers.

---

## Phase 14 — Persistence

Store:

- Chat sessions
- Planner sessions
- Answers
- Generated docs metadata

Use SQLite initially.

---

## Phase 15 — Testing

Create:

- Unit tests
- API tests
- Planner tests
- RAG integration tests

Run:

```bash
pytest
```

---

## Phase 16 — Docker

Create:

- Backend Dockerfile
- Frontend Dockerfile if desired
- `docker-compose.yml`

Do not make Docker mandatory for early development.

---

## Phase 17 — GitHub & README

README must contain:

- Overview
- Features
- Architecture
- Tech stack
- Project structure
- Installation
- Ollama setup
- Environment variables
- Running backend
- Running frontend
- API usage
- Evaluation
- Screenshots
- Limitations
- Future work

---

## Phase 18 — Final Verification

Fresh-test procedure:

1. Clone repository into a new folder.
2. Follow only README.
3. Create environment.
4. Install dependencies.
5. Start Ollama.
6. Load data/vector store.
7. Start backend.
8. Start frontend.
9. Ask test questions.
10. Run planner.
11. Generate documentation.
12. Run tests.

If any step requires hidden knowledge, improve the README.

---

# 43. MVP Definition

The MVP should include:

- PDF document collection
- PDF extraction
- Chunking
- Embeddings
- Chroma vector store
- Ollama
- Retrieval
- Grounded answer
- Citations
- FastAPI
- Streamlit
- 10-question evaluation
- Basic Project Architect interview
- Project specification generation

Do not add every advanced feature before this works.

---

# 44. Version 2 Features

After MVP:

- User uploads
- Multiple categories
- Automatic question routing
- Chat history
- Follow-up questions
- Source preview
- Hybrid retrieval
- Reranking
- SQLite persistence
- Full SRS generator

---

# 45. Version 3 Features

Optional advanced version:

- OCR
- Diagram understanding
- Multimodal input
- Image upload
- Computer vision
- Authentication
- User-private libraries
- PostgreSQL
- Admin dashboard
- GPU monitoring
- Advanced evaluation
- CI/CD
- Cloud deployment

---

# 46. Example End-to-End RAG Flow

User:

> Explain the difference between symmetric and asymmetric encryption.

System:

1. Receives question.
2. Classifies it as Cryptography.
3. Searches cryptography/security chunks.
4. Retrieves top results.
5. Reranks them if enabled.
6. Builds grounded prompt.
7. Sends to Ollama.
8. Produces answer.
9. Returns citations.
10. Displays answer and sources.

---

# 47. Example End-to-End Project Architect Flow

User:

> I want to build a smart university attendance system.

System:

> Who are the main users?

User:

> Students and instructors.

System:

> How should attendance be recorded?

User:

> Face recognition.

System recognizes computer vision is required.

Next:

> Will recognition run from a live camera, uploaded images, or both?

The interview continues.

Later:

> Here is my understanding of your project...

The user confirms.

System generates:

```text
PROJECT_SPECIFICATION.md
SRS.md
ARCHITECTURE.md
ROADMAP.md
TESTING_PLAN.md
README.md
```

---

# 48. Development Rules

Follow these rules throughout the project.

1. Build one working layer at a time.
2. Test before adding the next layer.
3. Keep business logic out of FastAPI route functions.
4. Keep frontend separate from backend.
5. Never hard-code secrets.
6. Never rebuild embeddings on every request.
7. Store source metadata from the beginning.
8. Preserve page numbers.
9. Do not trust the LLM to invent citations.
10. Validate generated planner documentation against stored answers.
11. Keep configuration centralized.
12. Keep modules small and understandable.
13. Commit frequently.
14. Maintain a clean Git history.
15. Make the README reproducible.

---

# 49. Suggested Git Strategy

Branches:

```text
main
develop
feature/rag-pipeline
feature/backend
feature/frontend
feature/document-upload
feature/project-architect
feature/reranking
```

For a small individual project, a simpler strategy is also acceptable:

```text
main
feature/*
```

Commit examples:

```text
chore: initialize project structure
feat: add PDF document loader
feat: implement Chroma vector store
feat: add RAG query endpoint
feat: add Streamlit chat interface
feat: add planner interview sessions
test: add query endpoint tests
docs: add project setup instructions
```

---

# 50. Git Ignore

At minimum:

```gitignore
.venv/
__pycache__/
*.pyc
.env
*.log
.ipynb_checkpoints/
data/raw/
data/vector_store/
```

Whether the vector store and raw documents are committed depends on size and project submission rules.

---

# 51. Environment Variables

Example:

```env
APP_ENV=development

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=your_model_name

CHROMA_PATH=./data/vector_store

DATABASE_URL=sqlite:///./techrag.db

FRONTEND_ORIGIN=http://localhost:8501
```

---

# 52. Common Failure Cases

## RAG

Problem:

Wrong source retrieved.

Possible fixes:

- Better chunking
- Smaller/larger chunks
- Increase top-k
- Better embeddings
- Add reranking
- Hybrid retrieval

---

Problem:

LLM answers from general knowledge.

Fix:

- Strong grounding prompt
- Require citations
- Refuse if context is insufficient

---

Problem:

Answers lack page citations.

Fix:

- Store page metadata during extraction
- Propagate metadata through retrieval

---

## Planner

Problem:

Planner repeats questions.

Fix:

- Store answered fields
- Track question history

---

Problem:

Planner asks irrelevant questions.

Fix:

- Conditional branches
- Project-type detection

---

Problem:

Generated documentation contradicts user answers.

Fix:

- Generate from structured requirement state
- Include validation pass before export

---

# 53. Presentation Plan

Recommended demo order:

1. Introduce the problem.
2. Explain RAG.
3. Show architecture.
4. Show document knowledge base.
5. Ask a technical question.
6. Show citations.
7. Show category filtering.
8. Open Project Architect.
9. Enter a project idea.
10. Answer several adaptive questions.
11. Show requirement summary.
12. Generate professional documentation.
13. Show GitHub repository.
14. Show evaluation results.

---

# 54. Final Deliverables

Required core deliverables:

- `notebooks/rag_pipeline.ipynb`
- persisted vector store
- FastAPI backend
- Streamlit frontend
- requirements
- `.env.example`
- tests
- README
- GitHub repository
- evaluation results
- live demonstration
- recorded walkthrough

Extended project deliverables:

- Project Architect
- planner sessions
- generated software documentation
- upload interface
- category system
- advanced retrieval
- optional OCR / multimodal features

---

# 55. Recommended Build Order

Do not start with all features.

Use this exact priority:

```text
1. Project setup
2. PDF loading
3. Cleaning
4. Chunking
5. Embeddings
6. Vector database
7. Retrieval
8. Ollama response
9. Citations
10. Evaluation
11. FastAPI
12. Streamlit
13. Uploads
14. Categories
15. Project Architect MVP
16. Adaptive planner
17. Documentation generation
18. Advanced retrieval
19. Persistence
20. Testing
21. Docker
22. GitHub polish
23. Final demo
```

---

# 56. First Development Session

When implementation begins, the first session should do only the following:

### Step 1
Choose the final project name.

Suggested:

**TechRAG Architect**

### Step 2
Create the root project directory.

### Step 3
Create the professional folder structure.

### Step 4
Create and activate `.venv`.

### Step 5
Install minimum dependencies.

### Step 6
Verify Ollama.

### Step 7
Initialize Git.

### Step 8
Create `.gitignore`.

### Step 9
Create `.env.example`.

### Step 10
Create initial `README.md`.

### Step 11
Add a very small initial PDF dataset.

### Step 12
Commit.

Only after this should implementation of the RAG notebook begin.

---

# 57. Final Project Definition

**TechRAG Architect** is a local-first AI platform for technology knowledge retrieval and software project planning.

It combines:

- RAG
- Local LLMs
- Vector search
- Technology document knowledge bases
- Source-grounded answers
- Software requirements engineering
- Adaptive interviews
- Professional documentation generation
- FastAPI
- Streamlit
- Optional GPU acceleration
- Optional multimodal processing

The project should first satisfy the graduation project's required RAG pipeline and then add the Project Architect as the main differentiating feature.

---

# 58. Success Criteria

The project is successful when:

- A user can ask a technology question.
- Relevant document chunks are retrieved.
- The answer is grounded in those chunks.
- Sources are displayed.
- The vector store is persisted.
- The backend and frontend communicate correctly.
- The application can run from a clean setup.
- At least 10 RAG test questions are evaluated.
- A user can start a project-planning session.
- The planner asks one question at a time.
- Answers persist across the interview.
- Questions adapt to previous responses.
- The planner generates professional documentation consistent with the user's requirements.
- The repository is documented well enough for another person to run it.

---

# 59. Immediate Next Step

Start with **Phase 0 + Phase 1**:

1. Confirm the final project name.
2. Confirm the initial knowledge categories.
3. Choose the first small document dataset.
4. Create the folder structure.
5. Create `.venv`.
6. Install dependencies.
7. Install/verify Ollama.
8. Initialize Git/GitHub.
9. Begin `rag_pipeline.ipynb`.

Do not start advanced features until the basic RAG question → retrieval → Ollama → cited answer flow works correctly.
