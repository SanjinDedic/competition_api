from oo_package import Quiz
import time

time.sleep(1)
with open("reset_db.py") as f:
    exec(f.read())
time.sleep(1)


competition = Quiz(team_name='team1',team_password='team1')

competition.submit_answer(1,'Sanjin')
competition.print_rankings()
time.sleep(2)


competition = Quiz(team_name='team2',team_password='team2')
competition.submit_answer(2,'38')
competition.submit_answer(3,'Python')
competition.print_rankings()
time.sleep(2)

competition = Quiz(team_name='team3',team_password='team3')
competition.submit_answer(2,'38')
competition.submit_answer(3,'Python')
sol = '''cerpxazeceaqacth
echampionsofcode
arehereichfuxncu'''
print(competition.submit_answer(4,sol))
competition.print_rankings()
time.sleep(2)


competition = Quiz(team_name='team4',team_password='team4')
competition.submit_answer(1,'Sanjin')
competition.submit_answer(2,'38')
competition.submit_answer(3,'Python')
sol = '''cerpxazeceaqacth
echampionsofcode
arehereichfuxncu'''
print(competition.submit_answer(4,sol))
competition.print_rankings()
print('Simulation complete')


competition.print_rankings()