"""
Discord notification service.

Sends newly discovered job postings to a Discord channel using
Discord Webhooks and rich embeds.
"""

import requests

from config import DISCORD_WEBHOOK
from models.job_posting import JobPosting


class DiscordNotifier:
    """Sends job notifications to Discord."""

    @staticmethod
    def send(job: JobPosting) -> None:
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
                    "footer": {
                        "text": "Job Alert"
                    },
                }
            ]
        }

        response = requests.post(
            DISCORD_WEBHOOK,
            json=payload,
            timeout=10,
        )

        response.raise_for_status()