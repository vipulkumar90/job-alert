"""
Defines the base interface for all job scrapers.

Every website scraper must inherit from BaseScraper and implement the
scrape() method. This guarantees that all scrapers return data in the
same format, allowing the rest of the application to remain independent
of the source website.
"""

from abc import ABC, abstractmethod

from models.job_posting import JobPosting


class BaseScraper(ABC):
    """
    Abstract base class for all job scrapers.
    """

    @abstractmethod
    def scrape(self) -> list[JobPosting]:
        """
        Scrape job postings from a website.

        Returns:
            list[JobPosting]:
                A list of normalized JobPosting objects.
                Returns an empty list if no jobs are found.
        """
        pass
