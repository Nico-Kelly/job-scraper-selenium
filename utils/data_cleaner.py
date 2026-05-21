class DataCleaner:
    """
    This utility class is dedicated to cleaning and formatting raw strings extracted from the web before they are saved to the JobPosting Model.
    """
    @staticmethod
    def clean_text(raw_text: str) -> str:
        """
        Basically removes extra whitespaces, newlines and tabs from scraped text.
        """

        if not raw_text:
            return ""
        
        return " ".join(raw_text.split())

    @staticmethod
    def extract_company_name(raw_company_text: str) -> str:
        if not raw_company_text:
            return ""

        name = raw_company_text.split('·')[0]
        name = name.split('\n')[0]

        return DataCleaner.clean_text(raw_company_text)