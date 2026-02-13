# neural-ir

Semantic search engine that retrieves anime title based on synopsis similarity rather than just key words. it turns plot synopsis into high-dmensional vectors to find the most similar across a database scraped from MyAnimeList 

![query_screenshot](./docs/query-ir.png)
![manhwa_info_screenshot](./docs/info-ir.png)
---

##  Features

- **Semantic Querying** – Find anime by describing a plot point rather than exact title and similar genre
- **Deep Embedding Pipeline** – Utilizes sentence transformer models to encode text into dense vector representations.
- **Automated Data Pipeline** – End-to-end flow from MAL scraping to MongoDB storage and vectorization.

---

##  Architecture Overview

### System Flow

1. **Ingestion**: Scrapes anime metadata and synopses from MyAnimeList
2. **Normalization & validation**: Cleans and pre-processes text for the model.
3. **Embedding**: Passes synopses through a Neural Network to generate numerical embeddings.
4. **Storage**: Persists metadata in MongoDB and vectors in a specialized search index.
5. **Retrieval**: User queries are embedded in real-time and compared against the database using Cosine Similarity.
6. **Delivery**: Returns the top *k* most relevant matches via a FastAPI endpoint.

---

##  Tech Stack

**Backend**
- **Python (Flask)** – A lightweight WSGI micro-framework focused on rapid development and simplicity.
- **Sentence-Transformers** – For generating high-quality embeddings.
- **MongoDB** – Scalable NoSQL storage for anime metadata and synopses.

**Frontend**
- **React / TypeScript** – Modern UI for a responsive search experience.

**Data Engineering Tools**
- **Pydantic** – Strict data validation and settings management

---


