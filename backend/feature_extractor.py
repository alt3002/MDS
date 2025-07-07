import os
import math
import string

def compute_entropy(data):
    """
    Compute the Shannon entropy of the given byte data.
    """
    if not data:
        return 0
    entropy = 0
    length = len(data)
    for i in range(256):
        p_x = data.count(bytes([i])) / length
        if p_x > 0:
            entropy -= p_x * math.log(p_x, 2)
    return entropy

def extract_features(file_path):
    """
    Extract key features from the given file.

    Features extracted:
      1. File size in bytes.
      2. Shannon entropy of the entire file.
      3. Ratio of printable characters to total bytes.
      4. Average byte value in the first 100 bytes.
    """
    # Ensure we have an absolute file path
    abs_path = os.path.abspath(file_path)
    
    # Feature 1: File size
    try:
        file_size = os.path.getsize(abs_path)
    except Exception as e:
        print("Error getting file size:", e)
        file_size = 0

    # Read file data in binary mode
    try:
        with open(abs_path, 'rb') as f:
            data = f.read()
    except Exception as e:
        print("Error reading file:", e)
        data = b""

    # Feature 2: Shannon entropy of the file data
    file_entropy = compute_entropy(data)
    
    # Feature 3: Ratio of printable characters in the file
    printable = set(bytes(string.printable, 'utf-8'))
    total_bytes = len(data)
    if total_bytes > 0:
        printable_count = sum(1 for b in data if b in printable)
        ratio_printable = printable_count / total_bytes
    else:
        ratio_printable = 0

    # Feature 4: Average byte value of the first 100 bytes
    first_100 = data[:100]
    if first_100:
        avg_first_100 = sum(first_100) / len(first_100)
    else:
        avg_first_100 = 0

    # Construct and return the feature vector
    features = [file_size, file_entropy, ratio_printable, avg_first_100]
    return features

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python feature_extractor.py <filename>")
        sys.exit(1)
    
    # Here we assume the file was uploaded into the 'uploads' folder.
    # Construct the file path as done in the Flask app:
    filename = sys.argv[1]
    file_path = os.path.join(os.getcwd(), 'uploads', filename)
    
    features = extract_features(file_path)
    print("Extracted features:", features)
