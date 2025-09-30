<!-- Optional: Add a project banner here -->

<div align="center">
<img src="https://github.com/user-attachments/assets/41d4fd42-ac80-444f-b649-9db0784daaeb" alt="Resume Analyzer Banner" width="800"/>
</div>

<h1 align="center"> Resume Analyzer 📁✨</h1>

<div align="center">
<!-- Badges - Corrected URLs -->
<img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT">
<img src="https://img.shields.io/badge/Python-3.9%2B-brightgreen.svg" alt="Python 3.9+">
<img src="https://img.shields.io/badge/Framework-Flask-orange.svg" alt="Framework: Flask">
</div>

Resume Analyzer is a comprehensive, full-stack web application designed to intelligently score a resume against a job description. Built with a robust Python Flask backend and a dynamic vanilla JavaScript frontend, this tool provides a multi-dimensional analysis to help users understand their job application readiness.

All processing is done locally, ensuring user privacy.

<div align="center">
<h3>Application Demo</h3>
<img src="https://github.com/user-attachments/assets/479fec74-a79d-4ce6-9264-8ed8cb94dd4b" alt="Resume Analyzer Demo" width="800"/>
</div>

## ✨ Core Features
**-Flexible Input Methods:** Provide your resume and job description by uploading a .pdf/.docx file or by pasting the raw text directly.

**-Intelligent Skill Extraction:** The analyzer parses the resume to extract skills only from dedicated sections (like "Skills," "Technical Skills"), avoiding inaccurate matches from general text.

**-Interactive Skill Confirmation:** Users can review the extracted skills in a checkbox grid and deselect any that aren't relevant before the final analysis.

**-Multi-Layered Scoring:** The application calculates three distinct match scores:

  **1. vs. Job Description:** A direct comparison of your skills against the specific job ad.

  **2. vs. Job Field:** A comparison against the standard, expected skills for a selected career path (e.g., "Software Engineer," "Data Analyst").

  **3. Best Career Match:** An analysis of your skills against all defined job fields to recommend the career path you are most qualified for.

## Detailed & Actionable Feedback:

- Identifies "critical" missing skills by analyzing their frequency in the job description.

- Provides multi-point, dynamic feedback on how to improve your alignment.

- Offers suggestions for online courses to fill specific skill gaps.

- Includes general resume improvement tips, like quantifying achievements and using action verbs.

## 🛠️ Tech Stack

**- Backend:** Python, Flask

**- Frontend:** HTML, CSS, Vanilla JavaScript

**- File Parsing:** python-docx, PyMuPDF

## 🚀 Running the Project Locally
Follow these steps to get the application running on your local machine.

### Prerequisites
- Python (3.9+ recommended)
- VS Code (or another code editor)

### Setup Instructions
Clone the repository:
```powershell
git clone [https://github.com/sanjana-halli/resume-analyzer.git](https://github.com/sanjana-halli/resume-analyzer.git)
cd resume-analyzer
```

Open the project in VS Code.

Open the integrated terminal by pressing Ctrl + ~.

Create and activate a virtual environment:

```powershell
# Create the environment
python -m venv venv
```

```powershell
# Activate the environment
.\venv\Scripts\activate
```

You should see (venv) at the start of your terminal prompt.

Install the required packages:

```powershell
pip install -r requirements.txt
```

Run the Flask application:

```powershell
flask run
```

View the app by opening your web browser and navigating to:
http://127.0.0.1:5000

## ✍️ Authors
This project was created by:

Sanjana Halli - https://github.com/sanjana-halli

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
