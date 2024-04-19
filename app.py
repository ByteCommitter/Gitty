from flask import Flask, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/addtrain',  methods=['GET', 'POST'])
def add_train():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="AlohaRailways"
    )

    # Get train data from the JSON body
    data = request.get_json()
    Train_ID = data['Train_ID']
    Name = data['Name']
    Train_Status = data['Train_Status']
    Type = data['Type']

    # Create a cursor
    cursor = db.cursor()

    # Check if Train_ID already exists
    cursor.execute("SELECT * FROM train WHERE Train_ID = %s", (Train_ID,))
    if cursor.fetchone() is not None:
        cursor.close()
        db.close()
        return 'Train ID already exists!', 400

    # Create the SQL query
    add_train_query = ("INSERT INTO train "
                       "(Train_ID, Name, Train_Status, Type) "
                       "VALUES (%s, %s, %s, %s)")

    # Execute the query
    cursor.execute(add_train_query, (Train_ID, Name, Train_Status, Type))
    
    # Commit the changes
    db.commit()

    # Close the cursor and connection
    cursor.close()
    db.close()

    return 'Train added successfully!', 200


if __name__ == '__main__':
    app.run(debug=True)