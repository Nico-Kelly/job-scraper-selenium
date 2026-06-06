# 🕷️ AutoJob Scraper: Selenium & POM Architecture

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Selenium](https://img.shields.io/badge/Selenium-Web_Scraping-43B02A?style=flat&logo=selenium)
![Architecture](https://img.shields.io/badge/Architecture-POM-purple)
![Status](https://img.shields.io/badge/Status-MVP_Completed-success)

An automated web scraping bot designed to optimize the job hunting process. This project extracts, filters, and organizes job postings (specifically targeting QA Automation and Python Developer roles) from major job boards, saving manual search time and accelerating application rates.

## 🏢 The Business Case

**The Problem:** Manually searching job boards daily for specific IT roles is highly repetitive, time-consuming, and prone to missing early-applicant windows. 
**The Solution:** An automated script that runs autonomously, searches for specific keywords, discards irrelevant postings, and aggregates clean data into a centralized location (CSV / Google Sheets).
**ROI (Return on Investment):** Saves approximately 10+ hours per week in manual searching and data entry, while providing a competitive edge by identifying new postings immediately.

## 📐 Architecture: Page Object Model (POM)

To ensure long-term maintainability and scalability, this project strictly adheres to the **Page Object Model (POM)** design pattern. 

Web UI changes frequently. By separating the web interaction logic from the business operations, the bot becomes resilient to DOM updates. Furthermore, pages are modularized by domain to support future multi-platform scaling (e.g., LinkedIn, Computrabajo).
- **Pages Layer:** Classes representing specific web pages, grouped by target website. They encapsulate all Selenium locators and web interactions.
- **Services Layer:** Handles data processing, API interactions (like Google Sheets), and local file management (CSV).
- **Utils Layer:** Core utilities like professional logging, data cleaners, and data models (Dataclasses).
- **Test/Execution Layer:** The orchestrator script (`main_scraper.py`) that defines the behavior flow without caring about the underlying HTML structure.

## ✨ Features & Technical Achievements

- [x] **Automated Navigation:** Seamless login and search execution on target job boards.
- [x] **Dynamic Wait Handling:** Implementation of `WebDriverWait` (Explicit Waits) to handle slow-loading dynamic elements safely.
- [x] **JS Injection for Lazy Loading:** Direct execution of JavaScript (`browser.execute_script`) to bypass lazy-loading mechanisms and force DOM rendering.
- [x] **Data Extraction & Sanitation:** Scraping critical data points and cleaning artifacts in real-time using Data Classes.
- [x] **Agnostic Data Export:** Automated pipeline to push structured data into local CSV files, completely decoupled from specific job boards.
- [x] **Professional Logging:** Centralized system to log execution steps, warnings, and errors.
- [ ] **Smart Filtering:** Keyword-based inclusion and exclusion logic.
- [ ] **Data Export (Cloud):** Automated pipeline to push structured data directly into a Google Sheets CRM.

## 📂 Project Structure

```text
📁 job_scraper
├── 📁 config/                 # Externalized configurations (e.g., settings.json)
├── 📁 pages/                  # Page Object classes (Selenium interactions)
│   ├── base_page.py           # Common wrapper methods with Explicit Waits
│   ├── 📁 computrabajo/       # Locators and logic for Computrabajo (MVP Ready)
│   └── 📁 linkedin/           # Locators and logic for LinkedIn
├── 📁 services/               # Output operations
│   ├── csv_service.py         # Handles CSV creation and appending
│   └── google_sheets.py       # (WIP) Google Sheets API integration
├── 📁 utils/                  # Helper modules
│   ├── data_cleaner.py        # Static methods for text sanitation
│   ├── logger.py              # Custom execution logger
│   └── models.py              # Data structures (JobPosting Dataclass)
├── .env.example               # Template for required environment variables
├── .gitignore
├── Pipfile                    # Pipenv dependencies and Python version
├── Pipfile.lock               # Deterministic builds and dependency resolution
├── main_scraper.py            # Orchestrator and main entry point
└── README.md                  # Documentation