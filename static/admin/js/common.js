//alert(0)
var isIE6 = $.browser.msie && $.browser.version < 7;
var app = {
	alert:function(option){
		var msg = option.msg,
			type = "i"+option.type,
			time = option.time || 2000;
		if($(".msgbox_wrap").length){return;}
		$("body").append('<div class="msgbox_wrap"><span class="msg_box"><span class="ico '+type+'"></span>'+msg+'<span class="box_end"></span></span></div>');
		setTimeout(function(){
			$(".msgbox_wrap").remove();
		},time);
		if(isIE6){
			$(".msgbox_wrap").css({top:($(window).scrollTop()+$(window).height()/2)});
		}
	},
	layer: function(option){
		this.css = option.css || "";
		this.msg = option.msg || "";
		this.time = option.time || "";
		this.type = option.type || 1; //1，普通  2，确认框
		this.zhezhao = option.zhezhao || 1;
		this.title = option.title || "";
		this.area =  option.area || [420,"auto"];
		this.box = null;
		this.callback = option.callback;
		this.init();
	},
	loading:{
		open:function(msg){
			$("body").append('<div class="msgbox_wrap loading_box"><span class="msg_box"><span class="ico i4"></span><span class="loading"></span>'+msg+'<span class="box_end"></span></span></div>');
		},
		close:function(){
			$(".loading_box").remove();
		}
	}
}
app.layer.prototype = {
	init: function(){
		this.creat();
		var that = this;
		if(this.zhezhao==1){
			zhezhao.open();
		}
		if(this.type==2){
			this.showComfirm();
			this.box.on("click",".submit",function(){
				that.callback();
				that.close();
			});
		}
		this.box.on("click",".close",function(){
			that.close();
		});
	},
	creat: function(){
		$("body").append('<div class="xz_pop" id="'+this.css+'"><div class="alert"><div class="pop_content">'+this.msg+'</div></div><div class="pop_shadow"></div></div>');
		
		var that = this;
		this.box = $(".xz_pop");
		var  box = this.box ;
		if(this.time){
			this.setTime();
		}
		if(this.title){
			this.setTitle(this.title);
		}
		this.setArea();
	},
	setTime:function(){//倒计时
		var alltime = this.time/1000;
		var that = this;
		if(this.title){
			$(".xz_pop").find(".pop_content").append('<div class="timer"><span id="mm">'+alltime+'</span>秒后关闭本窗口</div>');
		}
		var jishi = function(){
			$(".xz_pop").find("#mm").html(alltime);
			alltime--;
			if(alltime<0){
				that.close();
				return;
			}
			setTimeout(jishi,1000);
		}
		jishi();
	},
	setArea:function(){//设定宽高
		this.box.css({
			width:this.area[0],
			height:this.area[1],
			marginLeft:-(this.area[0]=="auto" ? this.box.outerWidth()/2 : this.area[0]/2),
			marginTop:-(this.area[1]=="auto" ? this.box.outerHeight()/2 : this.area[1]/2)
		});
		if(this.area[1]!="auto"){
			this.box.find(".pop_content").css({height:(this.area[1]-28-(this.box.find(".title").outerHeight() === undefined ? 0 : this.box.find(".title").outerHeight()))})
		}
		//alert(this.box.find(".title").outerHeight())
		if(isIE6){
			var scrollTop = $(window).scrollTop()+$(window).height()/2;
			this.box.css({top:scrollTop});
		}
	},
	close: function(){
		$(".xz_pop").remove();
		zhezhao.close();
	},
	setTitle: function(title){//改变标题
		var title = title,
			titleId = $(".xz_pop .alert .title");
		if(!titleId.length){
			$(".xz_pop").find(".alert").prepend('<div class="title"><span title="tt">'+title+'</span><span class="close"></span></div>');
		}else{
			titleId.html(title);
		}
	},
	setContent: function(content){//改变内容
		$(".xz_pop .pop_content").html(content);
	},
	showComfirm:function(){
		this.box.find(".pop_content").append('<div class="btn_box"><a class="app_btn app_btn-primary submit">确定</a><a class="close app_btn">取消</a></div>');
		isIE6 && $(".xz_zhezhao").css({height:$("body").height()});
	}
}

var zhezhao = {
	open: function(){
		$("body").append('<div class="xz_zhezhao"></div>');
		isIE6 && $(".xz_zhezhao").css({height:$("body").height()});
	},
	close: function(){
		$(".xz_zhezhao").remove();
	}
}

