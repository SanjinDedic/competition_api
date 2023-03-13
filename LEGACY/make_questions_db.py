import os, sqlite3

#create a list of questions based on the questions folder
import sqlite3

conn = sqlite3.connect('questions.db')
c = conn.cursor()
c.execute('''CREATE TABLE questions
                (id text, question_content text, answer text, starter_file blob, input_file blob)''')


for filename in os.listdir('questions'):
    if filename.endswith('.txt') and not 'input' in filename:
        with open('questions/' + filename, 'r') as f:
            id = filename[:-4]
            print(id)
            content = f.read()
            #write id and content to the database
            c.execute("INSERT INTO questions VALUES (?, ?, ?, ?, ?)", (id, content, '', '', ''))

    if filename.endswith('.py'):
        with open('questions/' + filename, 'rb') as f:
            id = filename.split('_')[0]
            print(id)
            starter_file = f.read()
            c.execute("UPDATE questions SET starter_file = ? WHERE id = ?", (starter_file, id))
            
    if 'input' in filename:
        with open('questions/' + filename, 'rb') as f:
            id = filename.split('_')[0]
            print(id)
            input_file = f.read()
            c.execute("UPDATE questions SET input_file = ? WHERE id = ?", (input_file, id))
    

for filename in os.listdir('solutions'):
    if filename.endswith('.txt'):
        with open('solutions/' + filename, 'r') as f:
            answer = f.read()
            #write answer to the database
            c.execute("UPDATE questions SET answer = ? WHERE id = ?", (answer, filename[:-4]))


conn.commit()
conn.close()