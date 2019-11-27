CREATE TABLE "help" (
	"id" INTEGER NOT NULL,
	"content" TEXT NOT NULL
);

CREATE TABLE "tags" (
	"name" TEXT NOT NULL,
	"help_id" INTEGER
);
