CREATE TABLE "NFVO" (
  "id" int PRIMARY KEY,
  "name" varchar NOT NULL,
  "type" varchar NOT NULL,
  "site" varchar NOT NULL,
  "uri" varchar,
  "created_at" datetime,
  "updated_at" datetime
);

CREATE TABLE "NFVO_CREDENTIALS" (
  "nfvo_id" int PRIMARY KEY,
  "host" varchar NOT NULL,
  "project" varchar NOT NULL,
  "user" varchar NOT NULL,
  "password" varchar NOT NULL,
  FOREIGN KEY ("nfvo_id") REFERENCES "NFVO" ("id")
);

CREATE TABLE "NS_SUBSCRIPTION" (
  "id" int PRIMARY KEY,
  "nfvo_id" varchar,
  "callbackUri" varchar NOT NULL,
  FOREIGN KEY ("nfvo_id") REFERENCES "NFVO" ("id")
);

CREATE TABLE "NS_INSTANCE" (
  "ns_id" varchar,
  "sub_id" varchar,
  PRIMARY KEY ("ns_id", "sub_id"),
  FOREIGN KEY ("sub_id") REFERENCES "NS_SUBSCRIPTION" ("id")
);

