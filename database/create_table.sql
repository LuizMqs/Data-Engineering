CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE "public"."suicides" (
  "id" uuid DEFAULT uuid_generate_v4() NOT NULL UNIQUE,
  "state" varchar(2) NOT NULL, 
  "year" varchar(4) NOT NULL,
  "month" varchar(2) NOT NULL,
  "date_of_death" varchar(10) NOT NULL,
  "gender" varchar(9),
  "race" varchar(10) NOT NULL,
  "death_cause" varchar(4) NOT NULL,
  "place_of_death" TEXT NOT NULL,
  "age" varchar(5) NOT NULL,
  CONSTRAINT "suicides_pk" PRIMARY KEY ("id")
);

CREATE TABLE "public"."death_causes" (
  "id" varchar(4) NOT NULL UNIQUE,
  "description" TEXT NOT NULL,
  CONSTRAINT "death_causes_pk" PRIMARY KEY ("id")
);

ALTER TABLE suicides ADD CONSTRAINT fk_suicides_death_causes FOREIGN KEY (death_cause) REFERENCES death_causes (id);