
## mysql数据库新增数据库log_records 在该数据库中新增分区表operation_records 操作流水表
create database log_records;
use log_records;
create table operation_records(
	_id int not null auto_increment,
	operator varchar(32) not null,
	operate_time datetime not null,
	operate_module varchar(64),
	url varchar(256),
	arguments varchar(512),
	PRIMARY KEY (_id,operate_time)
)DEFAULT CHARSET=utf8 COLLATE utf8_general_ci
PARTITION BY RANGE (TO_DAYS(operate_time))
(PARTITION OP2015_01 VALUES LESS THAN (TO_DAYS('2015-01-01')) ENGINE = InnoDB,
 PARTITION OP2015_02 VALUES LESS THAN (TO_DAYS('2015-02-01')) ENGINE = InnoDB,
 PARTITION OP2015_03 VALUES LESS THAN (TO_DAYS('2015-03-01')) ENGINE = InnoDB,
 PARTITION OP2015_04 VALUES LESS THAN (TO_DAYS('2015-04-01')) ENGINE = InnoDB,
 PARTITION OP2015_05 VALUES LESS THAN (TO_DAYS('2015-05-01')) ENGINE = InnoDB,
 PARTITION OP2015_06 VALUES LESS THAN (TO_DAYS('2015-06-01')) ENGINE = InnoDB,
 PARTITION OP2015_07 VALUES LESS THAN (TO_DAYS('2015-07-01')) ENGINE = InnoDB,
 PARTITION OP2015_08 VALUES LESS THAN (TO_DAYS('2015-08-01')) ENGINE = InnoDB,
 PARTITION OP2015_09 VALUES LESS THAN (TO_DAYS('2015-09-01')) ENGINE = InnoDB,
 PARTITION OP2015_10 VALUES LESS THAN (TO_DAYS('2015-10-01')) ENGINE = InnoDB,
 PARTITION OP2015_11 VALUES LESS THAN (TO_DAYS('2015-11-01')) ENGINE = InnoDB,
 PARTITION OP2015_12 VALUES LESS THAN (TO_DAYS('2015-12-01')) ENGINE = InnoDB,
 PARTITION OPMaxValue VALUES LESS THAN (MAXVALUE) ENGINE = InnoDB);
 alter table operation_records add index oper_id_operator_index(_id,operator);


 ## mysql数据库data_records 新增表code_desc_map 码表信息；插入必要数据
 use data_records;
 create table code_desc_map(
     code_id varchar(32) not null,
     code_type varchar(32) not null,
     code_desc varchar(64) not null,
     PRIMARY KEY (code_id,code_type)
 )DEFAULT CHARSET=utf8 COLLATE utf8_general_ci;

 insert into code_desc_map values ('admin_module','xbhd','新版活动');
 insert into code_desc_map values ('admin_module','cg','采购');
 insert into code_desc_map values ('admin_module','cfdd','迟发订单');
 insert into code_desc_map values ('admin_module','yhqgl','优惠券管理');
 insert into code_desc_map values ('admin_module','spsh','商品审核');
 insert into code_desc_map values ('admin_module','txgl','提现管理');
 insert into code_desc_map values ('admin_module','wfl','未分类');
 insert into code_desc_map values ('admin_module','czxf','充值消费');
 insert into code_desc_map values ('admin_module','wz','未知');
 insert into code_desc_map values ('admin_module','ddsh','订单审核');
 insert into code_desc_map values ('admin_module','flgl','福利管理');
 insert into code_desc_map values ('admin_module','msgl','买手管理');
 insert into code_desc_map values ('admin_module','csgl','测试管理');
 insert into code_desc_map values ('admin_module','sjtj','数据统计');
 insert into code_desc_map values ('admin_module','sdsjtj','深度数据统计');
 insert into code_desc_map values ('admin_module','mshugl','美术管理');
 insert into code_desc_map values ('admin_module','jxcgl','进销存管理');
 insert into code_desc_map values ('admin_module','dcgpplb','待采购品牌列表');
 insert into code_desc_map values ('admin_module','xkgl','选款管理');
 insert into code_desc_map values ('admin_module','qdgl','渠道管理');
 insert into code_desc_map values ('admin_module','bgzwls','包裹账务流水');
 insert into code_desc_map values ('admin_module','wlgl','物流管理');
 insert into code_desc_map values ('admin_module','xcgls','新采购历史');
 insert into code_desc_map values ('admin_module','yhqzbgl','优惠券作弊管理');
 insert into code_desc_map values ('admin_module','ddlsfx','订单流水分析');
 insert into code_desc_map values ('admin_module','hdpq','活动排期');
 insert into code_desc_map values ('admin_module','ppdf','品牌打分');
 insert into code_desc_map values ('admin_module','hqrw','获取任务');
 insert into code_desc_map values ('admin_module','hqspcm','获取商品尺码');
 insert into code_desc_map values ('admin_module','gggl','公告管理');
 insert into code_desc_map values ('admin_module','gxrwzt','更新任务状态');
 insert into code_desc_map values ('admin_module','qiandgl','签到管理');
 insert into code_desc_map values ('admin_module','xck','新仓库');
 insert into code_desc_map values ('admin_module','cwdz','财物对账');
 insert into code_desc_map values ('admin_module','splm','商品类目');
 insert into code_desc_map values ('admin_module','kf','客服');
 insert into code_desc_map values ('admin_module','thdls','退货单历史');
 insert into code_desc_map values ('admin_module','tppx','图片排序');
 insert into code_desc_map values ('admin_module','ccgl','仓储管理');
 insert into code_desc_map values ('admin_module','cgdz','采购对账');
 insert into code_desc_map values ('admin_module','cxhd','促销活动');


 ## mongo数据库shop.permission 新增tag 所属模块
 use shop;
 db.permission.update({}, {$set:{'tag':''}});