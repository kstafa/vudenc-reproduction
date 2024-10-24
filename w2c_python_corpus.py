from pydriller import Repository

import os
import concurrent.futures   # For parallel processing

# List of repositories
repos = [
    "https://github.com/numpy/numpy", "https://github.com/django/django",
    "https://github.com/scikit-learn/scikit-learn", "https://github.com/tensorflow/tensorflow",
    "https://github.com/keras-team/keras", "https://github.com/ansible/ansible",
    "https://github.com/TheAlgorithms/Python", "https://github.com/pallets/flask",
    "https://github.com/ytdl-org/youtube-dl", "https://github.com/pandas-dev/pandas",
    "https://github.com/scrapy/scrapy", "https://github.com/kennethreitz/requests",
    "https://github.com/home-assistant/home-assistant", "https://github.com/ageitgey/face_recognition"
]

output_dir = 'w2v'
os.makedirs(output_dir, exist_ok=True)  

def process_repository(r): 
    print(f"Processing {r}")
    files = set()
    code_snippets = []
    try: 
        for commit in Repository(r).traverse_commits(): 
            for modification in commit.modified_files:
                if modification.filename and modification.filename.endswith('.py'): 
                    filename = modification.new_path or modification.old_path # handle both new and old paths
                    if filename and filename not in files: 
                        code = modification.source_code
                        if code: 
                            code_snippets += f"\n\n# File: {filename}\n\n{code}"
                            files.add(filename)
    except Exception as e:
        print(f"Error processing {r}: {e}")
    return code_snippets

# Process repositories in parallel
pythontraining = ""
with concurrent.futures.ThreadPoolExecutor() as executor: 
    results = executor.map(process_repository, repos)

    for result in results: 
        pythontraining += result

output_path = os.path.join(output_dir, 'pythontraining.txt')
with open(output_path, 'w', encoding='utf-8') as outfile: 
    outfile.write(pythontraining)
 
