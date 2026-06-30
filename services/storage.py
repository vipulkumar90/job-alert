import hashlib
import sqlite3
import warnings

from database.db import get_connection
from models.job_posting import JobPosting
from utils.logger import logger

"""
DEPRECATED

This service has been replaced by JobRepository.

It is kept temporarily for backwards compatibility and will be removed
after all code has been migrated.
"""

"""
Storage service for JobPosting objects.

Responsibilities:
    - Generate a unique hash for each job.
    - Check whether a job already exists.
    - Save new jobs to the database.
"""


class Storage:
    """Handles storing jobs in the SQLite database."""

    def __init__(self):
        warnings.warn(
            "Storage is deprecated. Use JobRepository instead.",
            DeprecationWarning,
            stacklevel=2,
        )

    @staticmethod
    def generate_hash(job: JobPosting) -> str:
        """
        Generate a SHA256 hash for a job posting.

        The hash is based on:
            - Company
            - Job title
            - Job URL

        These fields uniquely identify a job while ignoring fields that
        may change over time (description, posted date, etc.).
        """

        text = (
            job.company.strip().lower()
            + job.title.strip().lower()
            + job.url.strip().lower()
        )

        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def job_exists(self, job_hash: str) -> bool:
        """
        Check whether a job already exists in the database.

        Args:
            job_hash: SHA256 hash of the job.

        Returns:
            True if the job already exists, otherwise False.
        """

        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT 1 FROM jobs WHERE hash = ?",
                (job_hash,),
            )

            return cursor.fetchone() is not None

    def save(self, job: JobPosting) -> bool:
        """
        Save a job if it does not already exist.

        Args:
            job: JobPosting object.

        Returns:
            True if the job was inserted.
            False if it already existed.
        """

        job_hash = self.generate_hash(job)
        logger.debug("Saving job '%s'", job.title)

        if self.job_exists(job_hash):
            logger.debug("Duplicate skipped '%s'", job.title)
            return False

        try:
            with get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO jobs (
                        title,
                        company,
                        location,
                        url,
                        description,
                        posted_date,
                        source,
                        hash
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        job.title,
                        job.company,
                        job.location,
                        job.url,
                        job.description,
                        job.posted_date,
                        job.source,
                        job_hash,
                    ),
                )

                conn.commit()

            return True

        except sqlite3.Error:
            logger.exception
            ("Failed to insert job '%s'", job.title)
            return False

    def save_all(self, jobs: list[JobPosting]) -> int:
        """
        Save multiple jobs.

        Args:
            jobs: List of JobPosting objects.

        Returns:
            Number of newly inserted jobs.
        """

        new_jobs = []

        for job in jobs:
            if self.save(job):
                new_jobs.append(job)

        logger.info("%d new jobs inserted", len(new_jobs))

        return new_jobs
