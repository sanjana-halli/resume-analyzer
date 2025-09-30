# app.py

# --- 1. Imports ---
from flask import Flask, render_template, request, jsonify
import os
import docx
import fitz  # PyMuPDF
from werkzeug.utils import secure_filename
import re

# --- 2. Flask App Initialization & Configuration ---
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- 3. Knowledge Base and Constants ---
# All databases are defined here, BEFORE any functions that use them.
SKILLS_DB = [
    'python', 'java', 'c++', 'javascript', 'html', 'css', 'react', 'angular', 'vue',
    'node.js', 'flask', 'django', 'ruby', 'php', 'swift', 'kotlin', 'sql', 'nosql',
    'mongodb', 'postgresql', 'mysql', 'git', 'docker', 'kubernetes', 'aws', 'azure',
    'gcp', 'machine learning', 'data analysis', 'project management', 'agile', 'scrum',
    'oop', 'data structures', 'excel', 'tableau'
]

SUGGESTIONS_DB = {
    'python': {
        'importance': 'A versatile backend language essential for server-side logic, data science, and automation.',
        'course_link': 'https://www.coursera.org/specializations/python-3-programming'
    },
    'javascript': {
        'importance': 'The core language of the web, crucial for creating interactive and dynamic frontend experiences.',
        'course_link': 'https://www.udemy.com/course/the-complete-javascript-course/'
    },
    'react': {
        'importance': 'A popular JavaScript library for building modern, component-based user interfaces.',
        'course_link': 'https://www.coursera.org/learn/react-basics'
    },
    'sql': {
        'importance': 'The standard language for managing and querying relational databases like PostgreSQL and MySQL.',
        'course_link': 'https://www.coursera.org/learn/sql-for-data-science'
    },
    'aws': {
        'importance': 'A leading cloud platform; skills in AWS are highly sought after for deploying and managing scalable applications.',
        'course_link': 'https://www.coursera.org/learn/aws-cloud-practitioner-essentials'
    },
    'docker': {
        'importance': 'A containerization tool that simplifies application deployment and ensures consistency across environments.',
        'course_link': 'https://www.udemy.com/course/docker-for-the-absolute-beginner/'
    },
    'git': {
        'importance': 'An essential version control system for tracking code changes and collaborating with other developers.',
        'course_link': 'https://www.coursera.org/learn/introduction-git-github'
    }
}

JOB_FIELDS_DB = {
    "Web Developer": ["Html", "Css", "Javascript", "React", "Node.js", "Git", "Sql"],
    "Software Engineer": ["Python", "Java", "Oop", "Data Structures", "Git", "Docker", "Sql"],
    "Data Analyst": ["Sql", "Excel", "Python", "Tableau", "Data Analysis"],
    "DevOps Engineer": ["Docker", "Kubernetes", "Aws", "Git", "Python"],
    "Mobile Developer": ["Java", "Swift", "Kotlin", "React"],
    "Project Manager": ["Agile", "Scrum", "Project Management"]
}

SKILL_KEYWORDS = ['skills', 'technical skills', 'programming languages', 'technologies']
STOPPER_KEYWORDS = ['experience', 'work experience', 'education', 'projects', 'certifications', 'interests', 'awards']

# --- Helper functions ---
def extract_text_from_docx(filepath):
    try:
        doc = docx.Document(filepath)
        return '\n'.join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error reading docx file: {e}")
        return ""

def extract_text_from_pdf(filepath):
    try:
        doc = fitz.open(filepath)
        text = "".join(page.get_text() for page in doc)
        doc.close()
        return text
    except Exception as e:
        print(f"Error reading pdf file: {e}")
        return ""

def get_text_from_input(file_key, text_key):
    text = ""
    file = request.files.get(file_key)
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        if filename.endswith('.docx'): text = extract_text_from_docx(filepath)
        elif filename.endswith('.pdf'): text = extract_text_from_pdf(filepath)
        os.remove(filepath)
    if not text: text = request.form.get(text_key, '')
    return text

def extract_skills_from_section(full_resume_text):
    skills_section_text = ""
    start_pattern = r"(?i)^\s*(" + "|".join(SKILL_KEYWORDS) + r")\s*$"
    start_match = re.search(start_pattern, full_resume_text, re.MULTILINE)
    if start_match:
        text_after_skills = full_resume_text[start_match.end():]
        end_pattern = r"(?i)^\s*(" + "|".join(STOPPER_KEYWORDS) + r")\s*$"
        end_match = re.search(end_pattern, text_after_skills, re.MULTILINE)
        skills_section_text = text_after_skills[:end_match.start()] if end_match else text_after_skills
    return extract_skills(skills_section_text) if skills_section_text else []

def extract_skills(text):
    found_skills = set()
    text_lower = text.lower()
    for skill in SKILLS_DB:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found_skills.add(skill.capitalize())
    return sorted(list(found_skills))

