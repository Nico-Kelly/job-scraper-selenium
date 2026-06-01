import csv
import os
from utils.models import JobPosting
from utils.logger import get_logger

logger = get_logger(__name__)
class CSVService:
    def __init__(self, folder_name: str, filename: str):
        self.folder_path = os.path.join(os.getcwd(), folder_name)
        os.makedirs(self.folder_path, exist_ok= True)
        self.filepath = os.path.join(self.folder_path, filename)
        self._ensure_file_exist()


    def _ensure_file_exist(self):

        if not os.path.exists(self.filepath):
            with open(self.filepath, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Title", "Company", "Location", "URL"])

    def append_jobs(self, jobs_data: list[JobPosting]):
        if not jobs_data:
            logger.info("no jobs to append")
            return

        try:
            with open(self.filepath, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for job in jobs_data:
                    writer.writerow([job.title, job.company, job.location, job.url])

            logger.info(f"Successfully saved {len(jobs_data)} jobs to {self.filepath}")

        except PermissionError:
            fallback_filepath = self.filepath.replace('.csv', '_backup.csv')
            logger.error(f"'{self.filepath}' is currently opened. Saving in backup file at {fallback_filepath}")

            with open(fallback_filepath, mode= 'a', newline='', encoding='utf-8') as backup_file:
                writer = csv.writer(backup_file)
                for job in jobs_data:
                    writer.writerow([job.title, job.company, job.location, job.url])
                logger.info(f"Successfully saved {len(jobs_data)} jobs to {fallback_filepath}")