import os 
import tokenize 

def process_file(mode="withString"): 
    input_file = 'w2v/pythontraining_edit.py' 
    output_dir = 'w2v'
    os.makedirs(output_dir, exist_ok=True)

    # Total size for progess reporting 
    total_size = os.path.getsize(input_file)    

    # Open the input file
    with open(input_file, 'rb') as f: 
        pythondata = ""
        count = 0 
        comment = 0 
        part = 0 

        bytes_processed = 0 

        # Tokenize the file 
        tokens = tokenize.tokenize(f.readline)
        for token in tokens: 
            toknum = token.type
            tokval = token.string

            # Update progress
            bytes_processed = f.tell()
            progress_percent = (bytes_processed / total_size) * 100

            if count % 100000 == 0: 
                print(f"Progress: {progress_percent:.2f}%")

            count += 1

            # skip encoding token 

            if toknum == tokenize.ENCODING: 
                continue

            # Skip comments
            if toknum == tokenize.COMMENT or (toknum == tokenize.STRING and '"""' in tokval): 
                comment += 1 
                continue

            # handle mode for strings 
            if mode == "withString" and toknum == tokenize.STRING: 
                tokval = '"string"'

            if toknum in (tokenize.NL, tokenize.NEWLINE): 
                pythondata += "\n"

            elif toknum == tokenize.INDENT: 
                pythondata += tokval

            elif toknum == tokenize.DEDENT:
                # no action if only removing indendts
                pass

            else:   
                pythondata += " " + tokval

            # save file periodically to reduce memory usage

            if count % 1000000 == 0:
                print(f"Saving part {part} ({mode})...")
                output_path = os.path.join(output_dir, f'pythontraining_{mode}_{part}.txt')
                with open(output_path, 'a', encoding='utf-8') as outfile: 
                    outfile.write(pythondata)
                pythondata = ""
                part += 1

        # Save the last part
        output_path = os.path.join(output_dir, f'pythontraining_{mode}_{part}.txt')
        with open(output_path, 'a', encoding='utf-8') as outfile: 
            outfile.write(pythondata)

        print(f"Processing complete. {count} tokens processed, {comment} comments skipped.")


            