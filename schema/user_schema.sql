DROP TABLE IF EXISTS users;

CREATE TABLE users(
	user_id TEXT PRIMARY KEY,
	username TEXT UNIQUE,
	password TEXT NOT NULL,
	access	INT	NOT NULL,
	gpt_key TEXT NOT NULL
);