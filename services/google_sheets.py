from utils.models import JobPosting

class GoogleSheetService:

    def __init__(self, spreadsheet_id: str):
        self.spreadsheet_id = spreadsheet_id
        #TODO
        print("Google Sheets Service initialized")


    def _format_data(self, jobs_data: list[JobPosting]) -> list[list[str]]:
        
        """
        This private method will trnasform the list of objects from JobPosting to a format of list of lists that Google Sheet's API requires
        """

        formated_data = []

        for job in jobs_data:
            row = [job.title, job.company, job.location, job.url]
            formated_data.append(row)

        return formated_data


    def authenticate(self):
        #TODO
        pass

    def append_jobs(self, jobs_data: list):
        #TODO
        pass