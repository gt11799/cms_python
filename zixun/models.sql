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
	if_display int default 1,
	update_time datetime,
	click_time int default 0，
	brand_id int default 0,
	delete_status int default 0
)default character set utf8 collate utf8_general_ci;


create table tag(
	id int not null primary key auto_increment,
	name varchar(128) not null,
	url varchar(64),
	meta_title varchar(128),
	meta_keyword varchar(128),
	meta_description text,
	click_time int default 0,
	update_time datetime,
	if_display int default 1,
	parent_id int not null default 0
)default character set utf8 collate utf8_general_ci;

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
	meta_description text,
	update_time timestamp,
	cover_image text,
	delete_status int default0
)default character set utf8 collate utf8_general_ci;

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
	cover_image text,
	shopping_goods text,
	update_time timestamp
)default character set utf8 collate utf8_general_ci;

insert into index_page (id,meta_title) values (1,"资讯首页");
insert into catagory (id,name,parent_id,delete_status) values (1000,"首页",1000,1);

create table record_flow(
	id int not null primary key auto_increment,
	operator varchar(128),
	operate varchar(128),
	object varchar(128),
	operate_time timestamp,
	sql_content text
)default character set utf8 collate utf8_general_ci;



