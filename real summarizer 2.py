from transformers import pipeline
import os
import time

# Specify the model explicitly
model_name = "sshleifer/distilbart-cnn-12-6"
summarizer = pipeline("summarization", model=model_name, clean_up_tokenization_spaces=True)


def summarize_text_file(file_path):
    print("Reading the file...")
    start_time = time.time()  # Start time measurement

    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    print("File read successfully. Length:", len(text))

    max_chunk_size = 1024  # Adjust this as necessary
    if len(text.split()) > max_chunk_size:
        print("Text is too long; splitting into chunks.")
        chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]
        print(f"Number of chunks created: {len(chunks)}")
        summaries = []

        for idx, chunk in enumerate(chunks):
            print(f"Summarizing chunk {idx + 1}/{len(chunks)}...")
            summaries.append(summarizer(chunk, max_length=130, min_length=30, do_sample=False))
            print("Chunk summarized.")

        # Combine all the summaries
        summary = ' '.join([s[0]['summary_text'] for s in summaries])
    else:
        print("Summarizing the entire text...")
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']

    end_time = time.time()  # End time measurement
    print(f"Summarization completed in {end_time - start_time:.2f} seconds.")

    return summary


if __name__ == "__main__":
    file_path = 'summary.txt'  # Replace with your actual file path
    if os.path.exists(file_path):
        summary = summarize_text_file(file_path)
        print("Summary:")
        print(summary)
    else:
        print("File not found.")
