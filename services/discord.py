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

                logger.info("%d Discord notifications sent", job.title)
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
                    "fields": [
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
                        {
                            "name": "💰 Salary",
                            "value": job.salary or "Not specified",
                            "inline": True,
                        },
                        {
                            "name": "🌏 Remote",
                            "value": job.remote_policy or "Not specified",
                            "inline": True,
                        },
                        {
                            "name": "🗣 Japanese",
                            "value": job.japanese_level or "Not specified",
                            "inline": True,
                        },
                        {
                            "name": "🎯 Visa",
                            "value": (
                                "✅ Available"
                                if job.visa_sponsorship
                                else "❌ Not specified"
                            ),
                            "inline": True,
                        },
                        {
                            "name": "📅 Posted",
                            "value": job.posted_date or "Unknown",
                            "inline": True,
                        },
                        {
                            "name": "🌐 Source",
                            "value": job.source,
                            "inline": True,
                        },
                    ],
                    "footer": {
                        "text": "Job Alert",
                    },
                }
            ]
        }
    
    @staticmethod
    def _get_embed_color(job: JobPosting) -> int:
        if job.visa_sponsorship and job.remote_policy == "Remote":
            return 0xFFD700      # Gold

        if job.visa_sponsorship:
            return 0x2ECC71      # Green

        if job.remote_policy == "Remote":
            return 0x3498DB      # Blue

        return 0x95A5A6          # Gray