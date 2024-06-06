from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Association table for User and Course
user_courses = db.Table('user_courses',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

# Association table for Module and Staff
module_staff = db.Table('module_staff',
    db.Column('module_code', db.String(150), db.ForeignKey('module.module_code'), primary_key=True),
    db.Column('staff_id', db.Integer, db.ForeignKey('staff.id'), primary_key=True)
)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_Name = db.Column(db.String(150))
    role = db.Column(db.String(50))
    notes = db.relationship('Note', backref='user', lazy=True)
    courses = db.relationship('Course', secondary=user_courses, backref=db.backref('students', lazy='dynamic'))

class Module(db.Model):
    module_code = db.Column(db.String(150), primary_key=True)
    title = db.Column(db.String(250), unique=True)
    description = db.Column(db.String(10000))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    staff = db.relationship('Staff', secondary=module_staff, backref=db.backref('modules', lazy='dynamic'))

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True)
    description = db.Column(db.String(10000))
    modules = db.relationship('Module', backref='course', lazy=True)

class ModuleContents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_code = db.Column(db.String(150), db.ForeignKey('module.module_code'))
    section_title = db.Column(db.String(250))
    description = db.Column(db.String(10000))

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    surname = db.Column(db.String(150), nullable=False)
    telephone = db.Column(db.String(150))
    position = db.Column(db.String(100), nullable=False)
