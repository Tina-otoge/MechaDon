CREATE TABLE IF NOT EXISTS `birthdays` (
  `id` VARCHAR(18) NOT NULL,
  `date` TEXT
);

CREATE TABLE IF NOT EXISTS `servers` (
  `id` VARCHAR(18) NOT NULL,
  `birthday_channel` VARCHAR(18)
);

CREATE TABLE IF NOT EXISTS `selfroles` (
	`id` VARCHAR(18) NOT NULL,
	`server_id` VARCHAR(18) NOT NULL
);

CREATE TABLE IF NOT EXISTS `bot_admins` (
	`id` VARCHAR(18) NOT NULL,
	`server_id` VARCHAR(18)
);
