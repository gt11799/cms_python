create database zixun default character set utf8 collate utf8_general_ci;

create table article(
	id int not null primary key auto_increment,
	catagory_id int not null,
	title varchar(128),
	description text not null,
	content longtext not null,
	cover_image text,
	author varchar(64),
	create_time datetime,
	meta_title varchar(128),
	meta_keyword varchar(128),
	meta_description text,
	if_recommend int default 0,
	if_display int default 1,
	update_time datetime,
	click_time int default 0
)default character set utf8 collate utf8_general_ci;

alter table article drop column if_recommend;
alter table article add column brand_id int default 0;
alter table article add column delete_status int default 0;

create table tag(
	id int not null primary key auto_increment,
	name varchar(128) not null,
	url varchar(64),
	if_recommend int default 0,
	meta_title varchar(128),
	meta_keyword varchar(128),
	meta_description text,
	click_time int default 0,
	update_time datetime,
	if_display int default 1
)default character set utf8 collate utf8_general_ci;

alter table tag drop column if_recommend;
alter table tag add column parent_id int not null default 0;

create table article_tag(
	id int not null primary key auto_increment,
	article_id int,
	tag_id int,
	foreign key (article_id) references article(id),
	foreign key (tag_id) references tag(id)
);

create table catagory(
	id int not null primary key auto_increment,
	name varchar(128) not null,
	parent_id int not null default 0,
	url varchar(64),
	meta_title varchar(128),
	meta_keyword varchar(128),
	meta_description text
)default character set utf8 collate utf8_general_ci;

alter table catagory add column delete_status int default 0;
alter table catagory add column update_time timestamp;
alter table catagory add column cover_image text;

create table brand(
	id int not null primary key auto_increment,
	name varchar(128) not null,
	description text,
	create_time datetime,
	update_time datetime,
	url varchar(64) not null,
	cover_image varchar(128),
	company_name varchar(128),
	company_website varchar(128),
	brand_classify varchar(128),
	company_address varchar(128),
	meta_title varchar(128),
	meta_keyword varchar(128),
	meta_description text,
	author varchar(64),
	click_time int default 0,
	delete_status int default 0
)default character set utf8 collate utf8_general_ci;

create table hot_brand(
	id int not null primary key auto_increment,
	catagory_id int ,
	brand_id int,
	update_time timestamp
)default character set utf8 collate utf8_general_ci;

create table hot_tag(
	id int not null primary key auto_increment,
	catagory_id int,
	tag_id int,
	update_time timestamp
)default character set utf8 collate utf8_general_ci;

create table index_page(
	id int not null primary key auto_increment,
	meta_title varchar(128),
	meta_keyword varchar(128),
	meta_description varchar(128),
	cover_image varchar(256),
	shopping_goods varchar(256),
	update_time timestamp
)default character set utf8 collate utf8_general_ci;

insert into index_page (id,meta_title) values (1,"资讯首页");
insert into catagory (id,name,parent_id,delete_status) values (1000,"首页",1000,1);

alter table index_page change column cover_image cover_image text;
alter table index_page change column shopping_goods shopping_goods text;

create table record_flow(
	id int not null primary key auto_increment,
	operator varchar(128),
	operate varchar(128),
	object varchar(128),
	operate_time timestamp,
	sql_content text
)default character set utf8 collate utf8_general_ci;



