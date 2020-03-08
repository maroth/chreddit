from dataAccess import DataAccess

def get_status():
    db = DataAccess()
    count_unsubmitted = len(db.all_unsubmitted())
    status_message = "unsubmitted items: {0}".format(count_unsubmitted)
    last_submission = db.last_submission().submitted
    status_message += "\nlast submission: {0}".format(last_submission)

    return status_message
