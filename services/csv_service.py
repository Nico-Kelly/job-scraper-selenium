import csv
import os
from utils.models import JobPosting

class CSVService:
    def __init__(self, filename: str):
        self.filepath = os.path.join(os.getcwd(), filename)
        self._ensure_file_exist()

    # Fijate cómo ahora están alineados a la izquierda, al nivel del __init__
    def _ensure_file_exist(self):
        # Corregido: exists con 's'
        if not os.path.exists(self.filepath):
            with open(self.filepath, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Title", "Company", "Location", "URL"])

    def append_jobs(self, jobs_data: list[JobPosting]):
        if not jobs_data:
            print("No jobs to append")
            return

        with open(self.filepath, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for job in jobs_data:
                writer.writerow([job.title, job.company, job.location, job.url])

        print(f"Successfully saved {len(jobs_data)} jobs to {self.filepath}")