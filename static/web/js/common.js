
$(function(){

	$('.iSidebar ul>li').click(function(e){
		e.stopPropagation();
		$(this).addClass('on').siblings().removeClass('on');
		return false;
	});

	$(document).on('click.sideBar',function(){
		$('.iSidebar ul>li').removeClass('on');
		$(".J_autocomplete").html("");
	});

	//手机端下载入口显示
	$(".user .down_phone").hover(function(){
		$('.phone_info').show();
	},function(){
		$('.phone_info').hide();
	})

	//年龄性别类型搜索显示
	$(".header .expand").hover(function(){
		$('.sub_nav').show();
	},function(){
		$('.sub_nav').hide();
	})

	//侧边栏广告
	$("body").append('<div class="float_md_l animate"><img src="/static/web/images/jieri/qingrenjie/left.png?v=2014122411"></div><div class="float_md_r animate"><img src="/static/web/images/jieri/qingrenjie/right.png?v=2014122411"></div>');

	//搜索 autocomplete
	$(".J_search_value").on("keyup",function(){
		var val = $(this).val()
		$.post("/search_name_ajax/",{
			n:val
			},function(data){
				var data = JSON.parse(data),
					tpl = '<div class="autocomplete"><h4>热门搜索</h4><div class="bd">';
				if(data.length){
					for(var i=0,len=data.length;i<len;i++){
						tpl += '<a class="clearfix" href="/detail/'+data[i].a_id+'/'+data[i].ag_id+'"><img src="'+data[i].img+'?imageView/1/w/50/h/50/q/100/interlace/1" width="50" height="50"><span>'+data[i].name+'</span></a>'
					}
					tpl += '</div></div>';
					$(".J_autocomplete").html(tpl);
					$(".J_autocomplete").on("click",function(e){
						e.stopPropagation();
					})
				}else{
					$(".J_autocomplete").html("");
				}
		})
	}).on("click",function(e){
		e.stopPropagation();
	})
});


