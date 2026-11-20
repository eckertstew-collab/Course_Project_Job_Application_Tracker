
from flask import Flask, render_template
from database import get_db
from flask import Flask, render_template, request, redirect, url_for, flash
import json

app = Flask(__name__)

app.secret_key = "change-this-to-a-random-secret"


# Dashboard route
@app.route('/')
def dashboard():

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # Count companies
    cursor.execute("SELECT COUNT(*) AS count FROM companies")
    companies = cursor.fetchone()

    # Count jobs
    cursor.execute("SELECT COUNT(*) AS count FROM jobs")
    jobs = cursor.fetchone()

    # Count applications
    cursor.execute("SELECT COUNT(*) AS count FROM applications")
    applications = cursor.fetchone()

    # Count contacts
    cursor.execute("SELECT COUNT(*) AS count FROM contacts")
    contacts = cursor.fetchone()

    cursor.close()
    conn.close()

    # Store statistics in a dictionary
    stats = {
        "companies": companies["count"],
        "jobs": jobs["count"],
        "applications": applications["count"],
        "contacts": contacts["count"]
    }

    return render_template("dashboard.html", stats=stats)

# Companies Route
@app.route("/companies", methods=["GET", "POST"])
def companies():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        company_name = request.form.get("company_name", "").strip()

        if not company_name:
            flash("Company name is required.")
        else:
            cursor.execute(
                """
                INSERT INTO companies
                    (company_name, industry, website, city, state, notes)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    company_name,
                    request.form.get("industry") or None,
                    request.form.get("website") or None,
                    request.form.get("city") or None,
                    request.form.get("state") or None,
                    request.form.get("notes") or None,
                ),
            )
            conn.commit()
            flash("Company added.")

        cursor.close()
        conn.close()
        return redirect(url_for("companies"))

    cursor.execute("SELECT * FROM companies ORDER BY company_name")
    company_list = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("companies.html", companies=company_list, editing=None)


@app.route("/companies/<int:company_id>/edit", methods=["GET", "POST"])
def edit_company(company_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        company_name = request.form.get("company_name", "").strip()

        if not company_name:
            flash("Company name is required.")
        else:
            cursor.execute(
                """
                UPDATE companies
                SET company_name = %s, industry = %s, website = %s,
                    city = %s, state = %s, notes = %s
                WHERE company_id = %s
                """,
                (
                    company_name,
                    request.form.get("industry") or None,
                    request.form.get("website") or None,
                    request.form.get("city") or None,
                    request.form.get("state") or None,
                    request.form.get("notes") or None,
                    company_id,
                ),
            )
            conn.commit()
            flash("Company updated.")
            cursor.close()
            conn.close()
            return redirect(url_for("companies"))

    cursor.execute("SELECT * FROM companies ORDER BY company_name")
    company_list = cursor.fetchall()

    cursor.execute(
        "SELECT * FROM companies WHERE company_id = %s",
        (company_id,),
    )
    company = cursor.fetchone()

    cursor.close()
    conn.close()

    if company is None:
        flash("Company not found.")
        return redirect(url_for("companies"))

    return render_template(
        "companies.html",
        companies=company_list,
        editing=company,
    )


@app.route("/companies/<int:company_id>/delete", methods=["POST"])
def delete_company(company_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM jobs WHERE company_id = %s",
        (company_id,),
    )
    job_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM contacts WHERE company_id = %s",
        (company_id,),
    )
    contact_count = cursor.fetchone()[0]

    if job_count or contact_count:
        flash("This company has jobs or contacts. Remove those records first.")
    else:
        cursor.execute(
            "DELETE FROM companies WHERE company_id = %s",
            (company_id,),
        )
        conn.commit()
        flash("Company deleted.")

    cursor.close()
    conn.close()
    return redirect(url_for("companies"))

#jobs route

def read_job_form():
    title = request.form.get("job_title", "").strip()
    company_id = request.form.get("company_id", "").strip()
    salary_min = request.form.get("salary_min", "").strip()
    salary_max = request.form.get("salary_max", "").strip()
    requirements_text = request.form.get("requirements", "").strip() or "[]"

    if not title:
        raise ValueError("Job title is required.")
    if not company_id:
        raise ValueError("Please select a company.")

    try:
        company_id = int(company_id)
        salary_min = int(salary_min) if salary_min else None
        salary_max = int(salary_max) if salary_max else None
    except ValueError:
        raise ValueError("Company ID and salary amounts must be valid numbers.")

    try:
        requirements = json.loads(requirements_text)
    except json.JSONDecodeError:
        raise ValueError('Requirements must be valid JSON, for example: ["Python", "SQL"]')

    if not isinstance(requirements, list):
        raise ValueError("Requirements must be a JSON list, such as [\"Python\", \"SQL\"].")

    return (
        company_id,
        title,
        request.form.get("job_type") or None,
        salary_min,
        salary_max,
        request.form.get("job_url") or None,
        request.form.get("date_posted") or None,
        json.dumps(requirements),
    )


@app.route("/jobs", methods=["GET", "POST"])
def jobs():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        try:
            job_data = read_job_form()
        except ValueError as error:
            flash(str(error))
            cursor.close()
            conn.close()
            return redirect(url_for("jobs"))

        cursor.execute(
            """
            INSERT INTO jobs
                (company_id, job_title, job_type, salary_min, salary_max,
                 job_url, date_posted, requirements)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            job_data,
        )
        conn.commit()
        flash("Job added.")
        cursor.close()
        conn.close()
        return redirect(url_for("jobs"))

    cursor.execute(
        """
        SELECT jobs.*, companies.company_name
        FROM jobs
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY jobs.job_id DESC
        """
    )
    job_list = cursor.fetchall()

    cursor.execute("SELECT company_id, company_name FROM companies ORDER BY company_name")
    company_list = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template(
        "jobs.html",
        jobs=job_list,
        companies=company_list,
        editing=None,
    )


