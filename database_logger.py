# [START all]
# https://stackoverflow.com/questions/14144150/passing-parameters-to-a-webapp2-requesthandler-object-in-python
import os
import MySQLdb
import datetime
import pytz



# These environment variables are configured in app.yaml.
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')

def connect_to_cloudsql():
    # When deployed to App Engine, the `SERVER_SOFTWARE` environment variable
    # will be set to 'Google App Engine/version'.
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD)

    else:
        db = MySQLdb.connect(
            host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)

    return db


def logging_to_database(user,question,answer):
    db = connect_to_cloudsql()
    cursor = db.cursor()
    cursor.execute("USE history")
    tz = pytz.timezone('America/Edmonton')
    timestamp = datetime.datetime.now(tz).isoformat()
    user=str(user)
    question=str(question)
    answer = str(answer)
    cursor.execute("INSERT INTO chat_history VALUES (%s, %s, %s, %s, %s)", [timestamp, user, question, answer, "Null"])
    db.commit()

# Need to find a way to update
def update_selected_answer(user, answer_selected, original_question):
    db = connect_to_cloudsql()
    cursor = db.cursor()
    cursor.execute("USE history")
    user=str(user)
    answer_selected = str(answer_selected)
    print("TESTING ", user,original_question, answer_selected)
    cursor.execute("UPDATE chat_history SET Answer_selected = %s WHERE User = %s and Question = %s", [answer_selected, user, original_question])
    db.commit()
