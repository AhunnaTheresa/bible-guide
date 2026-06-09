## Domain
This system makes the Bible's perspective on any topic searchable and answerable. Rather than relying on whoever can recall the most verses from memory, users can ask plain-language questions like "what does the Bible say about forgiveness?" or "how should a Christian handle conflict?" and receive a comprehensive, grounded response that draws together everything scripture says on that matter. It is designed for believers worldwide and anyone exploring Christianity. The problem it solves is that the Bible's 31,000 verses are spread across 66 books. Getting a complete picture on any topic requires encyclopedic knowledge of all of them and the ability to connect related ones instantly. Most people do not have that, and no single website offers it in a conversational, cited format.

## Documents
- Source: KJV.json (King James Version, 1769) downloaded from github.com/scrollmapper/bible_databases
- Format: JSON structured as book > chapter > verse with full text
- Coverage: All 66 books of the Bible, both Old and New Testament, approximately 31,000 verses
- Each book will be treated as a separate document during ingestion, giving 66 named sources for citation purposes
- No web scraping was required as the full Bible text is available in a clean, structured JSON format

## Chunking Strategy
- Chunk size: 5 verses per chunk
- Overlap: 2 verses shared between adjacent chunks
- Why 5 verses: A single verse is often too short to carry standalone meaning. Groups of 5 verses provide enough context for the embedding model to capture the topic being discussed while remaining specific enough to match precise queries.
- Why 2 verse overlap: Some passages build arguments across verse boundaries. The overlap ensures that if a key idea starts in one chunk and continues into the next, at least one chunk captures the full thought. This directly addresses the risk of splitting connected ideas across chunk boundaries.
- Why not whole chapters: Chapters in books like Psalms or Romans can be hundreds of words long and cover multiple sub-topics. A chunk that large would produce a weak, diluted embedding that matches too many queries loosely rather than matching the right query precisely.
- Expected chunk count: approximately 6,000 to 8,000 chunks across all 66 books

## Retrieval Approach
- Embedding model: all-MiniLM-L6-v2 via sentence-transformers (runs locally, no API key needed)
- Vector store: ChromaDB (runs locally, no account needed)
- Top-k: 8 chunks retrieved per query
- Why top-8: Enough to capture the Bible's perspective across multiple books while keeping the context focused. Too few risks missing relevant passages; too many dilutes the response with loosely related content.
- Why semantic search: A user asking "how do I deal with worry?" will not use the word "anxiety" but the embedding model understands they mean the same thing. Semantic search finds meaning-matches, not just word-matches.
- Production tradeoffs: For a production system, a multilingual embedding model would be worth considering since the Bible is read worldwide in many languages. A larger model like text-embedding-3-large would improve accuracy but at higher cost and latency.

## Evaluation Plan
1. Q: What does the Bible say about fear and anxiety? Expected: References to Philippians 4:6-7, Isaiah 41:10, Matthew 6:25-34, 1 Peter 5:7
2. Q: How should a Christian respond to enemies? Expected: References to Matthew 5:44, Romans 12:20, Luke 6:27-28
3. Q: What does the Bible say about pride? Expected: References to Proverbs 16:18, James 4:6, Proverbs 11:2
4. Q: What does the Bible say about money and wealth? Expected: References to 1 Timothy 6:10, Matthew 6:24, Proverbs 13:11, Luke 12:15
5. Q: What does the Bible say about the Holy Spirit? Expected: References to John 14:26, Acts 1:8, Galatians 5:22-23, Romans 8:26

## Anticipated Challenges
1. Verse-boundary splitting: Some theological arguments span multiple passages across different books. Chunking by verse groups may split a connected idea, causing retrieval to return only part of the argument. The 2-verse overlap is designed to reduce this risk but may not eliminate it entirely.
2. Figurative language: The Bible uses heavy metaphor, poetry, and symbolism. A user asking about "light" may get chunks about literal light rather than spiritual light. The embedding model may struggle to distinguish these without additional context.

## AI Tool Plan
- Ingestion and chunking code: I will prompt Claude with my Documents and Chunking Strategy sections and ask it to implement a script that loads KJV.json, groups verses into chunks of 5 with 2-verse overlap, and attaches metadata (book name, chapter, verse range) to each chunk.
- Embedding and ChromaDB storage: I will prompt Claude with my Retrieval Approach section and pipeline diagram and ask it to implement the embedding step using all-MiniLM-L6-v2 and store chunks in ChromaDB with source metadata.
- Grounded generation: I will prompt Claude with my grounding requirement (answers from retrieved context only, with source citation) and ask it to implement the Groq API call and prompt template.
- Gradio interface: I will prompt Claude with the complete pipeline and ask it to wire everything into a Gradio interface with a question input, answer output, and sources display.

## Architecture
Document Ingestion (KJV.json) -> Chunking (5 verses, 2 overlap) -> Embedding (all-MiniLM-L6-v2) -> Vector Store (ChromaDB) -> Retrieval (top-8 semantic search) -> Generation (Groq LLaMA) -> Response with citations
