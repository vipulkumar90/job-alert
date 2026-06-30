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

        payload = {
            "embeds": [
                {
                    "title": "🚀 New Job Found!",
                    "description": f"**{job.title}**",
                    "url": job.url,
                    "color": 0x2ECC71,  # Green
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
                            "name": "🌐 Source",
                            "value": job.source,
                            "inline": True,
                        },
                    ],
                    "footer": {"text": "Job Alert"},
                }
            ]
        }

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
