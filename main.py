import fitz  # PyMuPDF for reading PDFs
import spacy
import re
from collections import defaultdict
import os

# Load spaCy's pre-trained model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    # Check if the PDF path exists
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return None

    # Attempt to open the PDF
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return None
    
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text

# Function to clean and preprocess the extracted text
def preprocess_text(text):
    # Remove excessive whitespace and unwanted characters
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = text.strip()
    return text

# Function to identify and extract sections of interest
def extract_key_information(text):
    sections = defaultdict(str)
    
    # Define keywords that may indicate relevant sections
    growth_keywords = ["future growth", "growth prospects", "next year", "forecast", "expected growth"]
    changes_keywords = ["key changes", "business changes", "restructure", "acquisition", "merger"]
    triggers_keywords = ["triggers", "drivers", "factors", "material impact", "impact on earnings"]
    
    # Define regex patterns to match key sections
    growth_pattern = '|'.join(growth_keywords)
    changes_pattern = '|'.join(changes_keywords)
    triggers_pattern = '|'.join(triggers_keywords)

    # Find sections related to future growth, business changes, and financial triggers
    growth_section = []
    changes_section = []
    triggers_section = []

    # Break the document into sentences
    sentences = text.split('. ')
    
    for sentence in sentences:
        # Check for sentences mentioning future growth prospects
        if re.search(growth_pattern, sentence, re.IGNORECASE):
            growth_section.append(sentence)
        
        # Check for sentences mentioning key changes
        if re.search(changes_pattern, sentence, re.IGNORECASE):
            changes_section.append(sentence)
        
        # Check for sentences mentioning key triggers
        if re.search(triggers_pattern, sentence, re.IGNORECASE):
            triggers_section.append(sentence)
    
    # Store the extracted sections, handling empty sections
    sections['Growth Prospects'] = ' '.join(growth_section) if growth_section else "No relevant information found."
    sections['Business Changes'] = ' '.join(changes_section) if changes_section else "No relevant information found."
    sections['Triggers for Earnings Growth'] = ' '.join(triggers_section) if triggers_section else "No relevant information found."

    return sections

# Function to summarize the extracted information
def summarize_information(sections):
    summary = {}
    for key, content in sections.items():
        # Apply spaCy NLP to extract entities and important keywords
        doc = nlp(content)
        entities = [ent.text for ent in doc.ents]
        summary[key] = {
            'text': content,
            'entities': entities
        }
    return summary

# Main function to process the PDF
def analyze_pdf_for_investor(pdf_path):
    # Step 1: Extract text from the PDF
    text = extract_text_from_pdf(pdf_path)
    if text is None:
        return None  # Exit if there was an error opening the PDF
    
    # Step 2: Preprocess the text
    cleaned_text = preprocess_text(text)
    
    # Step 3: Extract key information related to growth, business changes, and earnings triggers
    key_info = extract_key_information(cleaned_text)
    
    # Step 4: Summarize key insights from the extracted information
    summary = summarize_information(key_info)
    
    return summary

# Example usage
pdf_path = "path_to_pdf_file.pdf"
summary = analyze_pdf_for_investor(pdf_path)

# Output the summary if it's not None
if summary:
    for section, details in summary.items():
        print(f"Section: {section}")
        print(f"Extracted Text: {details['text']}")
        print(f"Entities: {', '.join(details['entities'])}")
        print("-" * 50
