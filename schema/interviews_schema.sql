DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS weekly_chats;

CREATE TABLE teams(
	id INTEGER PRIMARY KEY,
	team_name TEXT
);

CREATE TABLE user_teams(
	username TEXT PRIMARY KEY,
	team_name TEXT
);

CREATE TABLE weekly_chats(
	id INTEGER PRIMARY KEY,
	week TEXT NOT NULL,
	interview TEXT
);
