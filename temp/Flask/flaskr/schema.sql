drop TABLE if EXISTS entries;
CREATE table entries(
  id INTEGER PRIMARY key AUTHORIZATION ,
  title text not null,
  text text not null
);