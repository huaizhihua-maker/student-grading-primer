from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this
def _error(message="Not found", status_code=404):
    return jsonify({"error": message}), status_code

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    # TODO: replace with your implementation. This is a mock response
    # return jsonify([
    #     {'course': 'COMP1531', 'id': 1, 'mark': 85, 'name': 'Alice Zhang'},
    #     {'course': 'COMP1531', 'id': 2, 'mark': 72, 'name': 'Bob Smith'}
    # ]), 200
    try:
        return jsonify(db.get_all_students()), 200
    except Exception as e:
        return _error(str(e), 500)



@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """

    # Getting the request body - replace with your implementation
    student_data = request.json
    name = student_data.get("name")
    course = student_data.get("course")
    raw_mark = student_data.get("mark", None)
    # check name, course, mark are valid
    if not isinstance(name, str) or not name.strip():
        return _error("Name must be a non-empty string", 400)
    if not isinstance(course, str) or not course.strip():
        return _error("Course must be a non-empty string", 400)
    # edge case
    mark = 0
    if raw_mark is None:
        mark = 0
    else:
        try:
            mark = int(raw_mark)
        except ValueError:
            return _error("Mark must be an integer", 400)
        if mark < 0 or mark > 100:
            return _error("Mark must be between 0 and 100", 400)
        
    # Create the student
    new_student = db.insert_student(name.strip(), course.strip(), mark)
    return jsonify(new_student), 200

@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    student_data = request.json
    name = student_data.get("name")
    course = student_data.get("course")
    raw_mark = student_data.get("mark", None)
    if not isinstance(name, str) or not name.strip():
        return _error("Name must be a non-empty string", 400)
    if not isinstance(course, str) or not course.strip():
        return _error("Course must be a non-empty string", 400)
    # edge case
    mark = 0
    if raw_mark is None:
        mark = 0
    else:
        try:
            mark = int(raw_mark)
        except ValueError:
            return _error("Mark must be an integer", 400)
        if mark < 0 or mark > 100:
            return _error("Mark must be between 0 and 100", 400)
    # update the student to db
    updated_student = db.update_student(student_id, name.strip(), course.strip(), mark)
    if updated_student is None:
        return _error("Student not found", 404)
    return jsonify(updated_student), 200
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    try:
        deleted_student = db.delete_student(student_id)
        if deleted_student is None:
            return _error("Student not found", 404)
        return jsonify(deleted_student), 200
    except Exception as e:
        return _error(str(e), 500)

@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    try:
        students = db.get_all_students()
        marks=[s.get("mark") for s in students if s.get("mark") is not None]
        if not marks:
            return jsonify({"count": 0, "average": 0, "min": 0, "max": 0}), 200
        
        count = len(marks)
        if count == 0:
            return jsonify({"count": 0, "average": 0, "min": 0, "max": 0}), 200
        else:
            average = sum(marks) / count
        return jsonify({
            "count": count,
            "average": average,
            "min": min(marks),
            "max": max(marks)
        }), 200
    except Exception as e:
        return _error(str(e), 500)


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
