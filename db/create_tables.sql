-- Create tables
CREATE TABLE roadmaps (
    id INTEGER PRIMARY KEY,
    name TEXT,
    swimlane_column_title TEXT
);

CREATE TABLE swimlanes (
    id INTEGER PRIMARY KEY,
    roadmap_id INTEGER,
    name TEXT,
    type TEXT
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    swimlane_id INTEGER,
    name TEXT,
    date TEXT,
    type TEXT
);