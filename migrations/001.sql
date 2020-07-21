
-- ------
-- initial database schema
-- ------


CREATE TABLE db_changelog (
    version VARCHAR(10), 
    notes VARCHAR(100),
    datetime DATETIME DEFAULT (DATETIME('now'))
);



CREATE TABLE operation (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    ticker VARCHAR(11) NOT NULL,
    price REAL,
    sell INTEGER, 
    buy INTEGER,
    date DATE
);

CREATE INDEX ix_operation_ticker ON operation (ticker);



-- FUTURE: brocker (easynvest), stock_exchange (B3 bovespa)



INSERT into db_changelog (version, notes) VALUES ('001', 'Initial DB')


