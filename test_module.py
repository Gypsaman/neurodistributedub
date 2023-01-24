from graders import check_submissions
from data import registered

# check_submissions.check_submissions()
# registered.update_registered()
not_registered = registered.not_registered('SP23-Monday',True)
print(len(not_registered))
print(not_registered)