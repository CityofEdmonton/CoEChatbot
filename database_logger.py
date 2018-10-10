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


def logging_to_database(user,question,answer,parsed_key_words, search_used, group):
    db = connect_to_cloudsql()
    cursor = db.cursor()
    cursor.execute("USE history")
    tz = pytz.timezone('America/Edmonton')
    timestamp = datetime.datetime.now(tz).isoformat()
    user=str(user)
    question=str(question)
    answer = str(answer)
    cursor.execute("INSERT INTO chat_history VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", [timestamp, user, question, answer, "Null", parsed_key_words, search_used, group])
    db.commit()


def update_selected_answer(user, answer_selected):
    db = connect_to_cloudsql()
    cursor = db.cursor()
    user=str(user)
    answer_selected = str(answer_selected)
    cursor.execute("SET SQL_SAFE_UPDATES = 0")
    cursor.execute("Update history.chat_history Set Answer_selected = %s where Timestamp = (SELECT Timestamp FROM (select * from history.chat_history) AS subtable where User = %s ORDER BY Timestamp DESC LIMIT 1) and User =%s", [answer_selected, user,  user])
    db.commit()
