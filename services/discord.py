"""
Discord notification service.

Sends newly discovered job postings to a Discord channel using
Discord Webhooks and rich embeds.
"""

import time

import requests

from config import DISCORD_WEBHOOK
from models.job_posting import JobPosting
from utils.logger import logger


class DiscordNotifier:
    """Sends job notifications to Discord."""

    @staticmethod
    def send(job: JobPosting) -> bool:
        """
        Send a single job posting to Discord.

        Args:
            job: The JobPosting to send.
        """

        payload = DiscordNotifier._build_payload(job)

        logger.info("Sending Discord notification")
        MAX_RETRIES = 3

        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(
                    DISCORD_WEBHOOK,
                    json=payload,
                    timeout=10,
                )
                response.raise_for_status()

                logger.info("Discord notification sent for '%s'", job.title)
                return True

            except requests.RequestException:
                if response is not None:
                    logger.error(
                        "Discord response: %s",
                        response.text,
                    )
                if attempt == MAX_RETRIES - 1:
                    logger.exception(
                        "Failed to send Discord notification for '%s'",
                        job.title,
                    )
                    return False
                time.sleep(2)

    @staticmethod
    def _build_payload(job: JobPosting) -> dict:
        """
        Build a Discord embed payload for a job posting.

        Args:
            job: JobPosting object.

        Returns:
            Discord webhook payload.
        """

        fields = [
            {
                "name": "🏢 Company",
                "value": job.company,
                "inline": True,
            },
            {
                "name": "📍 Location",
                "value": job.location,
                "inline": True,
            },
        ]

        # Only include optional fields if they have a value.
        optional_fields = [
            ("💰 Salary", job.salary),
            ("🌏 Remote", job.remote_policy),
            ("🗣 Japanese", job.japanese_level),
            ("📅 Posted", job.posted_date),
            ("🌐 Source", job.source),
        ]

        for name, value in optional_fields:
            if value and value.strip():
                fields.append(
                    {
                        "name": name,
                        "value": value,
                        "inline": True,
                    }
                )

        # Only include visa sponsorship if it's available.
        if job.visa_sponsorship:
            fields.append(
                {
                    "name": "🎯 Visa",
                    "value": "✅ Visa Sponsorship Available",
                    "inline": True,
                }
            )

        return {
            "embeds": [
                {
                    "title": f"🚀 {job.title}",
                    "url": job.url,
                    "description": (
                        job.description[:250] + "..."
                        if len(job.description) > 250
                        else job.description
                    ),
                    "color": DiscordNotifier._get_embed_color(job),
                    "fields": fields,
                    "footer": {
                        "text": "Job Alert",
                    },
                }
            ]
        }

    @staticmethod
    def _get_embed_color(job: JobPosting) -> int:
        if job.visa_sponsorship and job.remote_policy == "Remote":
            return 0xFFD700  # Gold

        if job.visa_sponsorship:
            return 0x2ECC71  # Green

        if job.remote_policy == "Remote":
            return 0x3498DB  # Blue

        return 0x95A5A6  # Gray
