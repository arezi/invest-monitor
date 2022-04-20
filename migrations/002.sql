
-- ------
-- planning feature
-- ------


CREATE TABLE planning (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    ticker VARCHAR(11) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT 1 CHECK (active IN (0,1)), 
    date DATE,
    stop_gain REAL,
    stop_loss REAL,
    alert_gain REAL,
    alert_loss REAL,
    fair_value REAL,
    notes VARCHAR(1000)
);






INSERT into db_changelog (version, notes) VALUES ('002', 'planning feature')


