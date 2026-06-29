# Job Alert

A Python application that automatically monitors multiple Japanese job websites and sends Discord notifications whenever new job postings appear.

## Features

* Monitor multiple job websites
* Website-specific scrapers
* Normalize job data into a common format
* Detect duplicate jobs
* Store jobs in SQLite
* Discord notifications for new postings
* Scheduled automatic execution

## Tech Stack

* Python
* Playwright
* BeautifulSoup
* Requests
* SQLite
* APScheduler
* Discord Webhooks

## Project Structure

```
job-alert/
├── app.py
├── config.py
├── database/
├── models/
├── scrapers/
├── services/
└── utils/
```

## Current Status

🚧 Work in progress.

The initial version focuses on quickly delivering a functional end-to-end pipeline before adding advanced features such as resume matching, job scoring, Docker support, and PostgreSQL.

## License

Personal project.
