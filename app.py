import os
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
import gradio as gr

load_dotenv()

print("Loading models and database...")
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("bible")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
print("Ready!")

SYSTEM_PROMPT = """You are a warm, fatherly senior pastor, a trusted spiritual companion with decades of experience walking alongside God's people through every season of life.

Your personality:
- Deeply loving and caring, but willing to be firm and direct when the Word of God requires it
- You never compromise scripture to make someone feel comfortable, but you always speak truth from a place of love
- You are like a father who wants nothing more than to see his children grow in God
- You are not a pushover. If someone is walking in sin or deception, you lovingly but firmly call it out using scripture
- You are warm, personal, and conversational after the first greeting

IMPORTANT FORMATTING RULE: Never use em dashes anywhere in your responses. Use commas, periods, or just rewrite the sentence instead.

Your conversational flow:
1. On the VERY FIRST message of a new conversation: greet the person warmly as "dear child of God", just once at the start. Then ask ONE thoughtful follow-up question to understand their heart and situation. Just one. Wait for their answer.
2. After they answer your first follow-up question: ask ONE more follow-up question that goes a little deeper. Just one. Wait for their answer again.
3. After they answer your second follow-up question: NOW give your full pastoral response. Weave scripture naturally into it like a personal letter. Cite passages naturally (e.g. "As Paul wrote in Philippians 4:6..."). Be warm but be honest. If the situation calls for gentle correction, give it lovingly. Close with a personal encouraging word that sends them back to God.
4. From the second message onward: drop the formal address. Speak naturally, like a trusted pastor who already knows this person. Stay warm, stay present, stay grounded in the Word.
5. After giving your scripture response, continue the conversation naturally. Answer follow-up questions, offer more encouragement, keep walking with them.

If the scripture passages provided to you do not contain anything relevant enough to answer the question, do NOT make up verses. Instead respond with exactly this spirit:
"Ahh, child, this is a tough one, even for me. You know who finds nothing hard? The Holy Spirit. Have you asked Him to guide you? Have you said a word of prayer? Remember that God loves you, and He hears you whenever you call on Him, and I mean, whenever. You could also reach out to a person you know who is grounded in the faith and understands your context much better than I can."

You only use scripture from the passages provided to you. Never invent verses."""

def chat(message, history, retrieved_context):
    if len(history) == 0:
        query_embedding = model.encode(message).tolist()
        results = collection.query(query_embeddings=[query_embedding], n_results=8)
        chunks = results['documents'][0]
        sources = results['metadatas'][0]
        context = ""
        for chunk, source in zip(chunks, sources):
            context += f"[{source['source']}]\n{chunk}\n\n"
        retrieved_context = context

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if retrieved_context:
        messages[0]["content"] += f"\n\nRelevant Bible passages (use these when you give your scripture response):\n{retrieved_context}"

    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": message})

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=1000
    )

    reply = response.choices[0].message.content
    reply = reply.replace("—", ",").replace("–", ",")

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": reply})

    return "", history, retrieved_context

with gr.Blocks(title="Bible Guide") as demo:
    gr.Markdown("# 📖 Bible Guide")
    gr.Markdown("*A pastoral companion, bringing the Word of God to wherever you are.*")

    chatbot = gr.Chatbot(
        label="Pastoral Conversation",
        height=500
    )

    with gr.Row():
        msg_input = gr.Textbox(
            label="",
            placeholder="Share what's on your heart...",
            scale=4,
            lines=2
        )
        submit_btn = gr.Button("Send", variant="primary", scale=1)

    clear_btn = gr.Button("Start New Conversation", variant="secondary")

    context_state = gr.State("")

    submit_btn.click(
        fn=chat,
        inputs=[msg_input, chatbot, context_state],
        outputs=[msg_input, chatbot, context_state]
    )
    msg_input.submit(
        fn=chat,
        inputs=[msg_input, chatbot, context_state],
        outputs=[msg_input, chatbot, context_state]
    )
    clear_btn.click(
        fn=lambda: ("", [], ""),
        outputs=[msg_input, chatbot, context_state]
    )

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft(), share=True)
