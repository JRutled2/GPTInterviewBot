DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS manager_teams;
DROP TABLE IF EXISTS user_teams;
DROP TABLE IF EXISTS weekly_chats;

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
	team_id TEXT NOT NULL,
	chat_date TEXT NOT NULL
);
