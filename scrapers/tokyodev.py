"""
TokyoDev scraper.

Scrapes job postings from TokyoDev and returns them as a list of
normalized JobPosting objects.
"""

import logging
import time

from playwright.sync_api import sync_playwright

from models.job_posting import JobPosting
from scrapers.base import BaseScraper

logger = logging.getLogger(__name__)


class TokyoDevScraper(BaseScraper):
    """
    Scraper implementation for TokyoDev.
    """

    BASE_URL = "https://www.tokyodev.com"
    JOBS_URL = "https://www.tokyodev.com/jobs"

    CARD_SELECTOR = "li[id]"

    COMPANY_SELECTOR = "h3 a"

    # NEW: each job posting inside a company card
    ITEM_SELECTOR = 'div[data-collapsable-list-target="item"]'

    # These are now relative to ITEM_SELECTOR, not the card
    TITLE_SELECTOR = "div.text-lg.font-bold.mb-1 > a"

    TAG_SELECTOR = "div.flex.gap-2.flex-wrap a"

    MAX_RETRIES = 3

    def scrape(self) -> list[JobPosting]:
        """
        Scrape all jobs from TokyoDev.

        Returns:
            List of JobPosting objects.
        """

        logger.info("Starting TokyoDev scraper.")

        for attempt in range(self.MAX_RETRIES):

            jobs: list[JobPosting] = []

            try:
                with sync_playwright() as p:

                    browser = p.chromium.launch(
                        headless=True,
                        args=["--no-sandbox"]
                    )

                    page = browser.new_page()

                    page.goto(self.JOBS_URL)

                    page.wait_for_load_state("networkidle")

                    cards = page.locator(self.CARD_SELECTOR)

                    for card in cards.all():

                        company = (
                            card.locator(self.COMPANY_SELECTOR).inner_text().strip()
                        )

                        # Each card can list multiple jobs for the
                        # same company - iterate over each item.
                        items = card.locator(self.ITEM_SELECTOR)

                        for item in items.all():

                            title_locator = item.locator(self.TITLE_SELECTOR)

                            # Skip malformed items with no title
                            if title_locator.count() == 0:
                                continue

                            title = title_locator.inner_text().strip()

                            relative_url = title_locator.get_attribute("href")

                            url = f"{self.BASE_URL}" f"{relative_url}"

                            salary = ""
                            japanese_level = ""
                            remote_policy = ""
                            technologies = []

                            tags = item.locator(self.TAG_SELECTOR).all_inner_texts()

                            for tag in tags:

                                tag = tag.strip()

                                if "¥" in tag:
                                    salary = tag

                                elif "Japanese" in tag:
                                    japanese_level = tag

                                elif "remote" in tag.lower():
                                    remote_policy = tag

                                else:
                                    technologies.append(tag)

                            jobs.append(
                                JobPosting(
                                    title=title,
                                    company=company,
                                    location="Not Specified",
                                    url=url,
                                    description="",
                                    posted_date="",
                                    source="TokyoDev",
                                    salary=salary,
                                    remote_policy=remote_policy,
                                    japanese_level=japanese_level,
                                    visa_sponsorship=False,
                                    employment_type="",
                                    team="",
                                    technologies=technologies,
                                )
                            )

                    browser.close()

                logger.info(
                    "TokyoDev scraper found %d jobs.",
                    len(jobs),
                )

                return jobs

            except Exception:

                if attempt == self.MAX_RETRIES - 1:
                    logger.exception(
                        "TokyoDev scraper failed after %d attempts.",
                        self.MAX_RETRIES,
                    )

                    return []

                logger.warning(
                    ("TokyoDev scraper failed " "(attempt %d/%d). " "Retrying..."),
                    attempt + 1,
                    self.MAX_RETRIES,
                )

                time.sleep(2)

        return []
