CREATE TABLE IF NOT EXISTS `birthdays` (
  `id` INTEGER NOT NULL,
  `date` TEXT
);

CREATE TABLE IF NOT EXISTS `servers` (
  `id` INTEGER NOT NULL,
  `birthday_channel` INTEGER
);

CREATE TABLE IF NOT EXISTS `selfroles` (
	`id` INTEGER NOT NULL,
	`server_id` INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS `bot_admins` (
	`id` INTEGER NOT NULL,
	`server_id` INTEGER
);
