from flask import request, jsonify
from config import app, db
from models import Contact

@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()  #fetch all contacts from database
    json_contacts = list(map(lambda x:x.to_json(), contacts))
    return jsonify({"contacts": json_contacts})    

#since when importing comes with the app running immediatly, this only focuses on running the app if only this file was run
if __name__ == "__main__":
    with app.app_context():
        app.create_all() #creating the database
    app.run(debug=True)
