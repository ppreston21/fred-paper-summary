import requests
from bs4 import BeautifulSoup
from io import BytesIO
import PyPDF2
from fpdf import FPDF

# Step 1: Function to scrape the St. Louis Fed working papers website
def scrape_fred_working_papers():
    url = "https://research.stlouisfed.org/wp/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the first 10 links with class="title"
    articles = soup.find_all('a', class_='title', limit=3)

    article_links = []
    for article in articles:
        article_title = article.text.strip()
        article_url = article['href']
        article_links.append((article_title, article_url))

    return article_links

# Step 2: Function to find the PDF link inside each article page
def find_pdf_link(article_url):
    base_url = "https://research.stlouisfed.org"
    full_url = base_url + article_url  # Append the base URL to the relative URL
    response = requests.get(full_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the first PDF link in the article
    for link in soup.find_all('a', href=True):
        if link['href'].endswith('.pdf'):
            return link['href'] if link['href'].startswith('http') else base_url + link['href']

    return None

# Step 3: Function to extract text from a PDF
def extract_text_from_pdf(pdf_url):
    response = requests.get(pdf_url)
    pdf_file = BytesIO(response.content)

    # Use PyPDF2 to extract text
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text() + '\n'

    return text

# Step 4: Function to summarize text using basic string operations
def summarize_text(text):
    # Split text into paragraphs
    paragraphs = text.split('\n')

    # Filter out empty paragraphs and take the first three non-empty paragraphs as a summary
    summary = [para for para in paragraphs if para.strip()][:3]

    return '\n'.join(summary)

# Step 5: Function to create a PDF of summaries
def create_summary_pdf(summaries):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for title, summary in summaries:
        # Replace unsupported characters
        title = title.replace('’', "'").replace('“', '"').replace('”', '"')
        summary = summary.replace('’', "'").replace('“', '"').replace('”', '"')

        pdf.cell(0, 10, title, ln=True, align='L')
        pdf.multi_cell(0, 10, summary)
        pdf.ln(5)

    pdf_file_path = "summaries.pdf"
    pdf.output(pdf_file_path)
    print(f"Summary PDF created: {pdf_file_path}")

# Main function
def main():
    article_links = scrape_fred_working_papers()

    # Print the article titles and URLs
    print("Retrieved Article Links:")
    for title, article_url in article_links:
        print(f"Title: {title}\nURL: {article_url}\n")

    summaries = []

    # Process each article to find the PDF link and summarize it
    for title, article_url in article_links:
        print(f"Processing: {title}")
        pdf_link = find_pdf_link(article_url)
        if pdf_link:
            print(f"PDF link found: {pdf_link}")
            pdf_text = extract_text_from_pdf(pdf_link)
            summary = summarize_text(pdf_text)
            summaries.append((title, summary))
        else:
            print(f"No PDF found for: {title}")

    # Create a PDF of the summaries
    create_summary_pdf(summaries)

if __name__ == "__main__":
    main()
