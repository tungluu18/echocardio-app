create database echo_cardio;
use echo_cardio;

create table video
(
  id         int auto_increment,
  created_at timestamp    null,
  updated_at timestamp    null,
  name       varchar(255) not null,
  session_id int          not null,
  data_path  varchar(255) not null,
  ef         float        null,
  gls        float        null,
  constraint id
    unique (id),
  constraint video_ibfk_1
    foreign key (session_id) references session (id)
);

alter table video
  add primary key (id);

create table annotation
(
  id         int auto_increment,
  created_at timestamp    null,
  updated_at timestamp    null,
  video_id   int          not null,
  json       text         not null,
  data_path  varchar(255) not null,
  constraint id
    unique (id),
  constraint annotation_ibfk_1
    foreign key (video_id) references video (id)
);

create index video_id
  on annotation (video_id);

alter table annotation
  add primary key (id);


create table session
(
  id           int auto_increment,
  created_at   timestamp    null,
  updated_at   timestamp    null,
  creator_id   int          not null,
  patient_name varchar(255) not null,
  patient_age  int          null,
  data_path    varchar(255) null,
  constraint id
    unique (id),
  constraint session_ibfk_1
    foreign key (creator_id) references user (id)
);

alter table session
  add primary key (id);

create index session_id
  on video (session_id);

create index creator_id
  on session (creator_id);

INSERT INTO echo_cardio.session (id, created_at, updated_at, creator_id, patient_name, patient_age, data_path) VALUES (6, '2019-03-04 01:13:49', '2019-03-04 01:13:49', 1, 'jack', 12, '/data/sessions/6');

create table user
(
  id           int auto_increment,
  created_at   timestamp    null,
  updated_at   timestamp    null,
  username     varchar(255) not null,
  password     varchar(255) not null,
  email        varchar(255) not null,
  phone        varchar(255) null,
  address      varchar(255) null,
  organization varchar(255) null,
  job          varchar(255) null,
  primary key (id, username, email),
  constraint id
    unique (id),
  constraint username
    unique (username)
);

INSERT INTO echo_cardio.user (id, created_at, updated_at, username, password, email, phone, address, organization, job) VALUES (1, '2019-03-02 01:05:21', '2019-03-02 01:05:21', 'tungluu18', '$2b$10$2p8VfOlHD4furyS.esMxm./7Xcf/Sa.jcnyo3PB7oFElagAAn4I3q', 'tungluu18@gmail.com', null, null, 'uet', 'student');
INSERT INTO echo_cardio.user (id, created_at, updated_at, username, password, email, phone, address, organization, job) VALUES (2, '2019-03-02 01:05:21', '2019-03-02 01:05:21', 'tungluu19', '$2b$10$GzSqHuF9GWEKpAjVlnzRwOk3fdr5GnjtZMcYiJqPUiq.IM9sje8yS', 'tungluu18@gmail.com', null, 'cau giay district', 'uet', 'student');
INSERT INTO echo_cardio.user (id, created_at, updated_at, username, password, email, phone, address, organization, job) VALUES (7, '2019-03-03 00:42:56', '2019-03-03 00:42:56', 'tqlong', '$2b$10$c5WiqioVmZgvujGVOzptR.bvjEByIxAU2qF/AGW.gW2SEdHCyRUxe', 'long.tq@uet.vn', '451231534', null, 'UET', 'lecturer');