##  Project Structure
<pre>
```
backend/
├── app
│   ├── api
│   │   └── routes
│   │       ├── manhwa.py                    # REST endpoints for manhwa CRUD / retrieval
│   │       └── search.py                    # REST endpoints for keyword/vector search
│
│   ├── db
│   │   ├── mongo.py                         # MongoDB connection setup + client/session management
│   │   └── repository.py                    # Data access layer (DB abstraction, CRUD ops)
│
│   ├── models
│   │   ├── embedding.py                     # Pydantic/Schema model for stored vector embeddings
│   │   ├── manhwa.py                        # Data model for manhwa entity (DB + API schema)
│   │   ├── search.py                        # Search request schema (query payload model)
│   │   └── search_result.py                 # Structured search response model
│
│   ├── pipelines
│   │   ├── embed_pipeline.py                # Pipeline to generate embeddings from text data
│   │   ├── ingest_pipeline.py               # Full ingestion flow: scrape → clean → store → embed
│   │   └── sync_pipeline.py                 # Sync logic to detect changes & update DB/embeddings
│
│   ├── services
│   │   ├── embedding_service.py             # Handles embedding model calls (OpenAI/local model)
│   │   ├── error_log_service.py             # Centralized error logging to DB/file
│   │   ├── manhwa_service.py                # Business logic for manhwa operations
│   │   ├── search_service.py                # Hybrid search logic (keyword + vector similarity)
│   │   └── sync_service.py                  # Orchestrates synchronization workflow
│
│   ├── tests
│   │   ├── test_scrapper.py                 # Tests for scraping logic correctness
│   │   └── test_vector_search.py            # Tests for vector similarity search accuracy
│
│   ├── utils
│   │   ├── embed_query.py                   # Helper to embed user search queries
│   │   ├── find_changes.py                  # Detect diffs between stored and scraped data
│   │   ├── format_search_result.py          # Post-process search output for API response
│   │   ├── hash_text.py                     # Hashing utility for content change detection
│   │   ├── normalize_manhwa_data.py         # Clean & standardize scraped manhwa metadata
│   │   ├── normalize_manhwa_vector.py       # Preprocess text before vectorization
│   │   └── text_cleaner.py                  # General text sanitization utilities
│
│   ├── config.py                            # App configuration (env vars, constants)
│   └── main.py                              # FastAPI app entry point
│
├── scraper
│   └── mal_scraper.py                       # Scraper for MyAnimeList manhwa data
│
├── scripts
│   ├── create_vector_index.py               # Script to create MongoDB vector search index
│   ├── ingest_all.py                        # CLI script to ingest full dataset
│   └── sync_mal.py                          # CLI script to sync updates from MAL
│
├── .gitignore                               # Git ignore rules
├── README.md                                # Project documentation
└── requirements.txt                         # Python dependencies

frontend/
├── src
│
│   ├── context
│   │   └── ResultContext.tsx                # Defines the React context contract for search results state.
│   │                                        # Pure state interface — no UI, no API calls.
│
│   ├── domain
│   │   └── manhwa
│   │       ├── Manhwa.ts                    # Core domain entity type representing a full Manhwa.
│   │       │                                # Mirrors backend detail model.
│   │       │
│   │       └── VectorSearchMeta.ts          # Domain type for vector search metadata.
│   │                                        # Represents ranked similarity result shape.
│
│   ├── feature
│   │   ├── manhwa
│   │   │   ├── DisplayFulInfo
│   │   │   │   ├── DisplayFulInfo.css
│   │   │   │   └── DisplayFulInfo.tsx       # Renders full Manhwa detail view.
│   │   │   │                                # Presentation layer for detail page.
│   │   │   │
│   │   │   ├── ManhwaCard                   # Search result card container. Combines image + overlay + click behavior.
│   │   │   │   ├── ManhwaCard.css
│   │   │   │   └── ManhwaCard.tsx
│   │   │   │
│   │   │   └── SearchResultOverlay
│   │   │       ├── SearchResultOverlay.css
│   │   │       └── SearchResultOverlay.tsx
│   │   │                                    # Displays secondary search metadata (score, rank, badges).
│   │   │                                    # Pure visual overlay component.
│   │   │
│   │   └── search
│   │       ├── QueryPanel.css
│   │       ├── QueryPanel.tsx
│   │       │                                # Handles search input submission.
│   │       │                                # Triggers vector search service.
│   │       │
│   │       ├── ResultPanel.css
│   │       ├── ResultPanel.tsx
│   │       │                                # Renders list/grid of ManhwaCard.
│   │       │                                # Consumes search results from context.
│   │       │
│   │       └── types.ts                     # Feature-local types (e.g. form state, props, local DTOs).
│   │
│   ├── page
│   │   ├── ManhwaDetailPage.tsx
│   │   │                                    # Route-level container for /manhwa/:source/:source_id.
│   │   │                                    # Fetches detail data and passes to DisplayFulInfo.
│   │   │
│   │   └── SearchPage.tsx
│   │                                       # Route-level container for "/".
│   │                                       # Composes QueryPanel + ResultPanel.
│   │
│   ├── provider
│   │   └── ResultProvider.tsx               # Implements ResultContext state logic.
│   │                                        # Owns resultsVectorSearch state lifecycle.
│
│   ├── service
│   │   ├── tests
│   │   │   └── mockResults.ts               # Mock search results for development/testing.
│   │   │
│   │   ├── getManhwaDetail.ts               # API service function for fetching full Manhwa detail.
│   │   │
│   │   └── getSimilarManhwa.ts              # API service for vector similarity search.
│   │
│   ├── ui
│   │   ├── ContainerPanel                   # Generic layout wrapper component.
│   │   │   ├── ContainerPanel.css
│   │   │   └── ContainerPanel.tsx
│   │   │       
│   │   │
│   │   ├── CustomButton                     # Reusable styled button.
│   │   │   ├── CustomButton.css
│   │   │   └── CustomButton.tsx
│   │   │        
│   │   ├── CustomTextArea                   # Reusable styled textarea input.
│   │   │   ├── CustomTextArea.css
│   │   │   └── CustomTextArea.tsx        
│   │   │
│   │   └── ScoreCircle                      # Pure visual component for similarity score display.
│   │       ├── ScoreCircle.css
│   │       └── ScoreCircle.tsx
│   │         
│   ├── App.tsx                              # Route configuration only.
│   │                                        # Defines application navigation structure.
│   │
│   ├── config.ts                            # Centralized frontend configuration (API base URL, constants).
│   ├── index.css                            # Global application styles.
│   ├── main.tsx                             # React entry point. Mounts BrowserRouter + App.
│   └── vite-env.d.ts                        # Vite-specific TypeScript environment definitions.
│   
├── .env                                     # Environment variables (API base URL etc.)
├── vite.config.ts                           # Build & dev server configuration.
```
</pre>
