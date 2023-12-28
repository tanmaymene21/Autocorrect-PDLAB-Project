import tkinter as tk
import re
from tkinter import filedialog
from textblob import TextBlob
from spellchecker import SpellChecker

# Initialize SpellChecker
spell = SpellChecker()

# TextBlob is a Python library that can be used to process textual data. It does Spelling Correction using natural language processing.
def useTextBlob(text):
    blob = TextBlob(text)
    return str(blob.correct())

# Removes the punctuations from the input text.
def removePunctuations(text):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    noPunctuations = ""
    
    for char in text:
        if char not in punctuations:
            noPunctuations += char
            
    return noPunctuations

def useSpellchecker(text):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    s = ""
    for char in text:
        if char not in punctuations:
            s += char
    
    wordlist = s.split()
    misspelled = list(spell.unknown(wordlist))
    corrections = {}
    for word in misspelled:
        corrections[word] = spell.correction(word)
    return corrections

def browseFile():
    filePath = filedialog.askopenfilename()
    if filePath:
        with open(filePath, "r+") as f:
            fileContent = f.read()
            originalText.delete(1.0, tk.END)
            originalText.insert(tk.END, fileContent)

def processText():
    text = originalText.get(1.0, tk.END)

    # Correct text with TextBlob
    correctedTextBlob = useTextBlob(text)
    correctedText.delete(1.0, tk.END)
    correctedText.insert(tk.END, correctedTextBlob)

    # Remove punctuations
    textWithoutPunctuation = removePunctuations(text)
    textWithoutPunctuationTextbox.delete(1.0, tk.END)
    textWithoutPunctuationTextbox.insert(tk.END, textWithoutPunctuation)

    # Spell check with SpellChecker
    corrections = useSpellchecker(textWithoutPunctuation)
    mispelledWordsTextbox.delete(1.0, tk.END)
    mispelledWordsTextbox.insert(tk.END, "\n".join(corrections.keys()))

    correctionsTextbox.delete(1.0, tk.END)
    correctionsTextbox.insert(tk.END, "\n".join([f"{word}: {corrections[word]}" for word in corrections]))

def askForSaving():
    # Finally, overwrite the text file with the corrected text
    filePath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    text = originalText.get(1.0, tk.END)
    correctedTextBlob = useTextBlob(text)
    if filePath:
        with open(filePath, "w") as f:
            f.write(correctedTextBlob)

# Set up Tkinter window
root = tk.Tk()
root.title("Text Correction Tool")

# Create and place widgets with color scheme
originalTextLabel = tk.Label(root, text="Original Text:", bg="#f0f0f0", fg="#333333").grid(row=0, column=0, pady=(10, 5), sticky="w")

originalText = tk.Text(root, height=7, width=80, wrap=tk.WORD, bg="#f0f0f0", fg="#333333")
originalText.grid(row=1, column=0, padx=(10, 5), pady=(0, 5), columnspan=3, sticky="w")

browseButton = tk.Button(root, text="Browse", command=browseFile, bg="#4CAF50", fg="white").grid(row=2, column=1, padx=(10, 5), pady=(0, 10), sticky="w")

correctedTextLabel = tk.Label(root, text="Corrected Text:", bg="#f0f0f0", fg="#333333").grid(row=3, column=0, pady=(10, 5), sticky="w")

correctedText = tk.Text(root, height=5, width=80, wrap=tk.WORD, bg="#f0f0f0", fg="#333333")
correctedText.grid(row=4, column=0, padx=(10, 5), pady=(0, 5), columnspan=3, sticky="w")

textWithoutPunctuationLabel = tk.Label(root, text="Text without Punctuations:", bg="#f0f0f0", fg="#333333").grid(row=5, column=0, pady=(10, 5), sticky="w")

textWithoutPunctuationTextbox = tk.Text(root, height=5, width=80, wrap=tk.WORD, bg="#f0f0f0", fg="#333333")
textWithoutPunctuationTextbox.grid(row=6, column=0, padx=(10, 5), pady=(0, 5), columnspan=3, sticky="w")

mispelledWordsLabel = tk.Label(root, text="Possible Misspelled Words:", bg="#f0f0f0", fg="#333333").grid(row=7, column=0, pady=(10, 5), sticky="w")

mispelledWordsTextbox = tk.Text(root, height=5, width=80, wrap=tk.WORD, bg="#f0f0f0", fg="#333333")
mispelledWordsTextbox.grid(row=8, column=0, padx=(10, 5), pady=(0, 5), columnspan=3, sticky="w")

correctionsLabel = tk.Label(root, text="Corrections:", bg="#f0f0f0", fg="#333333").grid(row=9, column=0, pady=(10, 5), sticky="w")

correctionsTextbox = tk.Text(root, height=5, width=80, wrap=tk.WORD, bg="#f0f0f0", fg="#333333")
correctionsTextbox.grid(row=10, column=0, padx=(10, 5), pady=(0, 5), columnspan=3, sticky="w")

processButton = tk.Button(root, text="Process Text", command=processText, bg="#4CAF50", fg="white").grid(row=11, column=1, padx=(10, 5), pady=(0, 10), sticky="w")

saveButton = tk.Button(root, text="Save Text", command=askForSaving, bg="#4CAF50", fg="white").grid(row=12, column=1, padx=(18, 5), pady=(0, 10), sticky="w")

root.mainloop()