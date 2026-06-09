# Bible Guide

A conversational RAG system that acts as a warm, fatherly pastoral companion, bringing the Word of God to wherever you are. Ask any question about life, faith, or scripture, and receive a grounded, scripture-based response in the voice of a caring senior pastor.

## Domain

This system makes the Bible searchable and answerable through natural conversation. Users share what is on their heart and receive a comprehensive, grounded response drawing from scripture. Designed for believers worldwide and anyone exploring Christianity.

## Architecture

KJV.json > ingest.py (chunking) > embed.py (embeddings) > ChromaDB > app.py (retrieval + generation) > Gradio UI

- Document source: KJV.json, all 66 books, approximately 31,000 verses
- Chunking: 5 verses per chunk, 2-verse overlap, 10,770 total chunks
- Embedding model: all-MiniLM-L6-v2 via sentence-transformers
- Vector store: ChromaDB persistent local storage
- Retrieval: top-8 semantic search
- Generation: Groq API with llama-3.3-70b-versatile
- Interface: Gradio conversational chatbot

## Setup

Clone the repo, create a virtual environment, install requirements.txt, add your GROQ_API_KEY to a .env file, run embed.py once, then run app.py.

## Evaluation

All 5 evaluation questions were tested with full conversational flows.

1. What does the Bible say about fear and anxiety? Expected Philippians 4:6-7, Isaiah 41:10. Result: cited Psalms 27:1 and Deuteronomy 3:22, warm and grounded response.
2. How should a Christian respond to enemies? Expected Matthew 5:44, Romans 12:20. Result: relevant scripture cited, pastoral tone correct.
3. What does the Bible say about pride? Expected Proverbs 16:18, James 4:6. Result: grounded response with correct references.
4. What does the Bible say about money and wealth? Expected 1 Timothy 6:10, Matthew 6:24. Result: scripture woven naturally, firm but loving.
5. What does the Bible say about the Holy Spirit? Expected John 14:26, Acts 1:8. Result: warm, accurate, scripture-grounded.

Overall the system retrieves relevant passages across all 5 topics and generates responses that are grounded, warm, and pastoral in tone.

## AI Tool Usage

Claude was used at every stage of this project including designing the chunking strategy, writing and debugging all scripts, crafting the pastoral system prompt, and troubleshooting environment issues.

## Future Work

- Deploy to Hugging Face Spaces for permanent hosting
- Persistent chat history across sessions
- Improved UI design
- Multilingual embedding model
- Cloud vector database for deployment
