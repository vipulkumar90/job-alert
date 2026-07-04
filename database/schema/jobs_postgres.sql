CREATE TABLE IF NOT EXISTS jobs (
    id              SERIAL PRIMARY KEY,

    title           TEXT NOT NULL,
    company         TEXT NOT NULL,
    location        TEXT,

    url             TEXT NOT NULL,
    description     TEXT,
    posted_date     TEXT,

    source          TEXT NOT NULL,
    hash            TEXT UNIQUE NOT NULL,

    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);