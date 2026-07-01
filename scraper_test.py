"""
Development utility for testing individual scrapers.

This script is intended for scraper development only.
It bypasses the database, filtering, and Discord notifications.

Responsibilities:
    - Run one scraper.
    - Print discovered jobs.
    - Display useful scraping statistics.
"""

import time

from scrapers.japandev import JapanDevScraper
from scrapers.tokyodev import TokyoDevScraper
from utils.logger import logger

SCRAPERS = {
    "japandev": JapanDevScraper,
    "tokyodev": TokyoDevScraper,
}


def print_job(job, index: int) -> None:
    """Pretty-print a single job."""

    print("=" * 80)
    print(f"Job #{index}")
    print("-" * 80)

    print(f"Title       : {job.title}")
    print(f"Company     : {job.company}")
    print(f"Location    : {job.location}")
    print(f"Salary      : {job.salary}")
    print(f"Remote      : {job.remote_policy}")
    print(f"Japanese    : {job.japanese_level}")
    print(f"Visa        : {job.visa_sponsorship}")
    print(f"Employment  : {job.employment_type}")
    print(f"Team        : {job.team}")
    print(f"Technologies: {', '.join(job.technologies)}")
    print(f"URL         : {job.url}")
    print(f"Source      : {job.source}")

    if job.description:
        print(f"Description : {job.description[:200]}...")

    print()


def main() -> None:

    # ---------------------------------------------------------
    # Choose ONE scraper while developing.
    # ---------------------------------------------------------

    SCRAPER_NAME = "tokyodev"

    scraper = SCRAPERS[SCRAPER_NAME]()

    # ---------------------------------------------------------

    logger.info("Starting scraper test.")

    start = time.perf_counter()

    jobs = scraper.scrape()

    elapsed = time.perf_counter() - start

    logger.info("Scraper returned %d jobs.", len(jobs))

    print("\n")
    print("=" * 80)
    print(f"Scraper : {scraper.__class__.__name__}")
    print(f"Jobs    : {len(jobs)}")
    print(f"Time    : {elapsed:.2f} seconds")
    print("=" * 80)
    print()

    for index, job in enumerate(jobs, start=1):
        print_job(job, index)

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Scraper       : {scraper.__class__.__name__}")
    print(f"Jobs Found    : {len(jobs)}")
    print(f"Execution Time: {elapsed:.2f} sec")
    print("=" * 80)


if __name__ == "__main__":
    main()