@app.route("/jobs/<int:job_id>/edit", methods=["GET", "POST"])
def edit_job(job_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        try:
            job_data = read_job_form()
        except ValueError as error:
            flash(str(error))
            cursor.close()
            conn.close()
            return redirect(url_for("edit_job", job_id=job_id))

        cursor.execute(
            """
            UPDATE jobs
            SET company_id = %s, job_title = %s, job_type = %s,
                salary_min = %s, salary_max = %s, job_url = %s,
                date_posted = %s, requirements = %s
            WHERE job_id = %s
            """,
            job_data + (job_id,),
        )
        conn.commit()
        flash("Job updated.")
        cursor.close()
        conn.close()
        return redirect(url_for("jobs"))

    cursor.execute("SELECT * FROM jobs WHERE job_id = %s", (job_id,))
    job = cursor.fetchone()

    cursor.execute("SELECT company_id, company_name FROM companies ORDER BY company_name")
    company_list = cursor.fetchall()

    cursor.execute(
        """
        SELECT jobs.*, companies.company_name
        FROM jobs
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY jobs.job_id DESC
        """
    )
    job_list = cursor.fetchall()

    cursor.close()
    conn.close()

    if job is None:
        flash("Job not found.")
        return redirect(url_for("jobs"))

    return render_template(
        "jobs.html",
        jobs=job_list,
        companies=company_list,
        editing=job,
    )


@app.route("/jobs/<int:job_id>/delete", methods=["POST"])
def delete_job(job_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE job_id = %s",
        (job_id,),
    )
    application_count = cursor.fetchone()[0]

    if application_count:
        flash("This job has applications. Remove those applications first.")
    else:
        cursor.execute("DELETE FROM jobs WHERE job_id = %s", (job_id,))
        conn.commit()
        flash("Job deleted.")

    cursor.close()
    conn.close()
    return redirect(url_for("jobs"))


    #applications route


# applications helper
def read_application_form():
    job_id = request.form.get("job_id", "").strip()
    application_date = request.form.get("application_date", "").strip()
    interview_text = request.form.get("interview_data", "").strip() or "{}"

    if not job_id:
        raise ValueError("Please select a job.")
    if not application_date:
        raise ValueError("Application date is required.")

    try:
        job_id = int(job_id)
    except ValueError:
        raise ValueError("Please select a valid job.")

    try:
        interview_data = json.loads(interview_text)
    except json.JSONDecodeError:
        raise ValueError(
            'Interview data must be valid JSON, for example: {"round": 1}'
        )

    if not isinstance(interview_data, dict):
        raise ValueError(
            'Interview data must be a JSON object, for example: {"round": 1}'
        )

    return (
        job_id,
        application_date,
        request.form.get("status") or None,
        request.form.get("resume_version") or None,
        1 if request.form.get("cover_letter_sent") == "on" else 0,
        json.dumps(interview_data),
    )


@app.route("/applications", methods=["GET", "POST"])
def applications():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        try:
            application_data = read_application_form()
        except ValueError as error:
            flash(str(error))
            cursor.close()
            conn.close()
            return redirect(url_for("applications"))

        cursor.execute(
            """
            INSERT INTO applications
                (job_id, application_date, status, resume_version,
                 cover_letter_sent, interview_data)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            application_data,
        )
        conn.commit()
        flash("Application added.")
        cursor.close()
        conn.close()
        return redirect(url_for("applications"))

    cursor.execute(
        """
        SELECT applications.*, jobs.job_title, companies.company_name
        FROM applications
        JOIN jobs ON applications.job_id = jobs.job_id
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY applications.application_date DESC
        """
    )
    application_list = cursor.fetchall()

    cursor.execute(
        """
        SELECT jobs.job_id, jobs.job_title, companies.company_name
        FROM jobs
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY companies.company_name, jobs.job_title
        """
    )
    job_list = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template(
        "applications.html",
        applications=application_list,
        jobs=job_list,
        editing=None,
    )


@app.route("/applications/<int:application_id>/edit", methods=["GET", "POST"])
def edit_application(application_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        try:
            application_data = read_application_form()
        except ValueError as error:
            flash(str(error))
            cursor.close()
            conn.close()
            return redirect(
                url_for("edit_application", application_id=application_id)
            )

        cursor.execute(
            """
            UPDATE applications
            SET job_id = %s, application_date = %s, status = %s,
                resume_version = %s, cover_letter_sent = %s,
                interview_data = %s
            WHERE application_id = %s
            """,
            application_data + (application_id,),
        )
        conn.commit()
        flash("Application updated.")
        cursor.close()
        conn.close()
        return redirect(url_for("applications"))

    cursor.execute(
        "SELECT * FROM applications WHERE application_id = %s",
        (application_id,),
    )
    application = cursor.fetchone()

    cursor.execute(
        """
        SELECT jobs.job_id, jobs.job_title, companies.company_name
        FROM jobs
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY companies.company_name, jobs.job_title
        """
    )
    job_list = cursor.fetchall()

    cursor.execute(
        """
        SELECT applications.*, jobs.job_title, companies.company_name
        FROM applications
        JOIN jobs ON applications.job_id = jobs.job_id
        JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY applications.application_date DESC
        """
    )
    application_list = cursor.fetchall()

    cursor.close()
    conn.close()

    if application is None:
        flash("Application not found.")
        return redirect(url_for("applications"))

    return render_template(
        "applications.html",
        applications=application_list,
        jobs=job_list,
        editing=application,
    )


@app.route("/applications/<int:application_id>/delete", methods=["POST"])
def delete_application(application_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM applications WHERE application_id = %s",
        (application_id,),
    )
    conn.commit()

    cursor.close()
    conn.close()
    flash("Application deleted.")
    return redirect(url_for("applications"))

#contacts route

@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        contact_name = request.form.get("contact_name", "").strip()
        company_id = request.form.get("company_id", "").strip()

        if not contact_name or not company_id:
            flash("Contact name and company are required.")
        else:
            try:
                company_id = int(company_id)
                cursor.execute(
                    """
                    INSERT INTO contacts
                        (company_id, contact_name, title, email, phone,
                         linkedin_url, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        company_id,
                        contact_name,
                        request.form.get("title") or None,
                        request.form.get("email") or None,
                        request.form.get("phone") or None,
                        request.form.get("linkedin_url") or None,
                        request.form.get("notes") or None,
                    ),
                )
                conn.commit()
                flash("Contact added.")
            except ValueError:
                flash("Please select a valid company.")

        cursor.close()
        conn.close()
        return redirect(url_for("contacts"))

    cursor.execute(
        """
        SELECT contacts.*, companies.company_name
        FROM contacts
        JOIN companies ON contacts.company_id = companies.company_id
        ORDER BY contacts.contact_name
        """
    )
    contact_list = cursor.fetchall()

    cursor.execute("SELECT company_id, company_name FROM companies ORDER BY company_name")
    company_list = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template(
        "contacts.html",
        contacts=contact_list,
        companies=company_list,
        editing=None,
    )


@app.route("/contacts/<int:contact_id>/edit", methods=["GET", "POST"])
def edit_contact(contact_id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        contact_name = request.form.get("contact_name", "").strip()
        company_id = request.form.get("company_id", "").strip()

        if not contact_name or not company_id:
            flash("Contact name and company are required.")
        else:
            try:
                company_id = int(company_id)
                cursor.execute(
                    """
                    UPDATE contacts
                    SET company_id = %s, contact_name = %s, title = %s,
                        email = %s, phone = %s, linkedin_url = %s, notes = %s
                    WHERE contact_id = %s
                    """,
                    (
                        company_id,
                        contact_name,
                        request.form.get("title") or None,
                        request.form.get("email") or None,
                        request.form.get("phone") or None,
                        request.form.get("linkedin_url") or None,
                        request.form.get("notes") or None,
                        contact_id,
                    ),
                )
                conn.commit()
                flash("Contact updated.")
                cursor.close()
                conn.close()
                return redirect(url_for("contacts"))
            except ValueError:
                flash("Please select a valid company.")

    cursor.execute("SELECT * FROM contacts WHERE contact_id = %s", (contact_id,))
    contact = cursor.fetchone()

    cursor.execute("SELECT company_id, company_name FROM companies ORDER BY company_name")
    company_list = cursor.fetchall()

    cursor.execute(
        """
        SELECT contacts.*, companies.company_name
        FROM contacts
        JOIN companies ON contacts.company_id = companies.company_id
        ORDER BY contacts.contact_name
        """
    )
    contact_list = cursor.fetchall()

    cursor.close()
    conn.close()

    if contact is None:
        flash("Contact not found.")
        return redirect(url_for("contacts"))

    return render_template(
        "contacts.html",
        contacts=contact_list,
        companies=company_list,
        editing=contact,
    )


@app.route("/contacts/<int:contact_id>/delete", methods=["POST"])
def delete_contact(contact_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM contacts WHERE contact_id = %s", (contact_id,))
    conn.commit()

    cursor.close()
    conn.close()
    flash("Contact deleted.")
    return redirect(url_for("contacts"))

#Job Match Route

@app.route("/job-match", methods=["GET", "POST"])
def job_match():
    entered_skills = []
    matches = []

    if request.method == "POST":
        skills_text = request.form.get("skills", "")
        entered_skills = [
            skill.strip()
            for skill in skills_text.split(",")
            if skill.strip()
        ]
        user_skills = {skill.casefold() for skill in entered_skills}

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT jobs.*, companies.company_name
            FROM jobs
            JOIN companies ON jobs.company_id = companies.company_id
            """
        )
        job_list = cursor.fetchall()
        cursor.close()
        conn.close()

        for job in job_list:
            requirements = job.get("requirements") or []

            if isinstance(requirements, str):
                try:
                    requirements = json.loads(requirements)
                except json.JSONDecodeError:
                    requirements = []

            if not isinstance(requirements, list):
                requirements = []

            required_skills = [
                str(skill).strip()
                for skill in requirements
                if str(skill).strip()
            ]

            matched_skills = [
                skill for skill in required_skills
                if skill.casefold() in user_skills
            ]
            missing_skills = [
                skill for skill in required_skills
                if skill.casefold() not in user_skills
            ]

            percentage = (
                round(len(matched_skills) / len(required_skills) * 100)
                if required_skills
                else None
            )

            matches.append({
                "job": job,
                "required_skills": required_skills,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "percentage": percentage,
            })

        matches.sort(
            key=lambda item: (
                item["percentage"] is None,
                -(item["percentage"] or 0),
                item["job"]["job_title"].casefold(),
            )
        )

    return render_template(
        "job_match.html",
        entered_skills=", ".join(entered_skills),
        matches=matches,
        searched=request.method == "POST",
    )



if __name__ == '__main__':
    app.run(debug=True)
