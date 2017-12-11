drop table if exists user;
create table user (
  username varchar(30) primary key,
  status varchar(30)
);

drop table if exists course;
create table course (
  cid varchar(30) primary key,
  name text
);

drop table if exists tag;
create table tag(
  tid integer auto_increment primary key,
  tag_name varchar (50)
);

drop table if exists question;
create table question (
  qid integer auto_increment primary key,
  vote_count int,
  courseid varchar(30),
  user_id varchar(30),
  text_input text,
  tag varchar(50)
);

drop table if exists response;
create table response (
  response_id integer auto_increment primary key,
  qid integer,
  foreign key (qid) references question(qid),
  vote_count int,
  user_id varchar(30),
  text_input text,
  tag varchar(50),
  course_num varchar(30)
);

drop table if exists vote;
create table vote (
  user_id varchar(30),
  comment_type varchar(30),
  comment_id int
);
