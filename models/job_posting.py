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

    # Salary or salary range (e.g., "¥6M–¥10M", "$120k-$150k").
    # Stored as a string because every website formats salary differently.
    salary: str

    # Remote work policy (e.g., "Remote", "Hybrid", "On-site").
    remote_policy: str

    # Required Japanese proficiency
    # (e.g., "None", "N2", "Business", "Fluent").
    japanese_level: str

    # Indicates whether the company offers visa sponsorship.
    visa_sponsorship: bool

    # Employment type
    # (e.g., "Full-time", "Contract", "Internship").
    employment_type: str

    # Name of the hiring team or department, if available.
    team: str

    # Technologies, programming languages, or tools mentioned in the job.
    # Examples: ["Python", "AWS", "Docker"]
    technologies: list[str]
