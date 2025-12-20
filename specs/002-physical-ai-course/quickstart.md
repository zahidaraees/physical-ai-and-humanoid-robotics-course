# Quickstart Guide: Physical AI and Humanoid Robotics Course

**Date**: 2025-12-19
**Feature**: Physical AI and Humanoid Robotics Course

## Getting Started

This guide will help you set up the development environment and begin working on the Physical AI and Humanoid Robotics Course. The course consists of 8 chapters with integrated chatbot functionality and reproducibility checkpoints.

## Prerequisites

- Node.js 18 or higher
- Python 3.11 or higher
- Git
- A text editor or IDE
- GitHub account (for deployment)
- OpenAI API key (for chatbot functionality)
- Qdrant Cloud account (for RAG implementation)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install Dependencies
```bash
npm install
pip install -r requirements.txt  # for Python simulations and tooling
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory with the following:
```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
```

### 4. Start Development Server
```bash
npm start
```

This will start the Docusaurus development server and open the course in your browser at http://localhost:3000.

### 5. Create the Course Structure
The course follows this structure:
```
docs/
├── chapters/
│   ├── 01-foundations-of-physical-ai/
│   │   ├── index.md
│   │   ├── subchapter-1.md
│   │   ├── subchapter-2.md
│   │   └── subchapter-3.md
│   ├── 02-humanoid-robotics-architecture/
│   ├── 03-control-systems-motion-planning/
│   ├── 04-perception-environment-interaction/
│   ├── 05-learning-adaptation/
│   ├── 06-human-robot-interaction/
│   ├── 07-ethics-governance-physical-ai/
│   └── 08-capstone-integrated-humanoid-system/
├── components/
│   └── chatbot/
├── static/
│   ├── images/
│   ├── datasets/  # For chapter 4
│   ├── simulations/  # For chapter 3
│   └── build-logs/  # For chapter 8
```

## Creating a New Chapter

1. Create a new directory in `docs/chapters/` with the format `NN-chapter-name`
2. Create an `index.md` file with the main chapter content (minimum 2,000 words)
3. Create additional markdown files for subchapters (minimum 3, each 300-400 words)
4. Add the chapter to `sidebars.js` to make it appear in navigation
5. Implement the chapter-specific reproducibility checkpoint as specified in the roadmap
6. Add the chapter content to the chatbot knowledge base

## Reproducibility Checkpoints

Each chapter must include its specific reproducibility checkpoint:

- **Chapter 1**: Source references validated via Spec-Kit Plus
- **Chapter 2**: Diagrams generated via Claude Code
- **Chapter 3**: Python simulations logged
- **Chapter 4**: Datasets documented
- **Chapter 5**: Training scripts stored in GitHub
- **Chapter 6**: FastAPI endpoints documented
- **Chapter 7**: Governance specs enforced via CI dashboards
- **Chapter 8**: Full build logs published

## Chapter Requirements

- Minimum 2,000 words per chapter
- At least 3 subchapters of 300-400 words each
- Reproducibility checkpoints as specified in the roadmap
- Technical depth appropriate for engineers and researchers
- Integration with chatbot functionality
- Citations from verified sources (minimum 20 per chapter)

## Chatbot Integration

The course includes an AI-powered chatbot with chapter-specific knowledge:

1. Content for each chapter is converted to embeddings and stored in Qdrant
2. User queries are matched against chapter content using vector similarity
3. Responses are generated using OpenAI API with retrieved context
4. Responses are limited to course content and include citations

To add chatbot functionality to a new chapter:
1. Add the chapter content to the RAG pipeline
2. Generate embeddings for the new content
3. Test chapter-specific queries to ensure accuracy

## Running Tests

To validate your content and functionality:

### Content Validation
```bash
npm run build
npm run serve
```

This will build the site and serve it locally to check for any errors or broken links.

### Chatbot Testing
```bash
npm run test-chatbot
```

This runs sample queries against the chatbot to verify accurate responses.

### Reproducibility Validation
Run the appropriate validation script for your chapter:
- Chapter 1: `npm run validate-sources` (Spec-Kit Plus validation)
- Chapter 2: `npm run generate-diagrams` (Claude Code diagrams)
- Chapter 3: `npm run test-simulations` (Python simulation validation)
- Chapter 4: `npm run document-datasets`
- Chapter 5: `npm run store-training-scripts`
- Chapter 6: `npm run document-endpoints`
- Chapter 7: `npm run ci-dashboard`
- Chapter 8: `npm run publish-build-logs`

## Deployment

The course is deployed to GitHub Pages. After pushing changes to the main branch, GitHub Actions will automatically:

1. Build the Docusaurus site
2. Process all reproducibility checkpoints
3. Update the chatbot knowledge base
4. Deploy the site to GitHub Pages

To deploy manually:
```bash
npm run deploy
```

## Development Workflow

### Adding a New Chapter
1. Create the chapter directory and files
2. Write the content meeting all requirements
3. Implement the reproducibility checkpoint
4. Add content to the chatbot knowledge base
5. Test chatbot responses for the chapter
6. Validate all links and cross-references
7. Add the chapter to the navigation

### Updating the Chatbot
1. Update the knowledge base with new content
2. Regenerate embeddings in Qdrant
3. Test new queries to ensure accuracy
4. Verify citations are properly formatted

## Troubleshooting

### Common Issues
- If the chatbot doesn't respond, check that:
  - OpenAI API key is properly configured
  - Qdrant cluster is accessible
  - Chapter content has been added to the knowledge base
- If reproducibility checks fail, ensure:
  - All required tools are installed
  - Environment variables are set correctly
  - Resources are in the correct location

### Performance Optimization
- Large vector databases can slow down chatbot responses
- Consider implementing caching for common queries
- Optimize embedding generation for better relevance