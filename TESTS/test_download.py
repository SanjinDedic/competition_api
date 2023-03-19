from fastapi.testclient import TestClient
from APP.main import app

client = TestClient(app=app)


def test_get_input(question_id):
    question_id = str(question_id)
    filename = question_id + '_input.txt'
    response = client.get("/download_input_file/4")
    file = open(filename, 'w')
    #write the response to the file, remove any newlines
    file.write(response.text.replace('\r', ''))
    file.close()


def test_get_starter():
    response = client.get("/download_starter_code/4")
    print(response)


test_get_input(question_id = 4)
test_get_starter()
