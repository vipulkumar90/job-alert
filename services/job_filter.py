"""
Job filtering service.

Determines whether a job posting matches the user's preferences.
"""

from __future__ import annotations

import logging
from pathlib import Path

import yaml

from models.job_posting import JobPosting

logger = logging.getLogger(__name__)


class JobFilter:
    """Filters jobs according to filters.yaml."""

    CONFIG_PATH = Path("configs") / "filters.yaml"

    def __init__(self) -> None:
        """Load filter configuration."""

        with open(self.CONFIG_PATH, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

        self.keywords = self.config.get("keywords", [])
        self.locations = self.config.get("locations", [])
        self.remote_only = self.config.get("remote_only", False)
        self.companies = self.config.get("companies", [])
        self.excluded = self.config.get("excluded_companies", [])
        self.sources = self.config.get("sources", [])
        self.remote_only = self.config.get("remote_only", False)
        self.visa_sponsorship_only = self.config.get("visa_sponsorship_only", False)
        self.required_technologies = self.config.get("required_technologies", [])

    @staticmethod
    def _contains_any(text: str, values: list[str]) -> bool:
        """
        Return True if text contains any value.
        """

        if not values:
            return True

        text = text.lower()

        return any(value.lower() in text for value in values)

    def matches(self, job: JobPosting) -> bool:
        """
        Check whether a job matches the configured filters.

        Args:
            job: JobPosting object.

        Returns:
            True if the job should continue through the pipeline.
        """

        searchable_text = f"{job.title} " f"{job.description}"

        if not self._contains_any(searchable_text, self.keywords):
            logger.debug(
                "Rejected '%s' (keyword filter).",
                job.title,
            )
            return False

        locations = self.config.get("locations", [])

        if locations and job.location not in locations:
            logger.debug(
                "Rejected '%s' (location filter).",
                job.title,
            )
            return False

        if self.companies and job.company not in self.companies:
            logger.debug(
                "Rejected '%s' (company whitelist).",
                job.title,
            )
            return False

        if job.company in self.excluded:
            logger.debug(
                "Rejected '%s' (company blacklist).",
                job.title,
            )
            return False

        if self.sources and job.source not in self.sources:
            logger.debug(
                "Rejected '%s' (source filter).",
                job.title,
            )
            return False

        if self.remote_only and job.remote_policy.lower() != "remote":
            logger.debug(
                "Rejected '%s' (remote only).",
                job.title,
            )
            return False

        if self.visa_sponsorship_only and not job.visa_sponsorship:
            logger.debug(
                "Rejected '%s' (visa sponsorship).",
                job.title,
            )
            return False

        if self.required_technologies:

            technologies = [tech.lower() for tech in job.technologies]

            for tech in self.required_technologies:
                if tech.lower() not in technologies:
                    logger.debug(
                        "Rejected '%s' (technology filter).",
                        job.title,
                    )
                    return False

        logger.debug(
            "Accepted '%s'.",
            job.title,
        )

        return True
