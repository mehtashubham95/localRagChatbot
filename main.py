import os
import numpy as np
import gradio as gr

from extractor import extract_texts_from_folder, chunk_text
from embedder import TextEmbedder
from search import FaissIndex
from chatbot import chatbot_fn
from utils import ask_ollama

def main():
    folder_path = 'info'  # Change this to your folder path

    embedder = TextEmbedder()

    # Load cached embeddings and chunks if available
    chunk_embeddings, all_chunks = embedder.load_embeddings()

    if chunk_embeddings is None or all_chunks is None:
        # Extract and chunk texts
        all_brochure_texts = extract_texts_from_folder(folder_path)
        all_chunks = []
        for brochure_text in all_brochure_texts:
            all_chunks.extend(chunk_text(brochure_text))

        # Embed chunks
        chunk_embeddings = embedder.embed_chunks(all_chunks)

        # Save for future use
        embedder.save_embeddings(chunk_embeddings, all_chunks)

    # Build FAISS index
    dimension = chunk_embeddings.shape[1]
    index = FaissIndex(dimension)
    index.add_embeddings(chunk_embeddings)

    def gradio_chatbot(user_query):
        return chatbot_fn(user_query, embedder, index, all_chunks, ask_ollama)

    iface = gr.Interface(
        fn=gradio_chatbot,
        inputs=gr.Textbox(lines=2, placeholder="Ask a question about your bank statements"),
        outputs="text",
        title="Personal Financial Assistant"
    )

    iface.launch()

if __name__ == "__main__":
    main()