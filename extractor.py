import os  
import pdfplumber  
  
def extract_texts_from_folder(folder_path):  
    all_texts = []  
    for filename in os.listdir(folder_path):  
        if filename.lower().endswith('.pdf'):  
            pdf_path = os.path.join(folder_path, filename)  
            with pdfplumber.open(pdf_path) as pdf:  
                text = ""  
                for page in pdf.pages:  
                    page_text = page.extract_text()  
                    if page_text:  
                        text += page_text + "\n"  
                all_texts.append(text)  
    return all_texts  
  
def chunk_text(text, max_length=500):  
    sentences = text.split('. ')  
    chunks = []  
    current_chunk = ""  
    for sentence in sentences:  
        if len(current_chunk) + len(sentence) < max_length:  
            current_chunk += sentence + ". "  
        else:  
            chunks.append(current_chunk.strip())  
            current_chunk = sentence + ". "  
    if current_chunk:  
        chunks.append(current_chunk.strip())  
    return chunks
