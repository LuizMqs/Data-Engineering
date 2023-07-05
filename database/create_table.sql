CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE "public"."suicides" (
  "id" uuid DEFAULT uuid_generate_v4() NOT NULL UNIQUE,
  "state" VARCHAR(2) NOT NULL, 
  "year" VARCHAR(4) NOT NULL,
  "month" VARCHAR(2) NOT NULL,
  "date_of_death" VARCHAR(10) NOT NULL,
  "gender" VARCHAR(9),
  "race" VARCHAR(10) NOT NULL,
  "death_cause" VARCHAR(4) NOT NULL,
  "place_of_death" TEXT NOT NULL,
  "age" VARCHAR(5) NOT NULL,
  CONSTRAINT "suicides_pk" PRIMARY KEY ("id")
);

CREATE TABLE "public"."death_causes" (
  "id" VARCHAR(4) NOT NULL UNIQUE,
  "description" TEXT NOT NULL,
  CONSTRAINT "death_causes_pk" PRIMARY KEY ("id")
);

CREATE TABLE "public"."macro_regions_populations" (
  "macro_region" VARCHAR(10) NOT NULL,
  "total_population_2010" INTEGER NOT NULL,
  "total_population_2011" INTEGER NOT NULL,
  "total_population_2012" INTEGER NOT NULL,
  "total_population_2013" INTEGER NOT NULL,
  "total_population_2014" INTEGER NOT NULL,
  "total_population_2015" INTEGER NOT NULL,
  "total_population_2016" INTEGER NOT NULL,
  "total_population_2017" INTEGER NOT NULL,
  "total_population_2018" INTEGER NOT NULL,
  "total_population_2019" INTEGER NOT NULL,
  "total_population_2020" INTEGER NOT NULL,
  "total_population_2021" INTEGER NOT NULL,
  "total_population_2022" INTEGER NOT NULL,
  CONSTRAINT "macro_regions_populations_pk" PRIMARY KEY ("macro_region")
);

CREATE TABLE "public"."idh" (
  "id" uuid DEFAULT uuid_generate_v4() NOT NULL UNIQUE,
  "reference_year" INTEGER NOT NULL,
  "idh" FLOAT NOT NULL,
  "female_idh" FLOAT NOT NULL,
  "male_idh" FLOAT NOT NULL,
  "life_expectancy" FLOAT NOT NULL,
  "female_life_expectancy" FLOAT NOT NULL,
  "male_life_expectancy" FLOAT NOT NULL,
  CONSTRAINT "idh_pk" PRIMARY KEY ("id")
);

CREATE TABLE "public"."states" (
  "id" uuid DEFAULT uuid_generate_v4() NOT NULL UNIQUE,
  "state_abbreviation" VARCHAR(2) NOT NULL,
  "state" VARCHAR(20) NOT NULL,
  "region" VARCHAR(12) NOT NULL,
  "year" VARCHAR(4) NOT NULL,
  "number_of_deaths" VARCHAR(5) NOT NULL,
  CONSTRAINT "states_pk" PRIMARY KEY ("id")
);

ALTER TABLE suicides ADD CONSTRAINT fk_suicides_death_causes FOREIGN KEY (death_cause) REFERENCES death_causes (id);