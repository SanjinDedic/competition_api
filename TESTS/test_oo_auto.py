import sys,os
sys.path.append('../PACKAGE')

from oo_package import Quiz

competition = Quiz(team_name='team1',team_password='password1')


print(competition.get_question(1))