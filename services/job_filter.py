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

        logger.info("Loading job filter configuration...")

        with open(self.CONFIG_PATH, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

        self.keywords = self.config.get("keywords", [])
        self.locations = self.config.get("locations", [])
        self.remote_only = self.config.get("remote_only", False)
        self.companies = self.config.get("companies", [])
        self.excluded = self.config.get("excluded_companies", [])
        self.sources = self.config.get("sources", [])
        self.remote_only = self.config.get("remote_only", False)
        self.visa_sponsorship_only = self.config.get(
            "visa_sponsorship_only",
            False,
        )
        self.required_technologies = self.config.get(
            "required_technologies",
            [],
        )

        logger.info("Job filter configuration loaded successfully.")
        logger.debug("Keywords               : %s", self.keywords)
        logger.debug("Locations              : %s", self.locations)
        logger.debug("Companies              : %s", self.companies)
        logger.debug("Excluded Companies     : %s", self.excluded)
        logger.debug("Sources                : %s", self.sources)
        logger.debug("Remote Only            : %s", self.remote_only)
        logger.debug(
            "Visa Sponsorship Only  : %s",
            self.visa_sponsorship_only,
        )
        logger.debug(
            "Required Technologies  : %s",
            self.required_technologies,
        )

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

        logger.debug("=" * 80)
        logger.debug("Evaluating Job")
        logger.debug("Title        : %s", job.title)
        logger.debug("Company      : %s", job.company)
        logger.debug("Location     : %s", job.location)
        logger.debug("Source       : %s", job.source)
        logger.debug("Salary       : %s", job.salary)
        logger.debug("Remote       : %s", job.remote_policy)
        logger.debug("Japanese     : %s", job.japanese_level)
        logger.debug("Technologies : %s", job.technologies)

        searchable_text = f"{job.title} {job.description}"

        logger.debug("Searchable Text: %s", searchable_text)

        # ----------------------------------------------------------
        # Keyword Filter
        # ----------------------------------------------------------

        if not self._contains_any(searchable_text, self.keywords):
            logger.debug(
                "❌ Keyword filter failed.\n"
                "Searchable Text : %s\n"
                "Expected Any Of : %s",
                searchable_text,
                self.keywords,
            )
            return False

        logger.debug("✅ Keyword filter passed.")

        # ----------------------------------------------------------
        # Location Filter
        # ----------------------------------------------------------

        if self.locations and job.location and job.location not in self.locations:
            logger.debug(
                "❌ Location filter failed.\n"
                "Job Location    : '%s'\n"
                "Allowed         : %s",
                job.location,
                self.locations,
            )
            return False

        logger.debug("✅ Location filter passed.")

        # ----------------------------------------------------------
        # Company Whitelist
        # ----------------------------------------------------------

        if self.companies and job.company not in self.companies:
            logger.debug(
                "❌ Company whitelist failed.\n"
                "Job Company     : '%s'\n"
                "Allowed         : %s",
                job.company,
                self.companies,
            )
            return False

        logger.debug("✅ Company whitelist passed.")

        # ----------------------------------------------------------
        # Company Blacklist
        # ----------------------------------------------------------

        if job.company in self.excluded:
            logger.debug(
                "❌ Company blacklist failed.\n" "Blacklisted Company: %s",
                job.company,
            )
            return False

        logger.debug("✅ Company blacklist passed.")

        # ----------------------------------------------------------
        # Source Filter
        # ----------------------------------------------------------

        if self.sources and job.source not in self.sources:
            logger.debug(
                "❌ Source filter failed.\n"
                "Job Source      : %s\n"
                "Allowed         : %s",
                job.source,
                self.sources,
            )
            return False

        logger.debug("✅ Source filter passed.")

        # ----------------------------------------------------------
        # Remote Filter
        # ----------------------------------------------------------

        if self.remote_only and job.remote_policy.lower() != "remote":
            logger.debug(
                "❌ Remote filter failed.\n" "Job Remote Policy : %s",
                job.remote_policy,
            )
            return False

        logger.debug("✅ Remote filter passed.")

        # ----------------------------------------------------------
        # Visa Sponsorship Filter
        # ----------------------------------------------------------

        if self.visa_sponsorship_only and not job.visa_sponsorship:
            logger.debug("❌ Visa sponsorship filter failed.")
            return False

        logger.debug("✅ Visa sponsorship filter passed.")

        # ----------------------------------------------------------
        # Technology Filter
        # ----------------------------------------------------------

        if self.required_technologies:

            technologies = [tech.lower() for tech in job.technologies]

            logger.debug(
                "Checking technologies.\n" "Required : %s\n" "Found    : %s",
                self.required_technologies,
                technologies,
            )

            for tech in self.required_technologies:

                if tech.lower() not in technologies:

                    logger.debug(
                        "❌ Technology filter failed.\n" "Missing Technology : %s",
                        tech,
                    )

                    return False

        logger.debug("✅ Technology filter passed.")

        logger.debug(
            "✅ JOB ACCEPTED: '%s'",
            job.title,
        )

        return True
