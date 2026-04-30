from dataclasses import dataclass
from utils.data_cleaner import DataCleaner

@dataclass()
class JobPosting:
    title: str
    company: str
    location: str
    url: str


    def __post_init__(self):

        """
        right after the dataclass assigns the variable values this applies the static methods from DataCleaner before the object
        goes to the Google Sheets service
        :return:
        """
        self.title = DataCleaner.clean_text(self.title)
        self.company = DataCleaner.extract_company_name(self.company)
        self.location = DataCleaner.clean_text(self.location)
