from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy #ORM

app = Flask(__name__)

# Create Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///student.db"

db = SQLAlchemy(app)

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(50), nullable=False)
    major = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id" : self.id,
            "student_name" : self.student_name,
            "major" : self.major,
            "grade" : self.grade
        }
with app.app_context():
    db.create_all()
        

# Create Routes

@app.route("/")
def home():
    return jsonify({"message":"Welcome to the Student API"})

# https://[ec2-public-ip]:5000/destinations

# GET

@app.route("/destinations",methods=["GET"])
def get_destinations():
    destinations = Destination.query.all()
    return jsonify([destination.to_dict() for destination in destinations])

# https://[ec2-public-ip]:5000/destinations/2
@app.route("/destinations/<int:destination_id>", methods=["GET"])
def get_destination():
    destination = Destination.query.get(destination_id)
    if destination:
        return jsonify(destination.to_dict())
    else:
        return jsonify({"error":"Destination not found!"}), 404


# POST 

@app.route("/destinations", methods=["POST"])
def add_destination():
    data = request.get_json()

    new_destination = Destination(student_name=data["student_name"],
                                  major=data["major"],
                                  grade=data["grade"])
    db.session.add(new_destination)
    db.session.commit()
    
    return jsonify(new_destination.to_dict()), 201


# PUT --> UPDATE

@app.route("/destinations/<int:destination_id>", methods=["PUT"])
def update_destination(destination_id):
    data = request.get_json()
    
    destination = Destination.query.get(destination_id)
    if destination:
        destination.student_name = data.get("student_name", destination.student_name)
        destination.major = data.get("major", destination.major)
        destination.grade = data.get("grade", destination.grade)
        
        db.session.commit()
        
        return jsonify(destination.to_dict())
    else:
        return jsonify({"error":"Destination not found!"}), 404


# DELETE 

@app.route("/destinations/<int:destination_id>", methods=["DELETE"])
def delete_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination:
        db.session.delete(destination)
        db.session.commit()
        
        return jsonify({"message":"destination was deleted!"})
    else:
        return jsonify({"error":"Destination not found!"}), 404
                              


if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000, debug=True)
