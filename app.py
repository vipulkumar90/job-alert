from database.db import initialize_database
from scrapers.japandev import JapanDevScraper
from services.discord import DiscordNotifier
from services.storage import Storage
from utils.logger import logger


def main() -> None:
    try:
        successful = 0

        logger.info("Application Started")

        initialize_database()

        scraper = JapanDevScraper()
        storage = Storage()
        notifier = DiscordNotifier()

        jobs = scraper.scrape()
        logger.info("Found %d jobs", len(jobs))

        new_jobs = storage.save_all(jobs)
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
