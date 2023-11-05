from flask import Flask, render_template, request, redirect, url_for, session

from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    university_name = db.Column(db.String(80), nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    expected_year_to_complete_degree = db.Column(db.Integer, nullable=False)
    projects_done = db.Column(db.Text, nullable=True)
    links_for_certificates = db.Column(db.Text, nullable=True)
    skills = db.Column(db.String(80), nullable=False)
    field_of_interest = db.Column(db.Text, nullable=True)
    linkedin_id = db.Column(db.String(80), nullable=True)
    github_id = db.Column(db.String(80), nullable=True)
    internship_done = db.Column(db.Boolean, nullable=False)
    company_name = db.Column(db.String(80), nullable=True)
    duration = db.Column(db.String(20), nullable=True)
    work_experience = db.Column(db.Text, nullable=True)
    password = db.Column(db.Text, nullable=False)
    test_per = db.Column(db.String(20))
    task_per = db.Column(db.String(20))
    project_per = db.Column(db.String(20))
    def __repr__(self):
        return f'{self.name}: {self.email}'

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(80), nullable=False)
    work_condition = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(80), nullable=False)
    duration = db.Column(db.String(20), nullable=False)
    stipend_per_month = db.Column(db.Float, nullable=False)
    apply_by = db.Column(db.String(20), nullable=False)
    applicants = db.Column(db.Integer, nullable=False)
    skills_required = db.Column(db.Text, nullable=True)
    perks = db.Column(db.Text, nullable=True)
    number_of_openings = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    projects_for_work = db.Column(db.Text, nullable=True)
    about_company = db.Column(db.Text, nullable=True)
    password = db.Column(db.Text, nullable=False)
    def __repr__(self):
        return f'{self.company}: {self.location}'

with app.app_context():
    db.create_all()
    
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/register_intern', methods=['GET', 'POST'])
def register_intern():
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match. Please try again."

        hashed_password = generate_password_hash(password)
        new_user = Data(
            name=request.form['name'],
            university_name=request.form['university_name'],
            cgpa=request.form['cgpa'],
            email=request.form['email'],
            phone_number=request.form['phone_number'],
            expected_year_to_complete_degree=request.form['expected_year_to_complete_degree'],
            projects_done=request.form['projects_done'],
            links_for_certificates=request.form['links_for_certificates'],
            skills=request.form['skills'],
            field_of_interest=request.form['field_of_interest'],
            linkedin_id=request.form['linkedin_id'],
            github_id=request.form['github_id'],
            internship_done=request.form['internship_done'] == 'yes',
            company_name=request.form.get('company_name'), 
            duration=request.form.get('duration'),
            work_experience=request.form.get('work_experience'),
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register_user.html')

@app.route('/register_provider', methods=['GET', 'POST'])
def register_provider():
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match. Please try again."

        hashed_password = generate_password_hash(password)
        new_company = Company(
            company=request.form['company'],
            work_condition=request.form['work_condition'],
            email=request.form['email'],
            phone_number=request.form['phone_number'],
            location=request.form['location'],
            duration=request.form['duration'],
            stipend_per_month=request.form['stipend_per_month'],
            apply_by=request.form['apply_by'],
            applicants=request.form['applicants'],
            skills_required=request.form['skills_required'],
            perks=request.form['perks'],
            number_of_openings=request.form['number_of_openings'],
            category=request.form['category'],
            projects_for_work=request.form['projects_for_work'],
            about_company=request.form['about_company'],
            password=hashed_password
        )

        db.session.add(new_company)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register_comp.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['user']
        password = request.form['password']

        user = Data.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_type'] = 'intern'
            return redirect(url_for('index'))

        company = Company.query.filter_by(email=email).first()
        if company and check_password_hash(company.password, password):
            session['user_id'] = company.id
            session['user_type'] = 'company'
            return redirect(url_for('index'))

        return "Invalid email or password. Please try again."
    return render_template('login.html')


@app.route('/index')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/profile')
def profile():
    
    if session['user_type'] == 'intern':
        user = Data.query.get(session['user_id'])
        return render_template('profile_user.html', user=user)
    else:
        company = Company.query.get(session['user_id'])
        return render_template('profile_comp.html', company=company)
    
@app.route('/companies')
def companies():
    companies = Company.query.all()
    return render_template('companies.html', companies=companies)

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', contacts=contacts)

@app.route('/projects')
def projects():
    return render_template('project.html', contacts=projects)

@app.route('/tasks')
def tasks():
    return render_template('task.html', contacts=tasks)

@app.route('/test')
def test():
    return render_template('test.html', contacts=test)

def percentageMatching(list1, list2):
    '''
    compares list1 with list2
    '''
    count = 0
    for val1 in list1:
        for val2 in list2:
            if val1 == val2:
                count += 1
    return count * 100/(len(list2))

import pandas as pd

with app.app_context():
    companies = Company.query.all()
    students = Data.query.all()

nirf = 0.1
CGPA = 0.2
project = 0.2
test = 0.1
task = 0.1
skill_based = 0.3

# Create a list of company requirements
company_all = {}
for company in companies:
    lst = []
    for student in students:
        temp = ( student.cgpa * CGPA + student.project_per * project + student.test_per * test + student.task_per * task)
        lst.append((student.name, temp))
    company_all[company.company] = lst

# Create a list of company requirements
company_requirements = {}
for company in companies:
    company_requirements[company.company] = company.skills_required.lower().split(', ')

# Create a list of student skills
student_skills = {}
for student in students:
    student_skills[student.name] = student.skills.lower().split(', ')

# Create a list of matched companies
matched_companies = {}
for j, requiredSkill in zip(company_requirements.items(), company_all.items()):
    value = requiredSkill[1]
    temp = []
    for i, student_skill in zip(student_skills.items(), value):
        tup = i[1]
        if percentageMatching(i[1], j[1]) >= 50:
            temp.append((i[0], percentageMatching(i[1], j[1]), 'skill based match',student_skill[1] + percentageMatching(i[1], j[1]) * skill_based, 'overall percentage'))
    matched_companies[j[0]] = temp

matched_user = {}
for j, student_skill in student_skills.items():
    # value = requiredSkill[1]
    # temp = []
    for i, requiredSkill in company_requirements.items():
        # tup = i[1]
        if percentageMatching(requiredSkill, student_skill) >= 50:
            temp.append((i,  percentageMatching(requiredSkill, student_skill), 'skill based match'))
    matched_user[j] = temp

matched_companies_all = {}


# matched_companies_df = pd.DataFrame({'matched_companies': matched_companies})

# json_data = matched_companies_df.to_json(orient='records')

@app.route("/intern/<company_name>")
def intern(company_name):
    return render_template("intern.html", matched_companies=matched_companies, company_name=company_name)



@app.route("/comp/<intern_id>")
def comp(intern_id):
    return render_template("user_comp.html", matched_user=matched_user, intern_id = intern_id)



