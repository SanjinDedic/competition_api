from oo_package import Quiz
import time

time.sleep(1)
with open("reset_db.py") as f:
    exec(f.read())
time.sleep(1)


competition = Quiz(team_name='team2',team_password='team2')

for i in range(1,competition.total_questions+1):
    print(competition.get_question(i))

print(competition.submit_answer(1,'Sajin'))
print(competition.submit_answer(2,'3'))
print(competition.submit_answer(3,'Pyhon'))

print(competition.submit_answer(1,'Sanjin'))
print(competition.submit_answer(2,'38'))
print(competition.submit_answer(3,'Python'))
sol = '''cerpxazeceaqacth
echampionsofcode
arehereichfuxncu'''
print(competition.submit_answer(4,sol))


print(competition.submit_answer(1,'Sanjin'))
print(competition.submit_answer(2,'38'))
print(competition.submit_answer(3,'Python'))

competition.print_rankings()