# =============================================================
# Filename: wordcount.py
# Description: Word Count using a custom MapReduce framework
# =============================================================
import os
import string

# --- MAPREDUCE FRAMEWORK DEFINITIONS ---

def mapper(text_chunk):
    """
    Map Phase:
    Input: A chunk of text (string).
    Output: A list of tuples (word, 1).
    """
    results = []
    # Normalize text: strip whitespace and convert to lowercase
    # Split text into individual words
    words = text_chunk.strip().lower().split()
    
    for word in words:
        # Remove punctuation marks (e.g., "hello," -> "hello")
        clean_word = word.strip(string.punctuation)
        if clean_word:
            results.append((clean_word, 1))
    return results

def reducer(word, counts_list):
    """
    Reduce Phase:
    Input: A word and a list of counts [1, 1, 1, ...].
    Output: A tuple (word, total_sum).
    """
    return word, sum(counts_list)

# --- DRIVER CODE ---

def run_mapreduce(filename):
    if not os.path.isfile(filename):
        print(f"[-] Error: File '{filename}' not found.")
        return

    print(f"[*] Reading file '{filename}'...")
    with open(filename, 'r', encoding='utf-8') as f:
        file_content = f.read()

    # --- STEP 1: MAP ---
    print("[*] Phase 1: Mapping...")
    # Process the text to get key-value pairs
    mapped_data = mapper(file_content)
    # mapped_data looks like: [('hello', 1), ('world', 1), ('hello', 1)...]
    print(f"    -> Generated {len(mapped_data)} pairs.")

    # --- STEP 2: SHUFFLE & SORT ---
    print("[*] Phase 2: Shuffling & Sorting...")
    shuffled_data = {}
    for word, count in mapped_data:
        if word not in shuffled_data:
            shuffled_data[word] = []
        shuffled_data[word].append(count)
    # shuffled_data looks like: {'hello': [1, 1], 'world': [1]}
    print(f"    -> Organized into {len(shuffled_data)} unique words.")

    # --- STEP 3: REDUCE ---
    print("[*] Phase 3: Reducing...")
    final_result = {}
    for word, counts_list in shuffled_data.items():
        _, total = reducer(word, counts_list)
        final_result[word] = total

    # --- OUTPUT RESULT ---
    print(f"\n[+] WORD COUNT RESULT:")
    print("-" * 30)
    # Sort results alphabetically for better readability
    for word in sorted(final_result.keys()):
        print(f"{word}: {final_result[word]}")
    print("-" * 30)

if __name__ == "__main__":
    # Create a dummy input file if it doesn't exist
    target_file = "input.txt"
    if not os.path.isfile(target_file):
        with open(target_file, "w", encoding="utf-8") as f:
            f.write("Hello world\nHello map reduce\nMap reduce is cool\nWorld count example")
            print(f"[*] Created sample file: {target_file}")

    run_mapreduce(target_file)