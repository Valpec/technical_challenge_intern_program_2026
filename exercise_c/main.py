import os
import re

def content_cleaner(content):
    """
    Cleans the input text content by removing special characters, 
    converting to lowercase, and collapsing multiple spaces.
    """
    if content is None:
        return ""
    # Convert to lowercase, remove special characters and extra spaces   
    content = str(content).lower()
    content = re.sub(r'[^a-z0-9áéíóúüñ\s]', '', content)
    content = ' '.join(content.split())
    return content

def detect_word_freq(content):
    """
    Detects and counts the frequency of each word in the cleaned content.
    """
    word_freq = {}
    # Split the content into words by whitespaces and count their frequencies 
    words = content.split()
    for word in words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1
    return word_freq

def main():
    # Input file path from the user
    input_file = input("Enter the path to the text file: ").strip()
    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        return
    if os.path.getsize(input_file) == 0:
        print(f"Error: The file '{input_file}' is empty.")
        return
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
            # Clean content from the file
            cleaned_content = content_cleaner(content)
            # Count the frequency of each word in the cleaned content (word_freq is a dictionary with word as key and frequency as value)
            word_freq = detect_word_freq(cleaned_content)
            sorted_list = sorted(word_freq.items(), key=lambda item: item[1], reverse=True)
            # Now we take the first 10 elements from the sorted list
            top_10_words = sorted_list[:10]

            # Print the 10 most common words and their frequencies
            print("\n" + "="*30)
            print(" TOP 10 MOST COMMON WORDS")
            print("="*30)
            print(f"{'WORD':<15} | {'FREQUENCY':<10}")
            print("-" * 30)
            for word, freq in top_10_words:
                print(f"{word:<15} | {freq:<10}")
            print("="*30)
            
    except Exception as e:
        print(f"Error reading the file: {e}")
        return
    
    word_freq = {}
    
    
if __name__ == "__main__":
    main()