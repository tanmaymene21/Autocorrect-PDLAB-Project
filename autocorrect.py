import tkinter as tk
import re
from tkinter import filedialog
from textblob import TextBlob
from spellchecker import SpellChecker

# Initialize SpellChecker
spell = SpellChecker()

def correct_text_with_textblob(text):
    blob = TextBlob(text)
    return str(blob.correct())

def remove_punctuations(text):
    return re.sub(r'[^\w\s]', '', text)

def spell_check_with_spellchecker(text):
    s = re.sub(r'[^\w\s]', '', text)
    wordlist = s.split()
    misspelled = list(spell.unknown(wordlist))
    corrections = {}
    for word in misspelled:
        corrections[word] = spell.correction(word)
    return corrections

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, "r+") as file_handle:
            file_content = file_handle.read()
            original_text.delete(1.0, tk.END)
            original_text.insert(tk.END, file_content)

def process_text():
    text = original_text.get(1.0, tk.END)

    # Correct text with TextBlob
    corrected_text_blob = correct_text_with_textblob(text)
    corrected_text.delete(1.0, tk.END)
    corrected_text.insert(tk.END, corrected_text_blob)

    # Remove punctuations
    text_without_punctuations = remove_punctuations(text)
    text_without_punctuations_display.delete(1.0, tk.END)
    text_without_punctuations_display.insert(tk.END, text_without_punctuations)

    # Spell check with SpellChecker
    corrections = spell_check_with_spellchecker(text_without_punctuations)
    misspelled_words_display.delete(1.0, tk.END)
    misspelled_words_display.insert(tk.END, "\n".join(corrections.keys()))

    corrections_display.delete(1.0, tk.END)
    corrections_display.insert(tk.END, "\n".join([f"{word}: {corrections[word]}" for word in corrections]))

    # Finally, overwrite the text file with the corrected text
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file_handle:
            file_handle.write(corrected_text_blob)
# Set up Tkinter window
root = tk.Tk()
root.title("Text Correction Tool")

# Create and place widgets
original_text = tk.Text(root, height=10, width=50, wrap=tk.WORD)
original_text_label = tk.Label(root, text="Original Text:")
browse_button = tk.Button(root, text="Browse", command=browse_file)

process_button = tk.Button(root, text="Process Text", command=process_text)

corrected_text = tk.Text(root, height=10, width=50, wrap=tk.WORD)
corrected_text_label = tk.Label(root, text="Corrected Text:")

text_without_punctuations_display = tk.Text(root, height=5, width=50, wrap=tk.WORD)
text_without_punctuations_label = tk.Label(root, text="Text without Punctuations:")

misspelled_words_display = tk.Text(root, height=5, width=50, wrap=tk.WORD)
misspelled_words_label = tk.Label(root, text="Possible Misspelled Words:")

corrections_display = tk.Text(root, height=5, width=50, wrap=tk.WORD)
corrections_label = tk.Label(root, text="Corrections:")

# Place widgets in the grid
original_text_label.grid(row=0, column=0, pady=(10, 5), sticky="w")
original_text.grid(row=1, column=0, padx=(10, 5), pady=(0, 5), rowspan=2, columnspan=2, sticky="w")

browse_button.grid(row=3, column=0, padx=(10, 5), pady=(0, 10), sticky="w")

process_button.grid(row=4, column=0, padx=(10, 5), pady=(0, 10), sticky="w")

corrected_text_label.grid(row=0, column=3, pady=(10, 5), sticky="w")
corrected_text.grid(row=1, column=3, padx=(10, 5), pady=(0, 5), rowspan=2, columnspan=2, sticky="w")

text_without_punctuations_label.grid(row=3, column=3, pady=(10, 5), sticky="w")
text_without_punctuations_display.grid(row=4, column=3, padx=(10, 5), pady=(0, 5), sticky="w")

misspelled_words_label.grid(row=5, column=3, pady=(10, 5), sticky="w")
misspelled_words_display.grid(row=6, column=3, padx=(10, 5), pady=(0, 5), sticky="w")

corrections_label.grid(row=7, column=3, pady=(10, 5), sticky="w")
corrections_display.grid(row=8, column=3, padx=(10, 5), pady=(0, 5), sticky="w")

root.mainloop()
