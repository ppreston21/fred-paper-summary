# St. Louis Federal Reserve Paper Summarization

### 
The St. Louis Fed runs the Federal Reserve Economic Data (FRED), which from time-to-time publishes economic papers of incredible density, but valuable insight. Rather than reading these 60+ page reports, leverage these scripts to:

1) Comb the FRED site for the latest research papers.
2) Summarizes thoses research papers.
3) Further summarizes the ~5000 output with a local transformer.

**fred report 2.py** - combs the FRED site for the three latest papers and returns their URLs.

**summarize fred paper.py** - summarizes the pdf file of the paper URL you have selected.

**real summarizer 2.py** - This Python script reads a `.txt` file, summarizes its content using the Hugging Face `transformers` library, and then saves the summarized text as a PDF file. The summarization process is done in chunks to handle larger text files effectively. By default, the script uses a pre-trained model from Hugging Face (`sshleifer/distilbart-cnn-12-6`) to generate summaries. You can customize the model if needed.

The script reads the input text from a specified `.txt` file. Large text files are split into manageable chunks (default: 1024 characters). Each chunk is summarized using the Hugging Face `pipeline` summarizer. The summarized chunks are combined and then further summarized for a concise final output. The final summary is saved as a PDF file (`final_summary.pdf`). 

Replace `'path/to/your/textfile.txt'` with the actual path to your text file. Run the script using Python. After the script runs, a PDF file named `final_summary.pdf` will be generated in the same directory as the script.
