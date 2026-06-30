"""
Defines the standard JobPosting model used throughout the application.

Every scraper must return a list of JobPosting objects regardless of the
website being scraped. This ensures the rest of the application remains
independent of any specific job board.
"""

from dataclasses import dataclass


@dataclass
class JobPosting:
    """
    Represents a normalized job posting.

    All website scrapers must populate this object so downstream components
    (database, duplicate detection, Discord notifications, etc.) can work
    with a consistent data structure.
    """

    # Title of the job posting.
    title: str

    # Name of the company offering the position.
    company: str

    # Job location (e.g., "Tokyo", "Remote", "Osaka").
    location: str

    # Direct link to the original job posting.
    url: str

    # Full job description or summary.
    description: str

    # Date the job was posted on the source website.
    # Stored as a string for now since different websites use different
    # date formats. This can later be standardized to a datetime object.
    posted_date: str

    # Name of the source website (e.g., "JapanDev", "Green", "LinkedIn").
    source: str
