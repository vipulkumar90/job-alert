from database.db import initialize_database
from database.repository import JobRepository
from scrapers.master import MasterScraper
from services.discord import DiscordNotifier
from utils.logger import logger


def main() -> None:
    try:
        successful = 0

        logger.info("Application Started")

        initialize_database()

        master_scraper = MasterScraper()
        repository = JobRepository()
        notifier = DiscordNotifier()

        new_jobs = []
        jobs = master_scraper.scrape()
        for job in jobs:
            if repository.save(job):
                new_jobs.append(job)
        logger.info("Found %d jobs", len(jobs))

        logger.info("%d new jobs inserted", len(new_jobs))

        for job in new_jobs[:2]:
            if notifier.send(job):
                successful += 1

        logger.info(
            "Successfully sent %d/%d Discord notifications",
            successful,
            len(new_jobs),
        )

        logger.info("Application finished")

    except Exception:
        logger.exception("Application terminated unexpectedly")


if __name__ == "__main__":
    main()