def calculate_match_score(resume_skills, target_skills):
    resume_skills_set = set(skill.lower() for skill in resume_skills)
    target_skills_set = set(skill.lower() for skill in target_skills)
    if not target_skills_set: return 0, [], []
    matched_skills = resume_skills_set.intersection(target_skills_set)
    missing_skills = target_skills_set.difference(resume_skills_set)
    score = (len(matched_skills) / len(target_skills_set)) * 100
    return int(score), sorted([s.capitalize() for s in matched_skills]), sorted([s.capitalize() for s in missing_skills])

def generate_feedback_and_suggestions(score, missing_skills, resume_text, jd_text):
    feedback_points = []
    suggestions = {}
    if score >= 80:
        feedback_points.append("<strong>Overall Assessment:</strong> Excellent match! Your skills align very well with this role's requirements.")
    elif score >= 50:
        feedback_points.append(f"<strong>Overall Assessment:</strong> Good match! You have a solid foundation of the required skills.")
    else:
        feedback_points.append("<strong>Overall Assessment:</strong> There's room for improvement. This role requires several skills not listed in your resume.")

    critical_missing_skills, other_missing_skills = [], []
    jd_text_lower = jd_text.lower()
    for skill in missing_skills:
        if jd_text_lower.count(skill.lower()) >= 3: critical_missing_skills.append(skill)
        else: other_missing_skills.append(skill)

    if critical_missing_skills:
        skills_str = ", ".join(f"<strong>{s}</strong>" for s in critical_missing_skills)
        feedback_points.append(f"<strong>Priority Areas:</strong> The job description places a high emphasis on {skills_str}. Focusing on these would significantly boost your alignment.")
    
    if other_missing_skills:
         feedback_points.append(f"<strong>Additional Gaps:</strong> Consider adding or highlighting your experience with: {', '.join(other_missing_skills)}.")

    course_recommendations = []
    for skill in critical_missing_skills + other_missing_skills:
        skill_lower = skill.lower()
        if skill_lower in SUGGESTIONS_DB:
            course_recommendations.append({'skill': skill, 'importance': SUGGESTIONS_DB[skill_lower]['importance'], 'course_link': SUGGESTIONS_DB[skill_lower]['course_link']})
    suggestions['courses'] = course_recommendations

    general_tips = [
        "**Quantify Achievements:** Instead of 'Managed a project,' try 'Managed a 3-month project, delivering it 2 weeks ahead of schedule.' Numbers are powerful.",
        "**Use Action Verbs:** Start each bullet point in your experience section with strong action verbs like 'Developed,' 'Engineered,' 'Managed,' or 'Optimized.'",
        "**Tailor Your Summary:** Customize the summary at the top of your resume to mirror the language and key requirements of the specific job description."
    ]
    if "experience" not in resume_text.lower():
        general_tips.append("**Add an 'Experience' Section:** Ensure you have a clearly defined section for your work experience, even for internships or volunteer roles.")
    suggestions['general'] = general_tips
    return {'points': feedback_points}, suggestions

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html', job_fields=JOB_FIELDS_DB.keys())

@app.route('/extract', methods=['POST'])
def extract():
    resume_text = get_text_from_input('resume_file', 'resume_text')
    if not resume_text: return jsonify({'error': 'No resume content provided.'}), 400
    extracted_skills = extract_skills_from_section(resume_text)
    return jsonify({'extracted_skills': extracted_skills})

@app.route('/analyze', methods=['POST'])
def analyze():
    confirmed_skills = request.form.getlist('confirmed_skills[]')
    resume_text = get_text_from_input('resume_file', 'resume_text')
    jd_text = get_text_from_input('jd_file', 'jd_text')
    selected_field = request.form.get('job_field')
    if not jd_text: return jsonify({'error': 'No job description content provided.'}), 400
    if not selected_field: return jsonify({'error': 'Please select a target job field.'}), 400

    jd_skills = extract_skills(jd_text)
    score_vs_jd, matched_vs_jd, missing_vs_jd = calculate_match_score(confirmed_skills, jd_skills)
    feedback, suggestions = generate_feedback_and_suggestions(score_vs_jd, missing_vs_jd, resume_text, jd_text)

    field_skills = JOB_FIELDS_DB.get(selected_field, [])
    score_vs_field, matched_vs_field, missing_vs_field = calculate_match_score(confirmed_skills, field_skills)

    best_match_score = -1
    best_match_field = "N/A"
    for field, skills in JOB_FIELDS_DB.items():
        score, _, _ = calculate_match_score(confirmed_skills, skills)
        if score > best_match_score:
            best_match_score = score
            best_match_field = field

    result = {
        'jd_analysis': {'score': score_vs_jd, 'matched_skills': matched_vs_jd, 'missing_skills': missing_vs_jd},
        'field_analysis': {'score': score_vs_field, 'matched_skills': matched_vs_field, 'missing_skills': missing_vs_field, 'field_name': selected_field},
        'best_match_analysis': {'score': best_match_score, 'field_name': best_match_field},
        'feedback': feedback,
        'suggestions': suggestions
    }
    return jsonify(result)

# --- Main Execution Block ---
if __name__ == '__main__':
    app.run(debug=True)