//
function showMsg(msg,type){
	app.alert({msg:msg,type:type})
}

function getCookie(name) {
    var c = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return c ? c[1] : undefined;
}


//去除首尾逗号
function trim(str){
    return str.replace(/^,+|,+$/g, "");
}

//删除cookie
function clearCookie(){
	//获取所有Cookie，并把它变成数组
	var cookies = document.cookie.split(";");
	//循环每一个数组项，把expires设置为过去时间，这样很容易地消除了所有Cookie
	for (var i = 0; i < cookies.length; i++) {
		var cookie = cookies[i];
		var eqPos = cookie.indexOf("=");
		var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
		name = name.replace(/^s*|s*$/, "");//清除Cookie里的空格
		document.cookie = name + "=;expires="+ new Date(0).toUTCString()
	}
}


//返回URL参数值
function getQueryString(name) {

	var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i"); 
	var u = window.location.search.substr(1); 
	encodeURI(u); 
	var r = decodeURI(u).match(reg); 
	if (r != null) return unescape(r[2]); return null;

	/*
	var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
	var r = window.location.search.substr(1).match(reg);
	if (r != null) return unescape(r[2]); return null;*/
}

//数组去重
Array.prototype.unique= function(){
	var res = [];
	var json = {};
	for(var i = 0; i < this.length; i++){
		if(!json[this[i]]){
			res.push(this[i]);
			json[this[i]] = 1;
		}
	}
	return res;
}


function loginOut(){
	clearCookie();
	//window.location.href = "/company/login/"
}


$(function(){
	//下拉菜单
	$(".J_dropdown").hover(function(){
		var dom = $(this).find("dd");
		if(!dom.is(':animated')){
			dom.stop(false,true).slideDown(200); 
		}
		
	},function(){
		var dom = $(this).find("dd");
		if(!dom.is(':animated')){
			dom.stop(false,true).slideUp(200); 
		}
		
	})
})


function ChangeURLParm(Turl,Parm,PValue,ClearParm){
	//thisURL = document.URL;
	//thisHREF = document.location.href;
	//thisSLoc = self.location.href;
	//thisDLoc = document.location;
	//strwrite = " thisURL: [" + thisURL + "]<br>"
	//strwrite += " thisHREF: [" + thisHREF + "]<br>"
	//strwrite += " thisSLoc: [" + thisSLoc + "]<br>"
	//strwrite += " thisDLoc: [" + thisDLoc + "]<br>"
	//document.write( strwrite );
	//Turl: 网址
	//Parm： 参数
	//PValue： 参数值
	//ClearParm: 要清除的参数
	var URL,Parms,ParmsArr,IsExist;
	var NewURL = Turl;//window.location.href
	IsExist = false;
	with(Turl){
		if(indexOf('?')>0){
			URL = substr(0,indexOf('?'));//不包含参数
			Parms = substr(indexOf('?')+1,length);//参数
		}
		else{
			URL = Turl;
			Parms = '';
		}
	}
	if (Parms!=''){
		var i;
		ParmsArr = Parms.split("&");
		for(i=0;i<=ParmsArr.length-1;i++){
			if (String(Parm).toUpperCase()==String(ParmsArr[i].split("=")[0]).toUpperCase()){//原来有参数Parm则改变其值
				ParmsArr[i] = Parm + "=" + PValue;
				IsExist = true;
				if (String(ClearParm) ==""){
					break;
				}
			}
			else if ( (String(ClearParm)!="") && (String(ClearParm).toUpperCase()==String(ParmsArr[i].split("=")[0])).toUpperCase() ){//去掉参数ClearParm的值
				ParmsArr[i] = ClearParm + "=";
			}
		}

		for(i=0;i<=ParmsArr.length-1;i++){
			if(i==0){
				Parms = ParmsArr[i];
			}
			else{
				Parms = Parms + "&" + ParmsArr[i];
			}
		}
		NewURL = URL + "?" + Parms;
		if (!IsExist){
			NewURL = NewURL + "&" + Parm + "=" + PValue;
		}
	}
	else{
		NewURL = URL + "?" + Parm + "=" + PValue;
	}
	return NewURL;
} 

//获取全部checkbox 值  反回数组  传入dom
function getAllChecked(elem){
	var thisVal = [];
	elem.find("input[type=checkbox]").each(function(){
		if($(this).attr("checked")){
			thisVal.push($(this).val());
		}
	})
	return thisVal;
}


