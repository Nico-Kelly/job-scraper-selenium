# 🕷️ AutoJob Scraper: Selenium & POM Architecture

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Selenium](https://img.shields.io/badge/Selenium-Web_Scraping-43B02A?style=flat&logo=selenium)
![Architecture](https://img.shields.io/badge/Architecture-POM-purple)
![Status](https://img.shields.io/badge/Status-Work_In_Progress-yellow)

An automated web scraping bot designed to optimize the job hunting process. This project extracts, filters, and organizes job postings (specifically targeting QA Automation and Python Developer roles) from major job boards, saving manual search time and accelerating application rates.

## 🏢 The Business Case

**The Problem:** Manually searching job boards daily for specific IT roles is highly repetitive, time-consuming, and prone to missing early-applicant windows. 
**The Solution:** An automated script that runs autonomously, searches for specific keywords, discards irrelevant postings, and aggregates clean data into a centralized location (Google Sheets).
**ROI (Return on Investment):** Saves approximately 10+ hours per week in manual searching and data entry, while providing a competitive edge by identifying new postings immediately.

## 📐 Architecture: Page Object Model (POM)

To ensure long-term maintainability and scalability, this project strictly adheres to the **Page Object Model (POM)** design pattern. 

Web UI changes frequently. By separating the web interaction logic from the business operations, the bot becomes resilient to DOM updates.
- **Pages Layer:** Classes representing specific web pages (e.g., `LinkedInLoginPage`, `LinkedInPage`). They encapsulate all Selenium locators and web interactions.
- **Services/Utils Layer:** Handles data processing, API interactions (like Google Sheets), and file management.
- **Test/Execution Layer:** The orchestrator scripts that define the behavior flow without caring about the underlying HTML structure.

## ✨ Planned Features

- [ ] **Automated Navigation:** Seamless login and search execution on target job boards.
- [ ] **Dynamic Wait Handling:** Implementation of `WebDriverWait` (Explicit Waits) to handle slow-loading dynamic elements safely.
- [ ] **Smart Filtering:** Keyword-based inclusion (e.g., "QA", "Automation", "Trainee") and exclusion (e.g., "Senior", "Lead") logic.
- [ ] **Data Extraction:** Scraping critical data points: Job Title, Company, Location, Date, and Direct URL.
- [ ] **Data Export:** Automated pipeline to push structured data directly into a Google Sheets CRM.

## 📂 Project Structure

```text
📁 job_scraper
├── 📁 config/                 # Externalized configurations
│   └── settings.json          # URLs, timeouts, and search parameters
├── 📁 pages/                  # Page Object classes (Selenium interactions)
│   ├── base_page.py           # Common wrapper methods with Explicit Waits
│   ├── linkedin_login_page.py # Locators and logic for authentication
│   └── linkedin_page.py       # Locators and logic for job feed navigation
├── 📁 services/               # External integrations
│   └── google_sheets.py       # Google Sheets API connection logic
├── 📁 utils/                  # Helper modules and data cleaners
├── .env                       # Environment variables (Gitignored secrets)
├── Pipfile                    # Virtual environment & dependencies
└── README.md                  # Documentation