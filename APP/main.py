from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sqlite3
import json

app = FastAPI()


class Answer(BaseModel):
    id: str
    answer: str
    team_name: str

class Login(BaseModel):
    name: str
    password: str


@app.get("/")
async def home():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM questions")
    questions = c.fetchall()
    return {"length": len(questions)}


@app.post("/login")
async def login(team: Login):
    team_name = team.name
    team_password = team.password
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM teams WHERE name = ? AND password = ?", (team_name, team_password))
    team = c.fetchone()
    if team == None:
        return {"message": "Login failed"}
    else:
        return {"message": "Login successful", "score": team[2], "solved_questions": team[3], "color": team[4],"connected": team[5]}


@app.get("/get_question/{id}")
async def get_question(id: str):
    attachment = ''
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM questions WHERE id = ?", (id,))
    question = c.fetchone()
    #print(question)
    if question == None:
        return {"message": "Question not found"}
    else:
        if question[4] != '':
            attachment = '\n' + 'Download starter code ' + question[4] + '\n'
        if question[5] != '':
            attachment += 'Download input file ' + question[5]
        return {"question": question[1] + attachment}
    

@app.get("/download_starter_code/{id}",response_class=FileResponse)
async def download_starter_code(id: str):
    return 'questions/' + id + '_starter.py'


#See if we can download the file from database?
#See if we can attach headers to this response that contain the file name
@app.get("/download_input_file/{id}", response_class=FileResponse)
async def download_input_file(id: str):
    return 'questions/' + id + '_input.txt'


@app.get("/get_teams_table")
async def get_teams_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM teams")
    teams = c.fetchall()
    return {"teams": teams}


#just need to figure out how to get the solved questions list updated in the database
@app.post("/submit_answer")
async def submit_answer(a: Answer):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM questions WHERE id = ?", (a.id,))
    question = c.fetchone()
    if question == None:
        return {"message": "Question not found"}   
    elif question[2] == a.answer:
        #print('correct answer for an existing question, points won: ', question[3])
        resp = update_teams_table(question_id=a.id, team_name=a.team_name, points_won=question[3])
        return resp
    else:
        return {"message": "Incorrect"}
        


def update_teams_table(question_id, points_won, team_name):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM teams WHERE name = ?", (team_name,))
    team = c.fetchone()
    if team == None:
        return {"message": "Team not found"}
    #parse the team info
    try:
        solved_questions = json.loads(team[3])
        #print(question_id, type(question_id), solved_questions, type(solved_questions))
        if int(question_id) in solved_questions:
            return {"message": "Already solved"}
    except:
        print("Cannot load team data")
    try:
        points_total = team[2]
        points_total += points_won
        solved_questions = json.loads(team[3])
        solved_questions.append(int(question_id))
        solved_questions = json.dumps(solved_questions)
        #print("solved questions: ", solved_questions)
        #update the database with the new values for score and solved questions
        c.execute("UPDATE teams SET score = ?, solved_questions = ? WHERE name = ?", (points_total, solved_questions, team_name))
        conn.commit()
        #print("team found attempting to update db for question_id", question_id)
        return {"message": "Correct", "points": points_won, "team_score": points_total}
    except:
        return {"message": "Error updating database"}
    return {"message": "Something went very wrong"}

