from database.initializer import initialize_database
from database.repository import JobRepository
from scrapers.master import MasterScraper
from services.discord import DiscordNotifier
from services.job_filter import JobFilter
from utils.logger import logger


def main() -> None:
    try:
        successful = 0

        logger.info("Application Started")

        # Initialize database
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

        job_filter = JobFilter()

        interesting_jobs = [job for job in new_jobs if job_filter.matches(job)]

        for job in interesting_jobs[:2]:
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

    finally:
        repository.close()


if __name__ == "__main__":
    main()
