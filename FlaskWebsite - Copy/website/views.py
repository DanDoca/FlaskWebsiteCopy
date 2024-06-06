
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, Course, Module, ModuleContents, User, Staff
from . import db
import json

views = Blueprint('views', __name__)

# Home page route
@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

# Dash Page 
@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dash():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("dashboard.html", user=current_user)
# Delete note function
@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted!', category='error')

    return jsonify({})

# User/course registration
@views.route('/user-courses')
@login_required
def user_courses():
    courses = current_user.courses  
    courses_data = [
        {
            'id': course.id,
            'title': course.title,
            'modules': [{'title': module.title} for module in course.modules]
        }
        for course in courses
    ]
    return jsonify(courses_data)

# ADMIN PAGE
@views.route('/admin')
def admin_page():
    users = User.query.all()
    modules = Module.query.all()
    courses = Course.query.all()
    staff = Staff.query.all()
    return render_template('admin.html', users=users, modules=modules, courses=courses, staff=staff, user=current_user)
# Add User record
@views.route('/add_user', methods=['POST'])
def add_user():
    email = request.form.get('email')
    first_Name = request.form.get('first_Name')
    role = request.form.get('role')
    
    new_user = User(email=email, first_Name=first_Name, role=role)
    db.session.add(new_user)
    db.session.commit()
    flash('Record added!', category='success')
    
    return redirect(url_for('views.admin_page'))
# Add Module record
@views.route('/add_module', methods=['POST'])
def add_module():
    module_code = request.form.get('module_code')
    title = request.form.get('title')
    description = request.form.get('description')
    
    new_module = Module(module_code=module_code, title=title, description=description)
    db.session.add(new_module)
    db.session.commit()
    flash('Record added!', category='success')
    
    return redirect(url_for('views.admin_page'))
# Add Course record
@views.route('/add_course', methods=['POST'])
def add_course():
    title = request.form.get('title')
    description = request.form.get('description')
    
    new_course = Course(title=title, description=description)
    db.session.add(new_course)
    db.session.commit()
    flash('Record added!', category='success')
    
    return redirect(url_for('views.admin_page'))
# Add Staff record
@views.route('/add_staff', methods=['POST'])
def add_staff():
    name = request.form.get('name')
    surname = request.form.get('surname')
    telephone = request.form.get('telephone')
    position = request.form.get('position')
    
    new_staff = Staff(name=name, surname=surname, telephone=telephone, position=position)
    db.session.add(new_staff)
    db.session.commit()
    flash('Record added!', category='success')
    
    return redirect(url_for('views.admin_page'))

# Featured course function:
@views.route('/featured_courses')
def featured_courses():
    courses = ["Artificial Intelligence", "Machine Learning Fundamentals", "Data Science and Analytics"]
    return jsonify(courses)

# Course page
@views.route('/course', methods=['GET', 'POST'])
def courses():
    courses = Course.query.all()  # Get all courses from the database
    return render_template("course.html", user=current_user, courses=courses)
# For course modules:
@views.route('/course-details/<int:course_id>', methods=['GET'])
@login_required
def course_details(course_id):
    try:
        course = Course.query.get(course_id)
        if course:
            modules = Module.query.filter_by(course_id=course_id).all()
            modules_data = []
            for module in modules:
                staff_data = [{'name': staff.name, 'surname': staff.surname, 'position': staff.position} for staff in module.staff]
                modules_data.append({'title': module.title, 'description': module.description, 'staff': staff_data})

            return jsonify({
                'course': {'title': course.title, 'description': course.description},
                'modules': modules_data
            })
        else:
            return jsonify({'error': 'Course not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Course register
@views.route('/register-course', methods=['POST'])
@login_required
def register_course():
    data = request.get_json()
    course_id = data.get('course_id')

    if not course_id:
        return jsonify({'error': 'No course ID provided'}), 400

    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404

    # Register the user to the course
    current_user.courses.append(course)
    db.session.commit()
    #flash('Registration completed!', category='success')

    return jsonify({'success': 'Registration completed!'})