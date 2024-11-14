import json

from webproject import create_app, db
from webproject.models import Assignments, Grades, Quiz_Header, Quizzes, User, Wallet
from webproject.modules.ubemail import UBEmail

letter_grades = {
    "A": (94.9, 100),
    "A-": (90, 94.8),
    "B+": (87, 89.9),
    "B": (83, 86.9),
    "B-": (80, 82.9),
    "C+": (77, 79.9),
    "C": (73, 76.9),
    "C-": (70, 72.9),
    "D+": (67, 69.9),
    "D": (63, 66.9),
    "D-": (60, 62.9),
    "F": (0, 59.9),
}


additional_extra_credit = []
grade_portion = {"Assignment": 40 / 16, "Midterm": 15, "Final": 15, "Extra Credit": 2}


def get_letter_grades(score):
    score = round(score, 1)
    for key, value in letter_grades.items():
        if score >= value[0] and score <= value[1]:
            return key
    return "F"


def final_grades_student(id):
    user = User.query.filter_by(id=id).first()

    grades = {"Assignment": {}, "Midterm": {}, "Final": {}, "Extra Credit": {}}
    assignments = Assignments.query.all()
    for assignment in assignments:
        grade = Grades.query.filter_by(user_id=id, assignment=assignment.id).first()
        score = 0 if grade is None else max(0, grade.grade)
        name = assignment.name.strip()
        if assignment.grade_category == "Midterm":
            if score == 0:
                continue
            name = "Mid Term"
        grades[assignment.grade_category][name] = {
            "score": score,
            "grade_portion": score/100 * grade_portion[assignment.grade_category],
        }
    if not 'Mid Term' in grades['Midterm']:
        grades['Midterm']['Mid Term'] = {"score": 0, "grade_portion": 0}

    if user.student_id in additional_extra_credit:
        grades["Extra Credit"].append(("Additional Extra Credit", score, 2))
    quizzes = Quizzes.query.filter_by(user_id=id).all()
    for quiz in quizzes:
        header = Quiz_Header.query.filter_by(id=quiz.quiz_header).first()
        if header.description == 'Do not Use':
            continue
        score = 0 if quiz.grade is None else quiz.grade
        grades[header.grade_category][f"{header.description}-Quiz"] = {
            "score": score,
            "grade_portion": score /100 * grade_portion[header.grade_category],
        }

    return grades
       
            

def publish_final_grades(type="Preview", email=False):
    grades = []

    for user in User.query.filter_by(role="student",section=1).all():
        # if user.student_id == '1187694':
        #     continue
        final_grades = final_grades_student(user.id)
        msg, grade = final_grade_message(final_grades, user, grades_due='April 22, 2024',type=type)
        if email:
            email = UBEmail()
            email.send_email(user.email, "Final Grades", msg)
        grades.append(
            {
                "id": user.id,
                "grade": grade,
                "Letter_grade":get_letter_grades(grade),
                "student_id": user.student_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "section": user.section,
            }
        )

    return grades


def final_grade_message(final_grades, user, grades_due, type="FINAL"):
    msg = f"Hello {user.first_name} ({user.student_id})\n\n"
    if type == "Preview":
        msg += "This is a preview of your final grade.\n"
        msg += f"Final Grades are due on {grades_due}\n"
        msg += "Please let me know if I have made any mistakes.\n\n"
    msg += "As a reminder, the final grade is calculated as follows:\n"
    msg += "Assignments and Quizzes: 40%\n"
    msg += "Midterm: 30%\n"
    msg += "Final: 30%\n\n"
    msg += "Extra Credit: 2%\n\n"

    msg += f"Your grades are as follows:\n\n"

    overall_total = 0
    for type, grades in final_grades.items():
        msg = msg + type + "\n"
        msg = msg + "-" * len(type) + "\n"
        type_total = 0
        for grade in grades:
            msg += f"{grade.strip()}: {grades[grade]['score']:.0f}\n"
            type_total += grades[grade]["grade_portion"]
        msg += f"\nGrade: {type_total:.2f}%\n\n"
        overall_total += type_total
    overall_total = min(overall_total, 100)
    msg += f"FINAL GRADE: {overall_total:.2f}% ({get_letter_grades(overall_total)})"
    return msg, overall_total


