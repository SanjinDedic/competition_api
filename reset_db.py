import os, sqlite3
import json

#create a list of questions based on the questions folder
import sqlite3
import os

os.remove('database.db')
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE questions
                (id text, question_content text, answer text, points integer, starter_file text, input_file text)''')

for filename in os.listdir('questions'):
    if filename.endswith('.txt') and not 'input' in filename:
        with open('questions/' + filename, 'r') as f:
            id = filename[:-4]
            points = -(-int(id)//10)*10 #10 pts for first 10 questions, 20 for next 10, 30 for next 10, etc.
            content = f.read()
            #write id and content to the database
            c.execute("INSERT INTO questions VALUES (?, ?, ?, ?, ?, ?)", (id, content, '', points, '', ''))

    if filename.endswith('.py'):
        id = filename.split('_')[0]
        print(id, filename)
        c.execute("UPDATE questions SET starter_file = ? WHERE id = ?", (filename, id))
            
    if 'input' in filename:
        id = filename.split('_')[0]
        print(id,filename)
        c.execute("UPDATE questions SET input_file = ? WHERE id = ?", (filename, id))
    

for filename in os.listdir('solutions'):
    if filename.endswith('.txt'):
        with open('solutions/' + filename, 'r') as f:
            answer = f.read()
            #write answer to the database
            c.execute("UPDATE questions SET answer = ? WHERE id = ?", (answer, filename[:-4]))


conn.commit()
'''create a table for teams with the following fields:
name - text
password - text
score - integer
solved_questions - text
color - text
connected - boolean
'''
c.execute('''CREATE TABLE teams
                (name text, password text, score integer, solved_questions text, color text, connected boolean)''')

#add the teams to the database
solved_qs = json.dumps([])
print(solved_qs, type(solved_qs))

c.execute("INSERT INTO teams VALUES (?, ?, ?, ?, ?, ?)", ('team1', 'team1', 0, solved_qs, 'red', False))
c.execute("INSERT INTO teams VALUES (?, ?, ?, ?, ?, ?)", ('team2', 'team2', 0, solved_qs, 'blue', False))
c.execute("INSERT INTO teams VALUES (?, ?, ?, ?, ?, ?)", ('team3', 'team3', 0, solved_qs, 'green', False))
c.execute("INSERT INTO teams VALUES (?, ?, ?, ?, ?, ?)", ('team4', 'team4', 0, solved_qs, 'yellow', False))

conn.commit()
conn.close()

print('Database created successfully')