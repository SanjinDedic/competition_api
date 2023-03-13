import json
import sqlite3



conn = sqlite3.connect('database_bk.db')
c = conn.cursor()
team_name = "team1"
#fetch team1 from database
c.execute("SELECT * FROM teams WHERE name = ?", (team_name,))
team = c.fetchone()
print(team)
answer_id = 1
points_won = 10
points_total = 0
points_total += points_won
solved_questions = team[3]
solved_questions = json.loads(solved_questions)
solved_questions.append(answer_id)
solved_questions = json.dumps(solved_questions)

#update the database with the new values for score and solved questions
c.execute("UPDATE teams SET score = ?, solved_questions = ? WHERE name = ?", (points_total, solved_questions, team_name))
conn.commit()