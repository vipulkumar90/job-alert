from playwright.sync_api import sync_playwright

from models.job_posting import JobPosting
from scrapers.base import BaseScraper


class JapanDevScraper(BaseScraper):
    """Scraper for JapanDev job listings."""

    BASE_URL = "https://japan-dev.com"
    JOBS_URL = f"{BASE_URL}/jobs"

    CARD_SELECTOR = ".job-item__inner"
    TITLE_SELECTOR = ".job-item__title"
    COMPANY_SELECTOR = ".job-item__contract-type"

    def scrape(self) -> list[JobPosting]:
        jobs: list[JobPosting] = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            page.goto(self.JOBS_URL)
            page.wait_for_load_state("networkidle")

            cards = page.locator(self.CARD_SELECTOR)

            for card in cards.all():
                title = card.locator(self.TITLE_SELECTOR).inner_text().strip()

                company = card.locator(
                    self.COMPANY_SELECTOR
                ).inner_text().strip()

                location = (
                    card.locator(
                        'xpath=.//img[@alt="location-icon"]/following-sibling::div[@class="job__tag-desc"]'
                    )
                    .inner_text()
                    .strip()
                )

                relative_url = card.locator(
                    self.TITLE_SELECTOR
                ).get_attribute("href")

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
                    )
                )

            browser.close()

        return jobs