DROP TABLE IF EXISTS user_teams;
DROP TABLE IF EXISTS weekly_chats;

CREATE TABLE user_teams(
	username TEXT PRIMARY KEY,
	team_name TEXT
);

CREATE TABLE weekly_chats(
	id INTEGER PRIMARY KEY,
	team_name TEXT NOT NULL,
	chat_week TEXT NOT NULL,
	interview TEXT
);
