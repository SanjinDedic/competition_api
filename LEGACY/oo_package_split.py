from fastapi.testclient import TestClient
from main import app
import json
import os

client = TestClient(app=app)

class ApiInterface:
    def __init__(self,team_name,team_password):
        self.team_name = team_name
        self.team_password = team_password
        self.__logged_in = False
        
    def login(self):
        #__logged_in is a private variable it is mirrored inside the Quiz class once login() is called
        response = client.post("/login", json={"name": self.team_name, "password": self.team_password})
        if response.status_code == 200:
            solved_qs = response.json()['solved_questions']
            solved_qs = json.loads(solved_qs)
            print('solved_qs:',solved_qs, type(solved_qs))
            self.__logged_in = True
            print('logged in')
            return True

        else:
            print('login failed')
            return False
        

    def get_question(self,question_num):
        if self.__logged_in:
            response = client.get("/get_question/"+str(question_num))
            if response.status_code == 200:
                return response.json()['question']
            else:
                return 'Question not found'
        if self.__logged_in == False:
            print('login first')
            return

    def submit_answer(self,question_num, answer):
        if self.__logged_in:
            response = client.post("/submit_answer", json={"id": str(question_num), "answer": answer, "team_name": self.team_name})
            if response.status_code == 200:
                return response.json()
            else:
                return 'API Connection error'
        if self.__logged_in == False:
            print('login first')
            return

    def get_teams_table(self):
        if self.__logged_in == False:
            print('login first')
            return
        response = client.get("/get_teams_table")
        if response.status_code == 200:
            return response.json()
        else:
            return 'API Connection error cannot get teams table'


class Quiz(ApiInterface):
    def __init__(self,team_name,team_password):
        super().__init__(team_name,team_password)
        self.__logged_in = self.login()
        response = client.get("/")
        self.total_questions = response.json()["length"]
        print('CONN ESTABLISHED, TOTAL QUESTIONS:', self.total_questions)

   
    def print_rankings(self):
        if self.__logged_in == False:
            print('login first')
            return
        teams_data = self.get_teams_table()
        scoreboard = Scoreboard(teams_data = teams_data)
        scoreboard.print_rankings()


    def print_status(self):
        if self.__logged_in == False:
            print('login first')
            return
        teams_data = self.get_teams_table()
        scoreboard = Scoreboard(teams_data = teams_data)
        scoreboard.print_status(self.team_name)

    def interactive_menu(self):
        if self.__logged_in == False:
            print('login first')
            return
        #os.system('cls' if os.name == 'nt' else 'clear')
        print('Welcome to VCC 2023', self.team_name,'What would you like to do?')
        print('1. View Question')
        print('2. Submit Answer')
        print('3. View Scoreboard')
        print('4. View Answered Questions')
        print('5. Exit')
        choice = input('Enter your choice:')
        if choice == '1':
            question_num = input('Enter question number:')
            question = self.get_question(question_num)
            print(question)
            input('Press enter to continue')
            self.interactive_menu()
        elif choice == '2':
            question_num = input('Enter question number:')
            print('Question:',self.get_question(question_num))
            answer = input('Enter answer:')
            result = self.submit_answer(question_num,answer)
            print(result)
            input('Press enter to continue')
            self.interactive_menu()
        elif choice == '3':
            self.print_rankings()
            input('Press enter to continue')
            self.interactive_menu()
        elif choice == '4':
            print('Here is the list of the questions you have answered:')
            self.print_status()
            input('Press enter to continue')
            self.interactive_menu()
        elif choice == '5':
            print('Goodbye')
            return


class Team():
    def __init__(self, name, score, solved_questions=[]):
        self.name = name
        self.score = score
        self.solved_questions = solved_questions


    def __str__(self):
        if len(self.name) < 8:
            answer = "TEAM NAME: "+ self.name + "\t\t  SCORE: " + str(self.score) + "\t  ANSWERED QUESTIONS: " + str(len(self.solved_questions))
        else:
            answer = "TEAM NAME: "+ self.name + "\t  SCORE: " + str(self.score) + + "\t  ANSWERED QUESTIONS: " + str(len(self.solved_questions))
        return answer


class Scoreboard():
    def __init__(self,teams_data):
        self.teams = []
        self.teams_data = teams_data
        self.load_teams()

    def load_teams(self):
        data_example = {'teams': [
            ['team1', 'team1', 0, '[]', 'red', 0], 
            ['team2', 'team2', 0, '[]', 'blue', 0], 
            ['team3', 'team3', 0, '[]', 'green', 0], 
            ['team4', 'team4', 0, '[]', 'yellow', 0]]}
        print(self.teams_data)
        for team in self.teams_data['teams']:
            solved_qs = json.loads(team[3])
            self.teams.append(Team(name=team[0],score=team[2],solved_questions=solved_qs))
        

    def print_rankings(self):
        #this function needs to add colors to the teams which are read from the json file
        #os.system('cls' if os.name == 'nt' else 'clear')
        ordered_teams = sorted(self.teams, key=lambda x: x.score, reverse=True)
        for team in ordered_teams:
            print(team)
    
    def print_status(self,team_name):
        for team in self.teams:
            if team.name == team_name:
                print(team_name,'score:',team.score,'solved questions:',team.solved_questions)

if __name__ == "__main__":
    quiz = Quiz('team1','team1')
    quiz.interactive_menu()