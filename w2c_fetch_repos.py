from pydriller import Repository
import os
import concurrent.futures

# Directory for saving the corpus
output_dir = 'w2v'
os.makedirs(output_dir, exist_ok=True)

def process_repository(r):
    print(f"Processing repository: {r}")
    files = set()
    code_snippets = ""
    try:
        for commit in Repository(r).traverse_commits():
            for mod in commit.modified_files:
                if mod.filename and mod.filename.endswith(".py"):
                    filename = mod.new_path or mod.old_path  # Handle both new and old paths
                    if filename and filename not in files:
                        code = mod.source_code
                        if code:
                            code_snippets += f"\n\n# File: {filename}\n\n{code}"
                            files.add(filename)
                        # Remove 'break' if you want to process all modified files
    except Exception as e:
        print(f"Error processing repository {r}: {e}")
    return code_snippets

def fetch_repositories():
    # List of repositories
    repos = [
        "https://github.com/numpy/numpy",
        "https://github.com/django/django",
        "https://github.com/scikit-learn/scikit-learn",
        "https://github.com/tensorflow/tensorflow",
        "https://github.com/keras-team/keras",
        "https://github.com/ansible/ansible",
        "https://github.com/TheAlgorithms/Python",
        "https://github.com/pallets/flask",
        "https://github.com/ytdl-org/youtube-dl",
        "https://github.com/pandas-dev/pandas",
        "https://github.com/scrapy/scrapy",
        "https://github.com/psf/requests",
        "https://github.com/home-assistant/core",
        "https://github.com/ageitgey/face_recognition"
    ]

    # Use ThreadPoolExecutor to process repositories in parallel
    pythontraining = ""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(process_repository, repos)

        for result in results:
            pythontraining += result

    # Save the collected Python code to a file
    output_path = os.path.join(output_dir, 'pythontraining.txt')
    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(pythontraining)
    print(f"Python training data saved to {output_path}")
