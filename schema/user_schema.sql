DROP TABLE IF EXISTS users;

CREATE TABLE users(
	username TEXT PRIMARY KEY,
	password TEXT NOT NULL,
	access	INT	NOT NULL,
	gpt_key TEXT NOT NULL
);