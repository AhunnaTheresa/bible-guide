import json
import os

def load_and_chunk_bible(filepath, chunk_size=5, overlap=2):
    """
    Loads KJV.json and splits verses into overlapping chunks.
    Each chunk carries metadata: book, chapter, verse range.
    """
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    all_chunks = []
    
    for book in data['books']:
        book_name = book['name']
        
        for chapter in book['chapters']:
            chapter_num = chapter['chapter']
            verses = chapter['verses']
            
            step = chunk_size - overlap
            for i in range(0, len(verses), step):
                chunk_verses = verses[i:i + chunk_size]
                if len(chunk_verses) == 0:
                    continue
                
                text = ' '.join(v['text'] for v in chunk_verses)
                
                start_verse = chunk_verses[0]['verse']
                end_verse = chunk_verses[-1]['verse']
                
                all_chunks.append({
                    'text': text,
                    'book': book_name,
                    'chapter': chapter_num,
                    'start_verse': start_verse,
                    'end_verse': end_verse,
                    'source': f"{book_name} {chapter_num}:{start_verse}-{end_verse}"
                })
    
    return all_chunks

if __name__ == "__main__":
    chunks = load_and_chunk_bible('data/KJV.json')
    print(f"Total chunks created: {len(chunks)}")
    print("\nSample chunk 1:")
    print(f"Source: {chunks[0]['source']}")
    print(f"Text: {chunks[0]['text'][:200]}")
    print("\nSample chunk 100:")
    print(f"Source: {chunks[100]['source']}")
    print(f"Text: {chunks[100]['text'][:200]}")
