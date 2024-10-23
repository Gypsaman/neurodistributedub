from webproject.models import Submissions
def check_duplicate_repo(assignment,repo,user_id):
    # Check if repo already exists
    existing_repo = Submissions.query.filter(
        Submissions.assignment == assignment, 
        Submissions.submission == repo,
        Submissions.user_id != user_id).first()
    if existing_repo:
        return True
    return False