def course_evaluation_email():
    with create_app().app_context():
        users = User.query.filter_by(role="student").all()
        for user in users:
            msg = f"Hello {user.first_name.title()},\n\n"
            msg += "I want to thank you for participating in the course this semester. I hope you found the course interesting and useful. If you haven't done so already, I would like to ask you to take a few minutes to fill out a course evaluation. The course evaluation is anonymous and will help me improve the course for future semesters.\n\n"
            msg += "Thank you\n\nCesar Garcia"
            email = UBEmail()
            email.send_email(user.email, "Course Evaluation", msg)


def get_student_grades():
    with create_app().app_context():
        for assgn in Assignments.query.all():
            assgn.name = assgn.name.strip()
        db.session.commit()
        all_students = {}

        for user in User.query.filter_by(role="student").all():
            final_grades = final_grades_student(user.id)
            final_grades["email"] = user.email
            final_grades["section"] = user.section
            wallet = Wallet.query.filter_by(user_id=user.id).first()
            final_grades["wallet"] = wallet.wallet if wallet else ""

            all_students[user.student_id] = final_grades

        json.dump(all_students, open("summary.json", "w"), indent=4)


def build_grades(get_grades=True):
    if get_grades:
        get_student_grades()
    grade_csv()


def grade_csv():
    all_students = json.load(open("summary.json", "r"))
    for student_id, student in all_students.items():
        for assgn, scores in student["Midterm"].items():
            if (
                assgn in ["Mid Term", "Mid Term 2", "Mid Term 3"]
                and scores["score"] > 0
            ):
                student["Midterm"]["Mid Term"] = scores

    columns = {"Assignment": [], "Midterm": [], "Final": [], "Extra Credit": []}
    with create_app().app_context():
        for header in Quiz_Header.query.all():
            columns[header.grade_category].append(f"{header.description}-Quiz")
        for assignment in Assignments.query.all():
            if assignment.grade_category in "Midterm" and assignment.name != "Mid Term":
                continue
            columns[assignment.grade_category].append(assignment.name)

    with open("grade_details.csv", "w") as f:
        header = "section,Student ID,email,wallet"
        for grade_category in columns:
            for col in columns[grade_category]:
                header += f",{col}"
        f.write(f"{header}\n")
        for student_id, student in all_students.items():
            data = f"{student['section']},{student_id},{student['email']},{student['wallet']}"
            for grade_category in columns:
                for col in columns[grade_category]:
                    data += ","
                    data += (
                        str(student[grade_category][col]["score"])
                        if col in student[grade_category]
                        else ""
                    )
            data += "\n"
            f.write(data)


def is_this_function_duplicate():
    with create_app().app_context():
        with open("grades.csv", "w") as f:
            final_grades = final_grades_student(1)
            header = []
            for key in final_grades["Assignment"]:
                header.append(key)
            for key in final_grades["Midterm"]:
                header.append(key)
            for key in final_grades["Final"]:
                header.append(key)
            for key in final_grades["Extra Credit"]:
                header.append(key)
            f.write(f'section,student_id,email,{",".join(header)}\n')

            for user in User.query.filter_by(role="student").all():
                grades = []
                final_grades = final_grades_student(user.id)
                for key, item in final_grades["Assignment"].items():
                    grades.append(item["score"])
                for key, item in final_grades["Midterm"].items():
                    grades.append(item["score"])
                for key, item in final_grades["Final"].items():
                    grades.append(item["score"])
                for key, item in final_grades["Extra Credit"].items():
                    grades.append(item["score"])
                string = "".join([str(x) + "," for x in grades])
                f.write(f"{user.section},e{user.student_id},{user.email},{string}\n")
