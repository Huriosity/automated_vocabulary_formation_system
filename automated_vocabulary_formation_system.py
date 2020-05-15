import nltk
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
from collections import defaultdict
nltk.download('punkt')
from tkinter import ttk
import tkinter as tk
from tkinter import *
import json
import pickle
from tkinter import filedialog

#Create lemmatizer and stopwords list
mystem = Mystem()
russian_stopwords = stopwords.words("russian")
not_words = [',', '.', '!', '?', '-', '+', '=']
vocabulary = {}

def preprocess_text(text):
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords\
              and token != " " \
              and token.strip() not in punctuation \
              and token.strip() not in not_words]
    return tokens

def forms_of_words(text):
  forms = defaultdict(lambda: 0)
  print("Все слова: ")
  print(text)

  message = ""
  message = text.replace(')', '').replace('(', '').replace('.', '').replace('?', '').replace('!', '').replace(':', '').replace(',', '').replace('\n', '')


  print("теперь")
  print(message)

  tokens = nltk.word_tokenize(message)
  tokens.sort()
  for token in tokens:
    if not token in not_words:
      forms[token] += 1

  for form in forms:
    count = forms[form]
    forms[form] = [count, '']
  return forms

def get_lexems(text):
  tokens = preprocess_text(text)
  tokens.sort()
  lexems = defaultdict(lambda: 0)
  for token in tokens:
    if not token in not_words:
      lexems[token] += 1
  return lexems

def process_text():
  vocabulary['forms'] = {}
  vocabulary['lexems'] = {}
  input = text.get(1.0, END)
  forms = forms_of_words(input)
  lexems = get_lexems(input)
  vocabulary['forms'] = forms
  vocabulary['lexems'] = lexems
  for key, value in forms.items():
    tree.insert("", "end", text="%s" % key, values=('%s' % value[0], value[1]))
  
  for key, value in lexems.items():
    lexems_tree.insert("", "end", text="%s" % key, values=('%s' % value))

def add_note():
  text_field.pack()
  submit_button.pack()

def submit():
  notes = text_field.get(1.0, END)
  text_field.pack_forget()
  submit_button.pack_forget()

  item = tree.selection()
  value = tree.item(item)['values'][0]
  text = tree.item(item)['text']
  vocabulary['forms'][text][1] = notes
  tree.item(item, values=(value, notes))

def save_vocabulary():
  file_path = filedialog.asksaveasfilename()
  if file_path != '':
    f = open(file_path, "w")
    f.write(json.dumps(vocabulary))
    f.close()

def upload_vocabulary():
  file_path = filedialog.askopenfilename()
  if file_path != '':
    with open(file_path) as json_file:
      vocabulary = json.load(json_file)
    tree.delete(*tree.get_children())
    lexems_tree.delete(*lexems_tree.get_children())
    for key, value in vocabulary['forms'].items():
      tree.insert("", "end", text="%s" % key, values=('%s' % value[0], value[1]))
    for key, value in vocabulary['lexems'].items():
      lexems_tree.insert("", "end", text="%s" % key, values=('%s' % value))

def info():
    messagebox.askquestion("Help", "1. Введите текст.\n"
                                   "2. Нажмите кнопку 'Process'.\n", type='ok')

root = tk.Tk()


text = Text(width=55, height=15)
text.pack()

text_field = Text(width=25, height=5)
submit_button = Button(text='Add', command=submit)

frame = Frame()
frame.pack()

button = Button(frame, text="Process", command=process_text)
button.grid(row=1, column=0)

tree = ttk.Treeview()
tree.pack()

lexems_tree = ttk.Treeview()
lexems_tree.pack()

lexems_tree["columns"]=("one","two")

lexems_tree.heading("#0",text="Lexems",anchor=tk.W)
lexems_tree.heading("one", text="Count",anchor=tk.W)

add_note_button = Button(frame, text='Add note', command=add_note)
add_note_button.grid(row=1, column=1)

save_vocabulary_button = Button(frame, text='Save to file', command=save_vocabulary)
save_vocabulary_button.grid(row=1, column=2)

upload_from_file_button = Button(frame, text='Upload from file', command=upload_vocabulary)
upload_from_file_button.grid(row=1, column=3)
Button(text="info?", width=10, command=info).pack()

tree["columns"]=("one","two")

tree.heading("#0",text="Forms",anchor=tk.W)
tree.heading("one", text="Count",anchor=tk.W)
tree.heading("two", text="Notes",anchor=tk.W)

root.mainloop()
