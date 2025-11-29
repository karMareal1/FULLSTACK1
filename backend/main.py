from flask import request, jsonify
from config import app, db
from models import Contact

@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contacts})


@app.route("/create_contact", methods=["POST"])
def create_contact():
    data = request.get_json()  # Using get_json() is generally safer than request.json
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    email = data.get("email")

    if not first_name or not last_name or not email:
        return (
            jsonify({"message": "You must include a first name, last name and email"}),
            400,
        )

    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    try:
        db.session.add(new_contact)
        db.session.commit() # ⬅️ FIX 1: Added parentheses
    except Exception as e:
        # Use str(e) or f-string for proper error message formatting
        return jsonify({"message": str(e)}), 400 # ⬅️ FIX 2: Corrected str() call
    
    return jsonify({"message": "Contact created successfully!"}), 201


# updating the contact
@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = Contact.query.get(user_id) # ⬅️ FIX 3: Corrected 'quesry' to 'query'

    if not contact:
        return jsonify({"message": "User not found"}), 404
    
    data = request.json
    # data.get(key, default) is the correct pattern for PATCH
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    db.session.commit()

    return jsonify({"message" : "User updated"}), 200


# deleting the contact
@app.delete("/delete_contact/<int:user_id>") # ⬅️ FIX 4: Used @app.delete, removed redundant methods=["DELETE"]
def delete_contact(user_id):
    contact = Contact.query.get(user_id) # ⬅️ FIX 3: Corrected 'quesry' to 'query'

    if not contact:
        return jsonify({"message": "User not found"}), 404
    
    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "User deleted!"}), 200

    
# Since when importing comes with the app running immediately, this only focuses on running the app if only this file was run
if __name__ == "__main__":
    with app.app_context():
        db.create_all() # Creating the database
    app.run(debug=True)