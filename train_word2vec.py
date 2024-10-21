import os
import sys
import nltk
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from gensim.utils import tokenize
from nltk.tokenize import sent_tokenize
from tqdm import tqdm

def prepare_corpus_in_chunks(input_file, output_file, chunk_size=10 * 1024 * 1024):
    """
    Reads the input file in chunks, tokenizes the text, and writes the processed sentences to an output file.
    Each line in the output file corresponds to a tokenized sentence.
    """
    print("Preparing corpus in chunks...")
    total_size = os.path.getsize(input_file)
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        pbar = tqdm(total=total_size, unit_scale=True, unit_divisor=1024, unit='B')
        while True:
            chunk = infile.read(chunk_size)
            if not chunk:
                break
            # Ensure we don't split a sentence in half
            if not chunk.endswith('\n'):
                remainder = infile.readline()
                chunk += remainder
            sentences = sent_tokenize(chunk)
            for sentence in sentences:
                tokens = list(tokenize(sentence, lowercase=True, deacc=False))
                if tokens:  # Avoid writing empty lines
                    outfile.write(' '.join(tokens) + '\n')
            pbar.update(len(chunk.encode('utf-8')))
        pbar.close()
    print(f"Corpus prepared and saved to {output_file}")

def main():
    mode = "withString"  # default mode
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
    # Paths
    pythontraining_file = f'w2v/pythontraining_{mode}_X'
    corpus_file = f'data/pythontraining_{mode}_corpus.txt'

    # Ensure necessary directories exist
    os.makedirs('w2v', exist_ok=True)
    os.makedirs('data', exist_ok=True)

    # Prepare the corpus if it doesn't exist
    if not os.path.isfile(corpus_file):
        prepare_corpus_in_chunks(pythontraining_file, corpus_file)
    else:
        print(f"Corpus file {corpus_file} already exists. Skipping corpus preparation.")

    # Use gensim's LineSentence to read the corpus from the file without loading into memory
    sentences = LineSentence(corpus_file)

    # Trying out different parameters
    for mincount in [10, 30, 50, 100, 300, 500, 5000]:
        for epochs in [1, 5, 10, 30, 50, 100]:
            for s in [5, 10, 15, 30, 50, 75, 100, 200, 300]:

                print(f"\n\n{mode} W2V model with min count {mincount}, {epochs} epochs, and size {s}")
                fname = f"w2v/word2vec_{mode}{mincount}-{epochs}-{s}.model"

                if os.path.isfile(fname):
                    print("Model already exists.")
                    continue
                else:
                    print("Calculating model...")
                    # Training the model using LineSentence
                    model = Word2Vec(
                        sentences=sentences,
                        vector_size=s,
                        min_count=mincount,
                        epochs=epochs,
                        workers=4
                    )
                    # Saving the model
                    model.save(fname)
                    print(f"Model saved to {fname}")

if __name__ == "__main__":
    # Ensure NLTK punkt tokenizer is available
    nltk.download('punkt', quiet=True)
    main()
