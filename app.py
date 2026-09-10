from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# In-memory mock database
students_db = [
    {"id": 1, "name": "Aarav Sharma", "email": "aarav@example.com", "course": "Computer Science", "gpa": 3.8},
    {"id": 2, "name": "Priya Patel", "email": "priya@example.com", "course": "Information Technology", "gpa": 3.5}
]
next_id = 3

# HTML Frontend Dashboard
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Student Management Portal</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="bg-light p-4">
    <div class="container">
        <h1 class="mb-4">Student Management System API Portal</h1>
        <div class="card p-3 mb-4 shadow-sm">
            <h3>API Base URL</h3>
            <code>http://127.0.0.1:5000/api/v1/students</code>
        </div>
        <div class="card p-3 shadow-sm">
            <h3>Current Student Records</h3>
            <table class="table table-striped mt-2">
                <thead>
                    <tr><th>ID</th><th>Name</th><th>Email</th><th>Course</th><th>GPA</th></tr>
                </thead>
                <tbody>
                    {% for student in students %}
                    <tr>
                        <td>{{ student.id }}</td>
                        <td>{{ student.name }}</td>
                        <td>{{ student.email }}</td>
                        <td>{{ student.course }}</td>
                        <td>{{ student.gpa }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

# Web Dashboard Route
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, students=students_db)

# ----------------- REST API ENDPOINTS -----------------

# GET /api/v1/students - Get all students or filter by course
@app.route('/api/v1/students', methods=['GET'])
def get_students():
    course = request.args.get('course')
    if course:
        filtered = [s for s in students_db if s['course'].lower() == course.lower()]
        return jsonify({"success": True, "data": filtered, "count": len(filtered)}), 200
    return jsonify({"success": True, "data": students_db, "count": len(students_db)}), 200

# GET /api/v1/students/<id> - Get single student
@app.route('/api/v1/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students_db if s['id'] == student_id), None)
    if not student:
        return jsonify({"success": False, "message": "Student not found"}), 404
    return jsonify({"success": True, "data": student}), 200

# POST /api/v1/students - Create new student
@app.route('/api/v1/students', methods=['POST'])
def create_student():
    global next_id
    # Authorization header check (Simulated)
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != "Bearer valid-token":
        return jsonify({"success": False, "message": "Unauthorized or invalid token"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid JSON body"}), 400

    required_fields = ['name', 'email', 'course', 'gpa']
    for field in required_fields:
        if field not in data:
            return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400

    # Validation
    if not isinstance(data['gpa'], (int, float)) or not (0.0 <= data['gpa'] <= 4.0):
        return jsonify({"success": False, "message": "GPA must be a float between 0.0 and 4.0"}), 422

    if any(s['email'] == data['email'] for s in students_db):
        return jsonify({"success": False, "message": "Email already registered"}), 409

    new_student = {
        "id": next_id,
        "name": data['name'],
        "email": data['email'],
        "course": data['course'],
        "gpa": float(data['gpa'])
    }
    students_db.append(new_student)
    next_id += 1
    return jsonify({"success": True, "data": new_student}), 201

# PUT /api/v1/students/<id> - Update existing student
@app.route('/api/v1/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != "Bearer valid-token":
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    student = next((s for s in students_db if s['id'] == student_id), None)
    if not student:
        return jsonify({"success": False, "message": "Student not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid JSON payload"}), 400

    student['name'] = data.get('name', student['name'])
    student['email'] = data.get('email', student['email'])
    student['course'] = data.get('course', student['course'])
    student['gpa'] = data.get('gpa', student['gpa'])

    return jsonify({"success": True, "data": student, "message": "Updated successfully"}), 200

# DELETE /api/v1/students/<id> - Delete student
@app.route('/api/v1/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != "Bearer valid-token":
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    global students_db
    student = next((s for s in students_db if s['id'] == student_id), None)
    if not student:
        return jsonify({"success": False, "message": "Student not found"}), 404

    students_db = [s for s in students_db if s['id'] != student_id]
    return jsonify({"success": True, "message": f"Student with ID {student_id} deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)