//弹窗显示产品图片
function showProPic(gid,dom,pname,psize){
	var item = $(dom).parents('tr'),
	width = 'auto',
	height = 'auto';
	app.loading.open("正在请求数据...");
	$.ajax({
		url: "/company/get_goods_image/?goods_id=" + gid,
		type : "get",
		success: function(data){
			app.loading.close();
			if(data.status==0){
				var imgs = data['goods']['image'];
				if(imgs.length>5){
				  width = 950;
				}
				if(imgs.length>10){
				  width = 980;
				  height = 350;
				}
				var productName = '',
					productSize = '';
				if(pname){
					productName = '<table class="tb_product"><tr><td class="odd">商品名称：</td><td>' + pname + '</td></tr>';
				}
				if(psize){
					productSize = '<tr><td class="odd">尺码：</td><td>' + psize + '</td></tr></table>';
				}
				var cont = $('<div>' + productName + productSize + '<div class="pop_goods_box" style="height:' + height + 'px; overflow-y:auto; "><ul class="list_img"></ul></div></div>');
				$.each(imgs,function(k,v){
					cont.find('ul').append('<li><img width="230" src="' + v + '"></li>');
				});
			}
			art.dialog({
				id : 'pop',
				title : $(dom).text(),
				fixed:true,
				lock : true,
				width:width,
				padding:"20px 5px",
				top:100,
				content: cont.html(),
				cancelVal:'关闭',
				cancel:function(){
				}
			});

		}
	});
}

//关闭当前页面
function closeWindow(){
	if (navigator.userAgent.indexOf("MSIE") > 0) {  
        if (navigator.userAgent.indexOf("MSIE 6.0") > 0) {  
            window.opener = null; window.close();  
        }  
        else {  
            window.open('', '_top'); 
            window.top.close();  
        }  
    }  
    else if (navigator.userAgent.indexOf("Firefox") > 0) {  
        window.location.href = 'about:blank ';  
        //window.history.go(-2);  
    }  
    else {  
        window.opener = null;   
        window.open('', '_self', '');  
        window.close();  
    } 
}

//分页
function pageRender(args){
	var queryStr = window.location.search;
	if(!queryStr){
		queryStr = '?' + args.fieldDef;
	}else{
		queryStr = queryStr.replace(/\&page=\d+/g,'');
	}
	//有些参数是可选的，比如lang，若不传有默认值
	kkpager.generPageHtml({
		pno : getQueryString('page') || 1,
		//总页码
		total : args.pageCount,
		//总数据条数
		totalRecords : args.recordNum,
		//链接前部
		hrefFormer :'',
		//链接尾部
		hrefLatter :'',
		getLink : function(n){
			if(args.fieldDef){
				return this.hrefFormer + this.hrefLatter + queryStr +  '&page=' + n;
			}else{
				return this.hrefFormer + this.hrefLatter + "?page=" + n;
			}
		}
	});
}

// - 全选/反选/单选
function checkRender(selecter){
	var table = $(selecter),
	check_dom =  table.find('tr.tbHead').find(':checkbox'); 

	//初始化checkbox状态
	table.find(':checkbox').attr('checked',false);

	//单选
	table.on("change","tbody>tr input[type='checkbox']", function () {
		var _this = $(this);
		if(_this.is(':checked')){
		  _this.parents('tr').addClass('isChecked');
		}else{
		  _this.parents('tr').removeClass('isChecked');
		}
	});

	//全选/反选
	check_dom.change(function(){
		var cbs = table.find('tbody tr').not('.tbHead'),
		_this = $(this);

		if(_this.is(':checked')){
		  cbs.each(function(k){
			var _that = $(this);
			var _input = _that.find('input[type="checkbox"]');
			if(_input.length){
			  _input.attr('checked','checked');
			  _that.addClass('isChecked');
			}
		  });
		}else{
		  cbs.each(function(k){
			var _that = $(this);
			var _input = _that.find('input[type="checkbox"]');
			if(_input.length){
			  _input.attr('checked',false);
			  _that.removeClass('isChecked');
			}
		  });
		}
	});

	//阻止冒泡
	table.find('a,input,textarea').on('click',function(e){
		e.stopPropagation();
	});

	table.find(':checkbox').parents('tr').on('click',function(){
		var cb = $(this).find(':checkbox');
		if(cb.is(':checked')){
			cb.attr('checked',false);
			$(this).removeClass('isChecked');
		}else{
			cb.attr('checked','checked');
			$(this).addClass('isChecked');
		}
		return false;
	});
}


