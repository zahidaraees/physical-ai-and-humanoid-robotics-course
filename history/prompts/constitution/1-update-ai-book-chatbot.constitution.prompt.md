---
id: 1
title: Update AI Book Chatbot Constitution
stage: constitution
date: 2025-12-19
surface: agent
model: Qwen
feature: none
branch: main
user: user
command: /sp.constitution
labels: [constitution, specification, ai-book, rag-chatbot]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

```
/sp.constitution

Project: Unified AI/Spec-Driven Book with Embedded RAG Chatbot about physical ai and humanoid robotic course.

Core principles:
- Accuracy through specification-driven development (Spec-Kit Plus + Claude Code)
- Clarity for technical audience (developers, AI engineers, and software architects)
- Integration (book content and chatbot must be seamlessly connected)
- Reproducibility (deployment steps traceable and repeatable via GitHub Pages)
- Reliability (chatbot answers must be grounded in book content and selected text)

Key standards:
- Book authored using Docusaurus framework.
- Deployment target: GitHub Pages (publicly accessible)
- Chatbot stack: OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres, Qdrant Cloud Free Tier
- Retrieval-Augmented Generation (RAG) must ensure responses are limited to book content or user-selected text
- Documentation of build and deployment pipeline included in book appendix
- Code examples must be executable and verified

Constraints:
- Book length: minimum 8 chapters, each with at least 2,000 words and maximum 3000 words.
- Technical references: minimum 20 sources (official docs, examples, specifications, or peer-reviewed material)
- Format: Markdown (Docusaurus-compatible), deployed static site
- Chatbot integration: must be functional within deployed site, tested with at least 50 sample queries

Success criteria:
- Book successfully deployed on local server as well as on GitHub pages.
- Chatbot embedded and operational, answering queries strictly from book content
- All technical claims verified against specifications or documentation
- Zero deployment errors across environments
- Passes reproducibility test: another developer can replicate book + chatbot setup using provided instructions

<<<EOF /sp.constitution
project: "AI/Spec-Driven Book with RAG Chatbot"

core_principles:
  - accuracy: "All claims verified against official docs and peer-reviewed sources"
  - clarity: "Readable for engineers, Flesch-Kincaid grade 11–13"
  - reproducibility: "Every step executable from specs"
  - rigor: "Chatbot must ground answers in book content"

standards:
  citation_format: "APA"
  source_types: "≥50% official docs or peer-reviewed"
  plagiarism: "0% tolerance"
  word_count: "3k–5k per chapter"
  sources_min: 20

constraints:
  format: "Docusaurus site deployed via GitHub Pages"
  chapters: "8–10"
  chatbot_stack: "OpenAI Agents/ChatKit, FastAPI, Neon Postgres, Qdrant"

success_criteria:
  - "Book deployed on GitHub Pages"
  - "Chatbot embedded and functional"
  - "All claims verified and reproducible"
  - "Zero plagiarism"
  - "Peer review passed"

EOF>>>
```

## Response snapshot

I have successfully created and updated the project constitution file at `.specify/memory/constitution.md` based on your requirements for the "Unified AI/Spec-Driven Book with Embedded RAG Chatbot about physical ai and humanoid robotic course".

### Key Updates Made:

- **New Constitution Created**: Created a complete constitution file from the template with all placeholder values filled in
- **Version Set**: Version 1.0.0 (initial creation) with today's date (2025-12-19) as both ratification and amendment date
- **Core Principles Defined**: Six core principles based on your requirements:
  1. Accuracy Through Specification-Driven Development
  2. Clarity for Technical Audience  
  3. Seamless Integration
  4. Reproducibility of Deployment
  5. Technical Standards Compliance
  6. Content Quality and Verification
- **Sections Added**: Content and Technical Constraints, Quality Assurance and Success Criteria, and Governance section

### Consistency Check:
- Verified that dependent templates (plan-template.md, spec-template.md, tasks-template.md) are compatible with the new constitution
- No template updates were required since this was an initial constitution creation

### Files Updated:
- `.specify/memory/constitution.md` - Complete constitution for the AI/Spec-Driven Book with RAG Chatbot project

### Suggested Commit Message:
```
feat: create project constitution for AI/Spec-Driven Book with RAG Chatbot
```

The constitution reflects all the core principles, standards, constraints, and success criteria you specified for your project involving a Docusaurus-based book with an embedded RAG chatbot that answers queries based on book content.

## Outcome

- ✅ Impact: Project constitution created with all specified principles and requirements
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md updated successfully
- 🔁 Next prompts: Build specification using the new constitution
- 🧠 Reflection: The constitution successfully captures all the required principles and constraints for the AI/Spec-Driven Book project with RAG Chatbot

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with feature specification based on this constitution