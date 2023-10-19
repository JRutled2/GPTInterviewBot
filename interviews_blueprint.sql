DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS weekly_chats;

CREATE TABLE teams(
	id INTEGER PRIMARY KEY,
	team_name text
);

CREATE TABLE weekly_chats(
	id INTEGER PRIMARY KEY,
	week TEXT NOT NULL,
	interview TEXT
);
