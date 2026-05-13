from utils.models import JobPosting
from utils.logger import get_logger

logger = get_logger(__name__)
class GoogleSheetService:

    def __init__(self, spreadsheet_id: str):
        self.spreadsheet_id = spreadsheet_id
        #TODO
        logger.info("Google Sheets Service initialized")


    def _format_data(self, jobs_data: list[JobPosting]) -> list[list[str]]:
        """
        This private method will transform the list of objects from JobPosting 
        to a format of list of lists that Google Sheet's API requires.
        """
        formatted_data = []

        for job in jobs_data:
            row = [job.title, job.company, job.location, job.url]
            formatted_data.append(row)

        return formatted_data


    def authenticate(self):
        #TODO
        pass

    def append_jobs(self, jobs_data: list):
        #TODO
        pass