/**
 * 弹窗AJAX修改信息
 * @param {Object} args 配置信息
 * @return {Object} 弹窗对象 
 */
function popAjax(args){
	var _args = $.extend({ 
		id : args.id || 'pop',
		top : 150 ,      //弹窗的top值，默认 150
		lock : true,     //弹出是否锁屏，默认true
		sMsg : '操作成功！',      //操作成功提示信息
		eMsg : '亲，后台报错了~', //后台报错，未返回提示信息情况
		status : 0,      //操作成功后台，返回的status值
		reload : false,  //操作成功后是否刷新页面，默认否
		isCloseWin : true, //操作成功后，是否关闭弹窗
		title : '提示',  //弹窗标题
		content : '',    //弹窗内容
		type : 'post',   //ajax请求的类型
		url : '',        //ajax请求的url
		getData : null,  //ajax数据的获取方法，返回json对象,
		callback : null,  //成功后回调方法
		checkData : null,
		loadFinished : null, //弹窗加载完成执行
		fixed : true,
		close : null //关闭弹出回调方法

	}, ( args || {} ) );

	var ajaxPop = art.artDialog({
		id : 'ajaxPop',
		title : _args.title,
		content : _args.content,
		top: _args.top,
		lock : _args.lock,
		fixed : _args.fixed,
		ok : function(){
			if(_args.checkData && !_args.checkData()){
				return false;
			}
			app.loading.open("正在载入...");
			$.ajax({
				type : _args.type,
				url: _args.url,
				data : _args.getData(),
				success: function(data){
					app.loading.close();
					if(data.status==_args.status){
						showMsg( _args.sMsg,1 );
						if(_args.callback){
							_args.callback(data);
						}
						_args.reload && window.location.reload();
						_args.isCloseWin && ajaxPop.close();
						
					}else{
						showMsg(data.msg || _args.eMsg,3);
					}
				}
			});
			return false;
		},
		cancel : function(){
			_args.close && _args.close();
		}
	});

	 _args.loadFinished && _args.loadFinished();
	return ajaxPop;
}

