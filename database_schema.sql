DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS manager_teams;
DROP TABLE IF EXISTS user_teams;
DROP TABLE IF EXISTS weekly_chats;

CREATE TABLE users(
	user_id TEXT PRIMARY KEY,
	username TEXT UNIQUE,
	password TEXT NOT NULL,
	access	INT	NOT NULL,
	gpt_key TEXT
);

CREATE TABLE teams(
	team_id TEXT PRIMARY KEY,
	team_name TEXT
);

CREATE TABLE manager_teams(
	user_id TEXT,
	team_id TEXT PRIMARY KEY
);

CREATE TABLE user_teams(
	user_id TEXT PRIMARY KEY,
	team_id TEXT
);

CREATE TABLE weekly_chats(
	chat_id TEXT PRIMARY KEY,
	team_id TEXT NOT NULL
);
