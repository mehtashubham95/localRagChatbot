import traceback

def load_prompt_template(template_path='prompt_template.txt'):
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def retrieve_relevant_chunks(query, embedder, index, chunks, top_k=5):
    query_embedding = embedder.embedder.encode([query])
    indices = index.search(query_embedding, top_k)
    return [chunks[i] for i in indices]

def chatbot_fn(user_query, embedder, index, all_chunks, ask_ollama, prompt_template_path='prompt_template.txt'):
    try:
        relevant_chunks = retrieve_relevant_chunks(user_query, embedder, index, all_chunks, top_k=2)
        context = "\n".join(relevant_chunks)

        # Load prompt template from file
        prompt_template = load_prompt_template(prompt_template_path)

        # Construct final prompt exactly as requested
        final_prompt = (
            f"{prompt_template}\n\n"
            f"\n{context}\n\n"
            f"{user_query}"
        )

        answer = ask_ollama(final_prompt, model='llama3')
        return answer
    except Exception as e:
        print(traceback.format_exc())
        return f"Error: {str(e)}"