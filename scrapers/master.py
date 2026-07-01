"""
Master scraper for the Job Alert application.

The MasterScraper is responsible for orchestrating all website-specific
scrapers. It executes each scraper, collects the results, and ensures
that a failure in one scraper does not prevent the others from running.
"""

import logging

from models.job_posting import JobPosting
from scrapers.base import BaseScraper
from scrapers.japandev import JapanDevScraper
from scrapers.tokyodev import TokyoDevScraper

logger = logging.getLogger(__name__)


class MasterScraper:
    """
    Executes all registered scrapers and returns a combined list of jobs.

    Responsibilities:
        - Register all website scrapers.
        - Execute each scraper.
        - Continue if one scraper fails.
        - Collect all valid JobPosting objects.
    """

    def __init__(self) -> None:
        """Initialize the list of registered scrapers."""

        self.scrapers: list[BaseScraper] = [
            JapanDevScraper(),
            TokyoDevScraper(),
        ]

    def scrape(self) -> list[JobPosting]:
        """
        Execute all registered scrapers.

        Returns:
            list[JobPosting]:
                Combined list of valid jobs from all scrapers.
        """

        logger.info(
            "Starting MasterScraper with %d scraper(s).",
            len(self.scrapers),
        )

        all_jobs: list[JobPosting] = []

        for scraper in self.scrapers:

            scraper_name = scraper.__class__.__name__

            logger.info("Running %s...", scraper_name)

            try:
                jobs = scraper.scrape()

                # Defensive programming.
                if jobs is None:
                    logger.warning(
                        "%s returned None. Skipping.",
                        scraper_name,
                    )
                    continue

                if not isinstance(jobs, list):
                    logger.warning(
                        "%s returned %s instead of list. Skipping.",
                        scraper_name,
                        type(jobs).__name__,
                    )
                    continue

                valid_jobs = 0

                for job in jobs:

                    if not isinstance(job, JobPosting):
                        logger.warning(
                            "%s returned an invalid object of type %s. Skipping.",
                            scraper_name,
                            type(job).__name__,
                        )
                        continue

                    all_jobs.append(job)
                    valid_jobs += 1

                logger.info(
                    "%s completed successfully (%d job(s)).",
                    scraper_name,
                    valid_jobs,
                )

            except Exception:
                logger.exception(
                    "%s failed unexpectedly.",
                    scraper_name,
                )

        logger.info(
            "MasterScraper finished. Collected %d job(s).",
            len(all_jobs),
        )

        return all_jobs