/**
* url拼接，一般用于搜索
* @param {Object} args 配置信息 
* - @param {String} url 
* - @param {Array}  key 拼接的字段 如：['brand_id','date']
* - @param {Array}  val 字段对应的值 如：[1,'2014-12-03']
*/
function urlJoin(args){
	var url = args.url,
	t = 0;
	for(var i=0, len=args.key.length; i<len; i++){
		if(args.val[i]!='' && args.val[i]!=undefined){
			if(args.hasParam){
				url+='&' + args.key[i] +'=' + String(args.val[i]).replace(/\&/g, '%26');
			}else{
				if(t==0){
					url+='?' + args.key[i] +'=' + String(args.val[i]).replace(/\&/g, '%26');
				}else{
					url+='&' + args.key[i] +'=' + String(args.val[i]).replace(/\&/g, '%26');
				}
				t++;
			}
		}
	}
	return url.replace(/\#/g, '%23');
}


/**
* 行内修改信息。常用在表格单元给内修改信息。
* @param {Object} selector 选择器或者jQuery对象
* @param {Object} args 配置参数
*/
function inlineModify(selector,args){
	var _dom = selector instanceof $ ? selector : $( selector );
	var _args = $.extend({ 
		sMsg : '操作成功！',      //操作成功提示信息
		eMsg : '亲，后台报错了~', //后台报错，未返回提示信息情况
		status : 0,      //操作成功后台，返回的status值
		type : 'post',   //ajax请求的类型
		url : '',        //ajax请求的url
		getData : null,  //ajax数据的获取方法，返回json对象,
		callback : null,  //成功后回调方法
		reload : false
	}, ( args || {} ) );

	var originalsVal = _dom.val(); //初始值
	_dom.on('change',function(){
		app.loading.open("正在修改...");
		$.ajax({
			type : _args.type ,
			url: _args.url,
			data : _args.getData(_dom),
			success: function(data){
				app.loading.close();
				if(data.status==_args.status){
					showMsg( _args.sMsg || '操作成功！',1 );
					_args.callback && _args.callback();
					_args.reload && window.location.reload();
				}else{
					_dom.val(originalsVal);
					showMsg(data.msg || _args.eMsg,3);
				}
			}
		});
	});
}


/**
* 下来列表
* @param {Object} selector 选择器或者jQuery对象
* @param {Object} args 配置参数
*/
function DropDownRender(selector, args){
	var _args = $.extend({ 
		eMsg : '亲，后台报错了~', //后台报错，未返回提示信息情况
		status : 0,       //操作成功后台，返回的status值
		type : 'get',     //ajax请求的类型
		url : '',         //ajax请求的url
		source : 'list',  //ajax返回json对象名称
		key : 'name',     //ajax返回json 对应的key名称
		val : 'id',       //ajax返回json 对应的key名称
		height : '300',   //列表搞定
		data : null,
		clickEvent : null,//列表元素点击事件
		callback : null   //数据加载成功后回调方法
	}, ( args || {} ) );

	var _self = this;

	//input text
	this.dom = selector instanceof $ ? selector : $( selector );

	//下来列表
	this.listDom = $('<ul class="xhui_droplist"></ul>').appendTo($('body'));

    //数据源		
	this.source = [];

	//选中的数据
	this.selectedTarget = [];

	//获取选择的数据
	this.getSelected = function(){
		return this.selectedTarget;
	}

	
	//通过key，查找val
	this.getVal = function(key){
		var val = '';
		$.each(_self.source, function(k,v){
			if(key==v['key']){
				val = v['val']
			}
		});
		return val;
	}

	//通过val，查找key
	this.getKey = function(val){
		var key = [];
		$.each(_self.source,function(k,v){
			if(val==v['val']){
				key.push(v['key'])
			}
		});
		return key;
	}

	//设置位置
	this.resize = function(arg){
		var arg = arg || {}
		_self.listDom.css({
			left : _self.dom.offset().left ,
			top : _self.dom.offset().top + _self.dom.outerHeight(),
			zIndex : arg.zIndex || 100
		});
	}

	this.getSource = function(){

		//静态数据
		if(_args.data){
			_self.source = _args.data;
			return false;
		}

		$.ajax({
		    url : _args.url,
		    type :_args.type,
		    async:false,
			dataType:"json",
		    success: function(data){
		        if(data.status==_args.status){
		        	$.each(data[_args.source],function(k,v){
		        		_self.source.push({
							key : v[_args.key],
							val : v[_args.val]
						});
		        	});
		        	_args.callback && _args.callback();
		        }else{
		            showMsg(data.msg || _args.eMsg,3);
		        }
		    }
		});
	}

	var search = function(){
		var val = _self.dom.val();
		_self.listDom.html('');
		$.each(_self.source, function(k,v){
			if(v['val'].indexOf(val)!==-1){
				var item = $('<li data-key="' + v['key'] + '">' + v['val'] + '</li>');
				item.on('click',function(){
					_self.dom.val($(this).text());
					_self.listDom.hide();
					_self.selectedTarget = v;
					_args.clickEvent(v);
				}).hover(function(){
					item.addClass('on').siblings().removeClass('on')
				});
				_self.listDom.append(item);
			}
		});
		_self.listDom.find('li').length && _self.listDom.show();
	}

	var control = function(keycode){
		var items  = _self.listDom.find('li'),
			sIndex = items.index(_self.listDom.find('li.on')),
			mIndex = items.length -1;
		//回车
		if(keycode===13){
			_self.listDom.find('li.on').click();
			return false;
		}
		//上
		if(keycode===38){
			sIndex = sIndex==0 ? mIndex : sIndex-1;
		}
		//下 
		if(keycode===40){
			sIndex = sIndex==mIndex ? 0 : sIndex+1;
		}
		items.eq(sIndex).addClass('on').siblings().removeClass('on');
	}

	var formatDom = function(){
		_self.listDom.css({
			width : _self.dom.outerWidth() -2,
			maxHeight : _args.height,
			position : 'absolute',
			left : _self.dom.offset().left ,
			top : _self.dom.offset().top + _self.dom.outerHeight()
		});

		//绑定事件
		$(document).on('click.droplist',function(){
			_self.listDom.hide();
		});

		_self.listDom.on('click',function(e){
			e.stopPropagation();
		});

		_self.dom.on('click',function(e){
			e.stopPropagation();
		}).on('keyup.droplist',function(e){
			if(e.keyCode===37 || e.keyCode===38 || e.keyCode===39 || e.keyCode===40 || e.keyCode===13){
				control(e.keyCode);
			}else{
				search();
			}
		}).on('focus',function(){
			_self.listDom.siblings('.xhui_droplist').hide();
			var val = $(this).val();
			if(val!==''){
				_self.getKey(val) && search();
			}else{
				search()
			}
		});
	}

	var init = function(){
		_self.getSource();
		formatDom();
	}
	init();
}
