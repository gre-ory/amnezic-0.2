
-- genre

drop table if exists genre;
create table genre (
  id text primary key,
  json text
);

-- track

drop table if exists track;
create table track (
  id text primary key,
  json text
);

-- game

drop table if exists game;
create table game (
  id text primary key,
  json text
);

-- player

drop table if exists player;
create table player (
  id text primary key,
  json text
);