jQuery.cookie = function(name, value, options) {
	if (typeof value != 'undefined') { // name and value given, set cookie
	    options = options || {};
	    if (value === null) {
	        value = '';
	        options.expires = -1;
	    }
	    var expires = '';
	    if (options.expires && (typeof options.expires == 'number' || options.expires.toUTCString)) {
	        var date;
	        if (typeof options.expires == 'number') {
	            date = new Date();
	            date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000));
	        } else {
	            date = options.expires;
	        }
	        expires = '; expires=' + date.toUTCString(); // use expires attribute, max-age is not supported by IE
	    }
	    var path = options.path ? '; path=' + options.path : '';
	    var domain = options.domain ? '; domain=' + options.domain : '';
	    var secure = options.secure ? '; secure' : '';
	    document.cookie = [name, '=', encodeURIComponent(value), expires, path, domain, secure].join('');
	} else { // only name given, get cookie
	    var cookieValue = null;
	    if (document.cookie && document.cookie != '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	}
};


var Base = {};

Base.isIE6 = $.browser.msie && $.browser.version < 7;

// Base.timeOut = function(dom,time,callback,timeback){
// 	var maxtime = time;//倒计时时间（秒）! 
// 	var	timer;
// 	CountDown();
// 	function CountDown(){ 
// 		if(maxtime>=0){   
// 			var minutes = Math.floor(maxtime/60),
// 				seconds = Math.floor(maxtime%60),
// 				msg = "";
// 			seconds<10 ? seconds = "0"+seconds : seconds;
// 			minutes<10 ? minutes = "0"+minutes : minutes;
// 			maxtime < 300 ? msg = "<span class='red'>！"+minutes+"分"+seconds + '秒</span>' : msg = minutes+"分"+seconds + '秒';
// 			dom.html(msg);
// 			maxtime--; 
// 			dom.attr("data-time",maxtime);
// 			if(maxtime<300){
// 				timeback && timeback();
// 			}
// 		}else{
// 			clearInterval(timer);
// 			callback && callback();
// 		}
// 	}
// 	if(typeof(timer)!="undefined"){
// 		clearInterval(timer);
// 		timer = setInterval(function(){CountDown()},1000);
// 		return;
// 	}
// 	timer = setInterval(function(){CountDown()},1000);
// }

function xhTimeOut(option){
	//var opt = option || {};
	this.elem = option.elem; //id
	this.maxtime = option.maxtime; //倒计时秒
	this.callback = option.callback; //倒计时结束时callback
	this.timeback = option.timeback; //剩余多少时间时callback
	this.timebacktt = option.timebacktt;
	this.mselem = option.mselem || "";
	this.settime();
	this.mselem && this.maxtime>0 && this.setMs();
}
xhTimeOut.prototype = {
	settime : function(){
		if(this.maxtime>=0){   
			var  day = Math.floor(this.maxtime/(60*60*24)),
				hour = Math.floor(this.maxtime/(60*60)%24),
				minutes = Math.floor(this.maxtime/60%60),
				seconds = Math.floor(this.maxtime%60),
				msg = "",
				dayTxt = "",
				hourTxt = "";
			day<10 ? day = "0"+day : day;
			hour<10 ? hour = "0"+hour : hour;
			if(this.maxtime<1210){
				dayTxt="";
				hourTxt="";
			}else{
				dayTxt = day+"：";
				hourTxt = hour+"：";
			}
			seconds<10 ? seconds = "0"+seconds : seconds;
			minutes<10 ? minutes = "0"+minutes : minutes;
			this.maxtime < 300 ? msg = "<span class='red'>！"+minutes+"："+seconds + '</span>' : msg =dayTxt+hourTxt+ minutes+"："+seconds;
			this.elem.html(msg);
			this.maxtime--; 
			this.elem.attr("data-time",this.maxtime);
			 if(this.maxtime<this.timebacktt){
			 	this.timeback && this.timeback();
			 }
			 if(this.maxtime<1){
			 	this.callback && this.callback();
			 }
		}else{
			clearInterval(this.timer);
		}
		if(typeof(this.timer)!="undefined"){
			return;
		}
		this.setInter()
	},
	setInter:function(){
		var that = this;
		this.timer = setInterval(function(){that.settime()},1000);
	},
	clear:function(){
		var that = this;
		if(typeof(this.timer)!="undefined"){
			clearInterval(this.timer);
		}
	},
	setMs:function(){
		var ms = 9,
			that = this;
		var setMs = setInterval(function(){
			that.mselem.html(" . "+ms);
			ms--;
			if(ms<0){
				ms = 9;
			}
		},100);
	}
}

Base.getCookie = function(name) {
	var c = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	return c ? c[1] : undefined;
}

//返回URL参数值
Base.getQueryString = function(name) {
	var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
	var r = window.location.search.substr(1).match(reg);
	if (r != null) return unescape(r[2]); return null;
}

Base.alert = function(option){
	var msg = option.msg,
	type = "i"+option.type,
	time = option.time || 2000;
	if($(".msgbox_wrap").length){return;}
	$("body").append('<div class="msgbox_wrap"><span class="msg_box"><span class="ico '+type+'"></span>'+msg+'<span class="box_end"></span></span></div>');
	setTimeout(function(){
		$(".msgbox_wrap").remove();
	},time);
	if(Base.isIE6){
		$(".msgbox_wrap").css({top:($(window).scrollTop()+$(window).height()/2)});
	}
}

//显示loading

function loadAjax(){
	this.loadingDia;
}

loadAjax.prototype = {
	open:function(){
		this.loadingDia = dialog({
			width: 60,
			height: 60,
			id:"loading"
		});
		this.loadingDia.show();
	},
	close:function(){
		this.loadingDia.close().remove();
	}
}

var loading = new loadAjax();

function getInternetExplorerVersion()
{
    var rv = -1; // 获取ie浏览器版本
    if (navigator.appName == 'Microsoft Internet Explorer') {
        var ua = navigator.userAgent;
        var re = new RegExp("MSIE ([0-9]{1,}[\.0-9]{0,})");
        if (re.exec(ua) != null)
            rv = parseFloat(RegExp.$1);
    }
    return rv;
}

//input 水印效果
Base.placeholder =function(obj){

	var ieVesion = getInternetExplorerVersion();
	

	if(!jQuery.browser.msie) return false;
	
	if(ieVesion>9){ return false; }

	if($.browser.mozilla && $.browser.version == '11.0'){return false;}

	var _self = this;
	obj.each(function(){
		var _this = jQuery(this);
		var _parent = _this.parent();
		
		if(_parent.css('position')=='static'){
			_parent.css('position','relative');
		}
		var top  = parseInt(_parent.css('paddingTop'));
		var paddingLeft = parseInt(_this.css('paddingLeft'));
		var color = _this.css('color');
		var fontSize = _this.css('fontSize');
		var placeholder = _this.attr('placeholder');
		var label = jQuery('<label>' + placeholder + '</label>');	
		
		if( jQuery.trim(_this.val())!=""){
			label.hide();
		}
		label.bind('click',function(){
			var _that = jQuery(this);
			_that.hide();
			_this.focus();
			
		});
		
		_this.blur(function(){
			var val = jQuery(this).val();
			if(	val==placeholder || val=='' ){
				label.text(placeholder).show();
			}
		});
		
		_this.focus(function(){
			label.hide();
		});
		
		label.css({
			width  : _this.outerWidth(),
			height : _this.outerHeight(),
			lineHeight  :_this.outerHeight() +'px',
			textIndent : paddingLeft,
			color : color,
			fontSize : fontSize,
			position : 'absolute',
			left: 0,
			zindex: 100,
			background:'none',
			top: top
		}).insertAfter(_this);
	});
}

Base.overLay = {
	open: function(){
		$("#content").append('<div class="overlay J_overlay"></div>');
	},
	close:function(){
		$(".J_overlay").fadeOut();
	},
	clickClose:function(){
		setTimeout(function(){
			$(".J_overlay").fadeOut();
		},1000)
		$("body").on("click",function(){
			$(".J_overlay").fadeOut();
		})
	}
}

//获得url后面的参数
function getUrlRequest(){
	var url = location.search; //获取url中"?"符后的字串  ?a=b
	var theRequest = new Object();
	if (url.indexOf("?") != -1) {
		var str = url.substr(1);
		if (str.indexOf("&") != -1) {
			strs = str.split("&");
			for (var i = 0; i < strs.length; i++) {
				theRequest[strs[i].split("=")[0]] = unescape(strs[i].split("=")[1]);
			}
		} else {
			var key = str.substring(0,str.indexOf("="));
			var value = str.substr(str.indexOf("=")+1);
			theRequest[key] = decodeURI(value);
		}
	}
	return theRequest;
}
//var geturl = new getUrlRequest()  使用方法 
//	  console.log(geturl["from"])

$.fn.hoverImg = function(){
	this.each(function(){
		var img = $(this).find("img"),
		oldurl = img.attr("src"),
		newurl = img.attr("load_src");
		$(this).hover(function(){
			img.attr("src",newurl);
		},function(){
			img.attr("src",oldurl);
		})
	})
}

$.fn.tab = function(){
	var that = this
	that.find(".tab_nav li").on("click",function(){
		$(this).addClass("current").siblings().removeClass("current");
		var index = $(this).index();
		that.find(".tab_content .tc_item").eq(index).addClass("current").siblings().removeClass("current");
	})
}

function showMsg(msg,id){
	var id = id || "";
	var d = dialog({
		title: '提示',
		content:msg,
		time:2,
		cancel:null
	});

	if(id){
		d.show(document.getElementById(id));
	}else{
		d.show();
	}

	setTimeout(function(){
		d.close()
	},2000)
}

function timeUp(opt){
	var time = opt.time,
	callback = opt.callback,
	elem = opt.elem;
	setTimeout(function(){
		elem.html("重新发送"+time+"秒");
		time--;
		if(0<time){
			setTimeout(arguments.callee,1000)
		}else{
			callback && callback()
		}
	},1000)
}

function getCaptcha(elem){
	elem.on("click",function(){
		if($(this).hasClass("disabled")){return;}
		var phoneExp = /0?(13|14|15|18|17)[0-9]{9}/,
		phone = $("#phone"),
		that = $(this);
		if(!phone.val()){
			showMsg('请输入手机号码!');
			return false;
		}else if(!phoneExp.test(phone.val())){
			showMsg('请输入正确手机号码!');
			return false;
		}else{
			that.addClass("disabled");
			$.post("/phone_gen_code/?_rand="+Math.random(),{
				_xsrf:Base.getCookie("_xsrf"),
				 source:"login",
				phone:phone.val()
			},function(data){
				var status = data.status,
				msg = data.msg;
				if(status===0){
					showMsg("验证码已发送至手机","succeed")
					timeUp({elem:that,time:60,callback:function(){
						that.removeClass("disabled");
						that.html("重发验证码");
					}})
				}else{
					that.removeClass("disabled");
					showMsg(msg);
				}
			})
		}
	})
}

function phoneLogin(elem,callback){
	elem.on("click",function(){
		var phoneExp = /0?(13|14|15|18|17)[0-9]{9}/,
		phone = $("#phone"),
		verifyCode = $("#verify_code"),
		that = $(this);
		if(!phone.val()){
			showMsg("请输入手机号码");
			return false;
		}else if(!phoneExp.test(phone.val())){
			showMsg("请输入正确手机号码");
			return false;
		}else if(!verifyCode.val()){
			showMsg("请输入验证码");
			return false;
		}else{
			that.val("正在提交...");
			$.post("/login_with_verify_code/?_rand="+Math.random(),{
				_xsrf:Base.getCookie("_xsrf"),
				phone:phone.val(),
				verify_code:verifyCode.val(),
				source:""
			},function(data){
				var status = data.status,
				msg = data.msg;
				if(status===0){
					showMsg("验证通过","succeed");
					if(callback){
						that.val("提交");
						callback()
					}else{
						setTimeout(function(){
							window.location.reload();
						},1000)
					}
				}else{
					showMsg(msg);
					that.val("提交");
				}
			})
			return false;
		}
	})
}

function showPhoneLogin(title,type,tips,phone){
	var type = type || 1,
		tips = tips || "",
		phone = phone || ""
	var loginTpl = '<div class=" form_box">'+
					'<form class="phone_login_box">';
		if(tips){
			loginTpl += tips;
		}
		if(type==3){
			loginTpl += '<ul class="clearfix" style="position:relative">'+
					 '<li class="J_no_phone item">手　机：<input type="text" id="phone" name="phone" maxlength="50" placeholder="请输入您的手机号码" class="textbox" style="width:190px; background:#f5f5f5" value="'+phone+'" readonly>'+
					'</li>';
		}else{
			loginTpl += '<ul class="clearfix" style="position:relative">'+
					 '<li class="J_no_phone item">手　机：<input type="text" id="phone" name="phone" maxlength="50" placeholder="请输入您的手机号码" class="textbox" style="width:190px">'+
					'</li>';
		}
			loginTpl += '<li class="item">验证码：<input type="text" id="verify_code" name="verify_code" maxlength="50" placeholder="请输入手机收到的验证码" class="textbox" style="width:190px"></li>'+
					'<a id="J_get_captcha" class="btn get_captcha fr" style="padding:4px 10px; position:absolute; top:13px; right:0">获取验证码</a>'+
					'</ul>'+
					'<div class="submit_box" style="margin:10px 0 0 57px">'+
					'<input id="phone_login_btn" type="submit" value="提交" class="btn btn_green" style="padding:10px 30px">';
		if(type==2){
			loginTpl +='<p><a href="/login/" class="link">普通登录>></a></p>'
		}
		loginTpl +='</div>'+
					'</form>'+
					'</div>';

	var loginDialog = dialog({
		title:title || "手机验证码快捷登录/注册",
		content:loginTpl,
		lock:true,
		opacity:0.65
	})
	loginDialog.show()
	getCaptcha($("#J_get_captcha"));
	phoneLogin($("#phone_login_btn"));
}

function toLogin(title){
	var tpl = '<p style="text-align:center; padding:10px">如果没有账号请选择快捷购买</p><p style="text-align:center;"><a class="btn" style="margin:10px" href="/login/" id="d_login">登录</a><a style="margin:10px" class="btn btn_green" href="/add_address/?from=cart">快捷购买</a></p><p style="text-align:center; padding:10px; color:#6a4688">登录，可以使用荷币 和 优惠券哦！</p>';
	var  toLoginDialog = dialog({
		title:title || "您尚未登录",
		content:tpl,
		width:360
	})
	toLoginDialog.show();
}

$.scrollToFix = function(option,callback){
	var opt = option || {},
		elem = typeof(opt.elem)==="string" ? $("#"+opt.elem) : opt.elem,
		to = opt.to || 0,
		time = opt.time;
	elem.on("click",function(){
		$("body,html").animate({"scrollTop":to},time,function(){
			callback && callback();
		});
	})
}

$.fn.xhHover = function(option,callback){
	var opt = option || {},
		elem = opt.elem,
		sub = opt.sub,
		condition = opt.cssCondition;
	this.on("mouseenter",function(){
		var that = $(this);
		if(that.hasClass(condition)){return}
		if(sub){
			that.find("."+sub).show();
		}
		setTimeout(function(){
			that.addClass("hover").siblings().removeClass("hover")
		},1);
		callback && callback();
		
	})
	this.on("mouseleave",function(){
		var that = $(this);
		//if(that.hasClass(condition)){return}
		that.removeClass("hover")
		if(sub){
			setTimeout(function(){
				that.find("."+sub).hide();
			},200)
		}
	})
}

$.fn.showContact = function(callback){
	var that = this;
	that.on("click",function(){
		var	url = document.location.pathname+document.location.search,
			host = document.location.hostname;
			if(host=="www.xiaoher.com"){
				tpl = '<iframe src="http://chat.xiaoher.com/kefu/consult/?from_url='+url+'" style="width:600px; height:500px; border:none; overflow:hidden" scrolling="no" frameborder="0"></iframe>'
			}else{
				tpl = '<iframe src="/kefu/consult/?from_url='+url+'" style="width:600px; height:500px; border:none; overflow:hidden" scrolling="no" frameborder="0"></iframe>'
			}
		
		var conDialog = dialog({
			id:"kefu",
			title:"小荷在线客服",
			content:tpl,
			padding:0,
			width:600,
			height:500,
			fixed:true,
			resize:true
		})
		conDialog.show();
		callback && callback();
		return false;
	})
}

$.xhSetTimeout = function (callback,time){
	setTimeout(function(){
		callback && callback()
	},time)
}

jQuery.cookie = function(name, value, options) {
	if (typeof value != 'undefined') { // name and value given, set cookie
		options = options || {};
		if (value === null) {
			value = '';
			options.expires = -1;
		}
		var expires = '';
		if (options.expires && (typeof options.expires == 'number' || options.expires.toUTCString)) {
			var date;
			if (typeof options.expires == 'number') {
				date = new Date();
				date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000));
			} else {
				date = options.expires;
			}
				expires = '; expires=' + date.toUTCString(); // use expires attribute, max-age is not supported by IE
		}
		var path = options.path ? '; path=' + options.path : '';
		var domain = options.domain ? '; domain=' + options.domain : '';
		var secure = options.secure ? '; secure' : '';
		document.cookie = [name, '=', encodeURIComponent(value), expires, path, domain, secure].join('');
	} else { // only name given, get cookie
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
};

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






