
-- theme

drop table if exists theme;
create table theme (
  oid text primary key,
  json text
);

-- track

drop table if exists track;
create table track (
  oid text primary key,
  json text
);

-- game

drop table if exists game;
create table game (
  oid text primary key,
  json text
);

-- player

drop table if exists player;
create table player (
  oid text primary key,
  json text
);
