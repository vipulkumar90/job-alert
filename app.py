from database.db import initialize_database
from scrapers.japandev import JapanDevScraper
from services.storage import Storage
from services.discord import DiscordNotifier


def main():

    initialize_database()

    scraper = JapanDevScraper()
    storage = Storage()
    notifier = DiscordNotifier()

    jobs = scraper.scrape()

    new_jobs = storage.save_all(jobs)

    print(f"Found: {len(jobs)} jobs")
    print(f"Inserted: {len(new_jobs)} jobs")

    for job in new_jobs:
        notifier.send(job)


if __name__ == "__main__":
    main()