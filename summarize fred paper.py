import pdfplumber
import requests
from transformers import pipeline

# Function to download the PDF from a URL
def download_pdf(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Function to summarize text using Hugging Face's transformers
def summarize_text(text):
    summarizer = pipeline("summarization")
    # Split text into chunks to avoid exceeding model limits
    text_chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]  # Adjust chunk size as needed
    summaries = summarizer(text_chunks, max_length=150, min_length=40, do_sample=False)
    return "\n".join([summary['summary_text'] for summary in summaries])

# Function to save summary to a text file
def save_summary_to_file(summary, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(summary)

# Main execution
if __name__ == "__main__":
    # Define the PDF URL and file paths
    pdf_url = "https://s3.amazonaws.com/real.stlouisfed.org/wp/2024/2024-031.pdf"
    pdf_file_path = "paper.pdf"
    summary_file_path = "summary.txt"

    # Download the PDF
    download_pdf(pdf_url, pdf_file_path)

    # Extract text from the PDF
    pdf_text = extract_text_from_pdf(pdf_file_path)

    # Summarize the extracted text
    summary = summarize_text(pdf_text)

    # Save the summary to a text file
    save_summary_to_file(summary, summary_file_path)

    print("Summary saved to", summary_file_path)
