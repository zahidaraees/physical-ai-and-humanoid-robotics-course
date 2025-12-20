# Data Model: Physical AI and Humanoid Robotics Course

**Model Phase**: 1
**Date**: 2025-12-19
**Feature**: Physical AI and Humanoid Robotics Course

## Entities

### Course Chapter
- **Attributes**:
  - id: string (unique identifier, e.g., "01-foundations-of-physical-ai")
  - title: string (display title)
  - description: string (brief summary)
  - wordCount: integer (minimum 2000)
  - subchapters: array of Subchapter objects
  - reproducibilityCheckpoints: array of Checkpoint objects
  - chatbotKnowledgeBase: string (path to RAG source for this chapter)
  - author: string (author of the chapter)
  - createdAt: date (creation date)
  - updatedAt: date (last updated date)
  - status: string (draft, in-review, published)
- **Relationships**:
  - Contains multiple Subchapter entities
  - Links to multiple ReproducibilityCheckpoint entities
  - Connected to one ChatbotResponseContext entity

### Subchapter
- **Attributes**:
  - id: string (unique within parent chapter)
  - title: string (display title)
  - content: string (markdown content, minimum 300-400 words)
  - position: integer (order within parent chapter)
  - wordCount: integer (actual word count)
- **Relationships**:
  - Belongs to one Chapter entity

### Reproducibility Checkpoint
- **Attributes**:
  - id: string (unique identifier)
  - title: string (descriptive title)
  - description: string (what needs to be reproduced)
  - method: string (how to reproduce - Spec-Kit Plus, Claude Code, Python simulation, etc.)
  - resources: array of Resource objects
  - verificationSteps: array of strings (steps to verify)
  - chapterId: string (associated chapter)
  - type: string (source-validation, diagram-generation, simulation, dataset, training-script, api-endpoint, governance, build-log)
- **Relationships**:
  - Associated with one Chapter entity
  - References multiple Resource entities

### Learning Resource
- **Attributes**:
  - id: string (unique identifier)
  - title: string (display title)
  - type: string (simulation, dataset, training script, build log, diagram, source reference, API documentation)
  - path: string (location of resource)
  - description: string (what the resource contains/does)
  - size: number (file size where applicable)
  - format: string (file format, e.g., python, markdown, json, pdf)
- **Relationships**:
  - Associated with one ReproducibilityCheckpoint entity

### Chatbot Response Context
- **Attributes**:
  - id: string (unique identifier)
  - chapterId: string (associated chapter)
  - contextScope: string (glossary, component, motion, perception, algorithm, dialogue, policy, capstone)
  - knowledgeSource: string (path to chapter content for RAG)
  - responseTemplates: array of strings (patterns for responses)
  - accuracyRate: number (measured accuracy of responses)
- **Relationships**:
  - Associated with one Chapter entity

### User Query
- **Attributes**:
  - id: string (unique identifier)
  - userId: string (user identifier)
  - queryText: string (original query text)
  - timestamp: date (when query was made)
  - sourceChapter: string (chapter context if applicable)
  - isRelevant: boolean (whether query is relevant to course content)
  - responseId: string (ID of response provided)
- **Relationships**:
  - Associated with one ChatbotResponse entity

### Chatbot Response
- **Attributes**:
  - id: string (unique identifier)
  - queryId: string (associated query)
  - responseText: string (generated response text)
  - sources: array of strings (citations from course content)
  - confidenceScore: number (confidence in response accuracy)
  - timestamp: date (when response was generated)
  - isAccurate: boolean (accuracy verified by system or human)
- **Relationships**:
  - Associated with one UserQuery entity
  - References multiple CourseChapter entities (if multi-chapter response)

## Relationships

1. One Course Chapter contains many Subchapters
2. One Course Chapter has many Reproducibility Checkpoints
3. One Reproducibility Checkpoint references many Learning Resources
4. One Course Chapter has one Chatbot Response Context
5. One User Query generates one Chatbot Response
6. One Chatbot Response may reference multiple Course Chapters

## Constraints

- Each Chapter must have at least one Subchapter
- Each Chapter must have at least one Reproducibility Checkpoint
- Chapter word count must be minimum 2000 words
- Subchapter word count must be minimum 300 words
- All resources referenced in reproducibility checkpoints must exist
- Chatbot responses must be grounded in course content (no external information)
- Chatbot response accuracy must be >= 95% when measured against course content
- Reproducibility checkpoints must be validated before chapter publication

## Indexes

### Performance indexes needed:
- Chapter.id for fast chapter lookup
- ReproducibilityCheckpoint.chapterId for checkpoint retrieval
- UserQuery.timestamp for query analysis
- ChatbotResponse.queryId for response tracking

### Search indexes needed:
- Full-text index on Chapter.content for search functionality
- Full-text index on ChatbotResponse.responseText for response analysis
- Full-text index on UserQuery.queryText for query pattern analysis

## Validation Rules

1. **Content Validation**: All chapter content must pass plagiarism checks and citation verification
2. **Link Validation**: All internal links must be valid and point to existing resources
3. **Reproducibility Validation**: All reproducibility checkpoints must be testable and verifiable
4. **Chatbot Validation**: Responses must cite specific course content and not introduce external information
5. **User Access Validation**: Ensure proper authentication and authorization for any user-specific functionality