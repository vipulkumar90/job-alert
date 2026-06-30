import time

from playwright.sync_api import sync_playwright

from models.job_posting import JobPosting
from scrapers.base import BaseScraper
from utils.logger import logger


class JapanDevScraper(BaseScraper):
    """Scraper for JapanDev job listings."""

    BASE_URL = "https://japan-dev.com"
    JOBS_URL = f"{BASE_URL}/jobs"

    CARD_SELECTOR = ".job-item__inner"
    TITLE_SELECTOR = ".job-item__title"
    COMPANY_SELECTOR = ".job-item__contract-type"
    LOCATION_SELECTOR = 'xpath=.//img[@alt="location-icon"]/following-sibling::div[@class="job__tag-desc"]'

    def scrape(self) -> list[JobPosting]:
        logger.info("Starting JapanDev scraper")

        MAX_RETRIES = 3

        for attempt in range(MAX_RETRIES):

            jobs: list[JobPosting] = []

            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=False)
                    page = browser.new_page()

                    page.goto(self.JOBS_URL)
                    page.wait_for_load_state("networkidle")

                    cards = page.locator(self.CARD_SELECTOR)

                    for card in cards.all():
                        title = card.locator(self.TITLE_SELECTOR).inner_text().strip()

                        company = (
                            card.locator(self.COMPANY_SELECTOR).inner_text().strip()
                        )

                        location = (
                            card.locator(self.LOCATION_SELECTOR).inner_text().strip()
                        )

                        relative_url = card.locator(self.TITLE_SELECTOR).get_attribute(
                            "href"
                        )

                        url = f"{self.BASE_URL}{relative_url}"

                        jobs.append(
                            JobPosting(
                                title=title,
                                company=company,
                                location=location,
                                url=url,
                                description="",
                                posted_date="",
                                source="JapanDev",
                                salary="",
                                remote_policy="",
                                visa_sponsorship=False,
                                japanese_level="",
                            )
                        )

                    browser.close()

                logger.info("JapanDev scraper found %d jobs", len(jobs))
                return jobs

            except Exception:

                if attempt == MAX_RETRIES - 1:
                    logger.exception(
                        "JapanDev scraper failed after %d attempts", MAX_RETRIES
                    )
                    return []

                logger.warning(
                    "JapanDev scraper failed (attempt %d/%d). Retrying in 2 seconds...",
                    attempt + 1,
                    MAX_RETRIES,
                )

                time.sleep(2)

        return []
