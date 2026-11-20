# AI Usage Documentation

## Tools Used
- ChatGPT (GPT-4) for Flask routes and SQL queries
- Claude for debugging and code review

## Key Prompts
1.  I'm creating a job application tracker that has the following requirements. Database: MySQL,  Backend: Python 3 with Flask, Frontend: HTML, CSS (Bootstrap optional)  I already created my database and 4 tables (companies, jobs, applications, and contacts) with schema.sql. Each table needs to, create: forms to add new records, read: lists and details views, Update: Edit forms for existing records, Delete: Remove with confirmation. There needs to be 6 pages that do the following 1.    Dashboard: Statistics overview, Companies: List/Add/Edit/Delete, Jobs: List/Add/Edit/Delete, Applications: List/Add/Edit/Delete, Contacts: List/Add/Edit/Delete, Job Match: Skills matching feature. I'm creating a job application tracker that has the following requirements. Database: MySQL,  Backend: Python 3 with Flask, Frontend: HTML, CSS (Bootstrap optional)  I already created my database and 4 tables (companies, jobs, applications, and contacts) each table needs, create: forms to add new records, read: lists and details views, Update: Edit forms for existing records, Delete: Remove with confirmation. There needs to be 6 pages that do the following 1.    Dashboard: Statistics overview, Companies: List/Add/Edit/Delete, Jobs: List/Add/Edit/Delete, Applications: List/Add/Edit/Delete, Contacts: List/Add/Edit/Delete, Job Match: Skills matching feature. Here is the following project structure for the job_tracker_2 folder. I am also providing a example for the app.py structure using a txt file                                                                                                             job_tracker_2/

├── app.py              # Main Flask application

├── database.py         # Database connection functions

├── templates/          # HTML templates

│   ├── base.html

│   ├── dashboard.html

│   ├── companies.html

│   ├── jobs.html

│   ├── applications.html

│   ├── contacts.html

│   └── job_match.html

├── static/             # CSS, images

│   └── style.css

├── schema.sql          # Database creation script

├── AI_USAGE.md         # GenAI documentation

├── README.md           # Project description
  └── requirements.txt    # Python dependencies Here is the following project structure for the job_tracker_2 folder                                                                      job_tracker_2/

├── app.py              # Main Flask application

├── database.py         # Database connection functions

├── templates/          # HTML templates

│   ├── base.html

│   ├── dashboard.html

│   ├── companies.html

│   ├── jobs.html

│   ├── applications.html

│   ├── contacts.html

│   └── job_match.html

├── static/             # CSS, images

│   └── style.css

├── schema.sql          # Database creation script

├── AI_USAGE.md         # GenAI documentation

├── README.md           # Project description
  └── requirements.txt    # Python dependencies                                                                                                     

## What Worked Well
- GPT Luna-6 was very effective at completing the CRUD Routes in app.py and forming the html and css files.
- It also provided clear instructions for installing flask and connecting python to MySQL
- 

## What I Modified
- Added more comments to the py, html, and css files
-deleted notes from the companies page because it was unnecessary 

## Lessons Learned
- AI coding was very effective for this assignment and was very helpful when something was not working correctly the chatbot was usually able to help assist with any modifications i wanted to make.
