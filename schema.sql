SET search_path TO public;

-- ACCOUNTS
CREATE TABLE "accounts" (
    "username" VARCHAR PRIMARY KEY NOT NULL,
    "password" VARCHAR NOT NULL,
    "email" TEXT NOT NULL,
    "type" VARCHAR NOT NULL DEFAULT 'student',
    "moodle_id" INTEGER
);

-- Achievements
CREATE TABLE "achievements" (
    "achievement_id" SERIAL PRIMARY KEY,
    "achievement_name" TEXT,
    "description" TEXT,
    "xp_value" INTEGER,
    "icon" TEXT,
    "rarity" TEXT
);

-- Degree
CREATE TABLE "degree" (
    "degree_id" SERIAL PRIMARY KEY,
    "degree" VARCHAR UNIQUE
);

-- inventory_items
CREATE TABLE "inventory_items" (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR,
    "description" VARCHAR,
    "rarity" INTEGER,
    "type" VARCHAR
);

CREATE UNIQUE INDEX "inventory_items_id_uindex" ON "inventory_items" ("id");

-- QuestionSets
CREATE TABLE "question_sets" (
    "set_id" SERIAL PRIMARY KEY,
    "set_name" TEXT DEFAULT 'Unnamed',
    "date_created" DATE,
    "author" TEXT,
    "questions" TEXT,
    "answers" TEXT,
    "cards_played" INTEGER DEFAULT 0
);

-- Quiz
CREATE TABLE "quiz" (
    "quiz_id" SERIAL PRIMARY KEY,
    "quiz_name" VARCHAR,
    "date_created" DATE,
    "author" VARCHAR,
    "plays" INTEGER DEFAULT 0
);

CREATE UNIQUE INDEX "quiz_quiz_id_uindex" ON "quiz" ("quiz_id");

-- CloseFriend
CREATE TABLE "close_friend" (
    "user1" TEXT REFERENCES "accounts"("username"),
    "user2" TEXT REFERENCES "accounts"("username"),
    PRIMARY KEY ("user1", "user2")
);

-- CompleteAchievements
CREATE TABLE "complete_achievements" (
    "username" TEXT REFERENCES "accounts"("username"),
    "achievement_id" INTEGER REFERENCES "achievements"("achievement_id"),
    "date_completed" DATE,
    PRIMARY KEY ("username", "achievement_id")
);

-- Connection
CREATE TABLE "connection" (
    "user1" TEXT REFERENCES "accounts"("username"),
    "user2" TEXT REFERENCES "accounts"("username"),
    "connection_type" TEXT,
    PRIMARY KEY ("user1", "user2")
);

-- inventory_backgrounds
CREATE TABLE "inventory_backgrounds" (
    "id" INTEGER REFERENCES "inventory_items"("id"),
    "url" VARCHAR
);

-- notification
CREATE TABLE "notification" (
    "username" VARCHAR REFERENCES "accounts"("username"),
    "body" TEXT,
    "date" TIMESTAMP,
    "url" VARCHAR
);

-- POSTS
CREATE TABLE "posts" (
    "post_id" SERIAL PRIMARY KEY,
    "body" VARCHAR,
    "likes" INTEGER DEFAULT 0,
    "username" VARCHAR REFERENCES "accounts"("username"),
    "date" DATE DEFAULT CURRENT_DATE,
    "privacy" VARCHAR
);

-- PrivateMessages
CREATE TABLE "private_messages" (
    "sender" VARCHAR REFERENCES "accounts"("username"),
    "receiver" VARCHAR REFERENCES "accounts"("username"),
    "message" TEXT,
    "date" TIMESTAMP
);

-- Question
CREATE TABLE "question" (
    "question_id" SERIAL PRIMARY KEY UNIQUE,
    "quiz_id" INTEGER REFERENCES "quiz"("quiz_id") NOT NULL,
    "question" VARCHAR NOT NULL,
    "answer_1" VARCHAR NOT NULL,
    "answer_2" VARCHAR NOT NULL,
    "answer_3" VARCHAR NOT NULL,
    "answer_4" VARCHAR NOT NULL
);

-- user_inventory
CREATE TABLE "user_inventory" (
    "username" VARCHAR REFERENCES "accounts"("username"),
    "id" INTEGER REFERENCES "inventory_items"("id")
);

-- UserLevel
CREATE TABLE "user_level" (
    "username" TEXT PRIMARY KEY REFERENCES "accounts"("username") NOT NULL,
    "experience" BIGINT NOT NULL DEFAULT 0
);

-- UserLikes
CREATE TABLE "user_likes" (
    "username" VARCHAR REFERENCES "accounts"("username"),
    "post_id" INTEGER REFERENCES "posts"("post_id")
);

-- UserProfile
CREATE TABLE "user_profile" (
    "username" VARCHAR PRIMARY KEY NOT NULL REFERENCES "accounts"("username") UNIQUE,
    "name" VARCHAR NOT NULL,
    "bio" TEXT,
    "gender" VARCHAR NOT NULL DEFAULT 'Not_specified',
    "birthday" DATE NOT NULL DEFAULT CURRENT_DATE,
    "profilepicture" TEXT,
    "degree" INTEGER REFERENCES "degree"("degree_id") NOT NULL DEFAULT 1,
    "privacy" VARCHAR NOT NULL DEFAULT 'public'
);

-- UserSocial
CREATE TABLE "user_social" (
    "username" TEXT REFERENCES "user_profile"("username"),
    "social" TEXT,
    "link" TEXT,
    PRIMARY KEY ("username", "social")
);

-- AllUserLikes
CREATE TABLE "all_user_likes" (
    "username" VARCHAR REFERENCES "accounts"("username"),
    "post_id" INTEGER REFERENCES "posts"("post_id")
);

-- Comments
CREATE TABLE "comments" (
    "comment_id" SERIAL PRIMARY KEY UNIQUE NOT NULL,
    "username" VARCHAR NOT NULL REFERENCES "accounts"("username"),
    "body" TEXT NOT NULL,
    "date" TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "post_id" BIGINT NOT NULL REFERENCES "posts"("post_id")
);

-- PostContent
CREATE TABLE "post_content" (
    "post_id" INTEGER REFERENCES "posts"("post_id"),
    "content_url" TEXT
);

-- UserHobby
CREATE TABLE "user_hobby" (
    "username" VARCHAR REFERENCES "user_profile"("username") NOT NULL,
    "hobby" TEXT NOT NULL,
    PRIMARY KEY ("username", "hobby")
);

-- UserInterests
CREATE TABLE "user_interests" (
    "username" VARCHAR REFERENCES "user_profile"("username") NOT NULL,
    "interest" TEXT,
    PRIMARY KEY ("username", "interest")
);
