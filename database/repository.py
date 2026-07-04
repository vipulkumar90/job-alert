"""
Repository for persisting JobPosting objects.

This module is the only place in the application that should contain SQL.
"""

from __future__ import annotations

import hashlib
import sqlite3

from config import DATABASE_PROVIDER
from database.connection import get_connection, placeholder
from models.job_posting import JobPosting
from utils.logger import logger

PLACEHOLDER = "%s" if DATABASE_PROVIDER == "postgres" else "?"


class JobRepository:
    """Provides CRUD operations for JobPosting objects."""

    def __init__(self) -> None:
        """Create a single database connection."""

        self.conn = get_connection()

    @staticmethod
    def generate_hash(job: JobPosting) -> str:
        """
        Generate a deterministic SHA256 hash for a job posting.
        """

        value = (
            job.company.strip().lower()
            + job.title.strip().lower()
            + job.url.strip().lower()
        )

        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    def exists(self, job_hash: str) -> bool:
        """
        Check whether a job already exists.

        Args:
            job_hash: SHA256 hash.

        Returns:
            True if the job exists.
        """
        logger.debug("Checking if job exists.")
        try:

            cursor = self.conn.cursor()

            cursor.execute(
                f"SELECT 1 FROM jobs WHERE hash = {PLACEHOLDER}",
                (job_hash,),
            )
            exists = cursor.fetchone() is not None

            logger.debug("Job exists: %s", exists)

            return exists

        except sqlite3.Error:
            logger.exception("Failed to check if job exists.")
            raise

    def save(self, job: JobPosting) -> bool:
        """
        Save a job if it does not already exist.

        Returns:
            True if inserted.
            False if duplicate.
        """
        logger.debug("Saving job '%s'.", job.title)

        try:
            job_hash = self.generate_hash(job)

            cursor = self.conn.cursor()

            if DATABASE_PROVIDER == "postgres":
                sql = f"""
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
                    VALUES ({placeholder(8)})
                    ON CONFLICT (hash) DO NOTHING
                """
            else:
                sql = f"""
                    INSERT OR IGNORE INTO jobs (
                        title,
                        company,
                        location,
                        url,
                        description,
                        posted_date,
                        source,
                        hash
                    )
                    VALUES ({placeholder(8)})
                """

            cursor.execute(
                sql,
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

            self.conn.commit()

            if cursor.rowcount == 0:
                logger.info("Duplicate skipped: %s", job.title)
                return False

            logger.info("Saved '%s'", job.title)
            return True

        except sqlite3.Error:
            logger.exception(
                "Failed to save job '%s'.",
                job.title,
            )
            raise

    def get(self, job_hash: str) -> JobPosting | None:
        """
        Retrieve a single job by hash.
        """
        logger.info("Fetching a job")

        try:

            cursor = self.conn.cursor()

            cursor.execute(
                f"""
                SELECT
                    title,
                    company,
                    location,
                    url,
                    description,
                    posted_date,
                    source
                FROM jobs
                WHERE hash = {PLACEHOLDER}
                """,
                (job_hash,),
            )

            row = cursor.fetchone()

            if row is None:
                return None

            return JobPosting(
                title=row[0],
                company=row[1],
                location=row[2],
                url=row[3],
                description=row[4],
                posted_date=row[5],
                source=row[6],
            )

        except sqlite3.Error:
            logger.exception(
                "Failed to get job.",
            )
            raise

    def get_all(self) -> list[JobPosting]:
        """
        Retrieve all jobs.
        """
        logger.debug("Fetching all jobs.")

        jobs: list[JobPosting] = []

        try:

            cursor = self.conn.cursor()

            cursor.execute("""
                SELECT
                    title,
                    company,
                    location,
                    url,
                    description,
                    posted_date,
                    source
                FROM jobs
                """)

            rows = cursor.fetchall()

            for row in rows:
                jobs.append(
                    JobPosting(
                        title=row[0],
                        company=row[1],
                        location=row[2],
                        url=row[3],
                        description=row[4],
                        posted_date=row[5],
                        source=row[6],
                    )
                )

            return jobs

        except sqlite3.Error:
            logger.exception("Failed to retrieve jobs.")
            raise

    def delete(self, job_hash: str) -> None:
        """
        Delete a job by hash.
        """
        logger.info("Deleting job.")

        try:

            cursor = self.conn.cursor()

            cursor.execute(
                f"DELETE FROM jobs WHERE hash = {PLACEHOLDER}",
                (job_hash,),
            )

            self.conn.commit()
        except sqlite3.Error:
            logger.exception("Failed to delete job.")
            raise

    def update(self, job: JobPosting) -> None:
        """
        Update an existing job.
        """
        logger.info("Updating job '%s'.", job.title)

        job_hash = self.generate_hash(job)
        try:

            cursor = self.conn.cursor()

            cursor.execute(
                f"""
                UPDATE jobs
                SET
                    title = {PLACEHOLDER},
                    company = {PLACEHOLDER},
                    location = {PLACEHOLDER},
                    url = {PLACEHOLDER},
                    description = {PLACEHOLDER},
                    posted_date = {PLACEHOLDER},
                    source = {PLACEHOLDER}
                WHERE hash = {PLACEHOLDER}
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

            self.conn.commit()

        except sqlite3.Error:
            logger.exception(
                "Failed to update '%s'.",
                job.title,
            )
            raise

    def delete_all(self) -> None:
        try:

            self.conn.execute("DELETE FROM jobs")
            self.conn.commit()
            logger.info("[DEV ONLY] ALL ROWS HAS BEEN DELETED")
        except sqlite3.Error:
            logger.exception("Failed to update delete all rows")
            raise

    def close(self) -> None:
        """Close the database connection."""

        self.conn.close()
        logger.debug("Database connection closed.")
