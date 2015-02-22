//倒计时
function timeOut(time){
	var maxtime = time;//倒计时时间（秒）! 
	if(!$(".J_timer").length){
		$(".J_cart").after('<span class="time_out"><span class="J_timer"></span><em></em></span> ');
	}
	CountDown()
	function CountDown(){ 
		if(maxtime>=0){
			var minutes = Math.floor(maxtime/60),
				seconds = Math.floor(maxtime%60);
			seconds<10 ? seconds = "0"+seconds : seconds;
			minutes<10 ? minutes = "0"+minutes : minutes;
			var msg = minutes+":"+seconds;   
			$(".J_timer").html(msg);
			if(maxtime == 5*60){
				var dialog = new Dialog({
					content:'您的购物车只剩<span class="red">5分钟</span>时间，立即结算？',
					callback: function(){
						window.location.href="/cart";
						this.close();
					}
				})
			}
			maxtime--; 
		}
		else{
			clearInterval(timer);
			var dialog2 = new Dialog({
					content:"订单超时，请重新下单哦!",
					callback: function(){
						window.location.href="/cart";
						this.close();
					}
				})
		}
	}
	if(typeof(timer)!="undefined"){
		clearInterval(timer);
		timer = setInterval(function(){CountDown()},1000);
		return;
	}
	timer = setInterval(function(){CountDown()},1000);
}

//表单验证
function errorShow (opt) {
	var elem = typeof(opt.elem) === "string" ? $("."+opt.elem+" .bd") : opt.elem,
		times = opt.times || 9,
		msg = opt.msg;
	//window.scrollTo(0,elemTop-100)
	elemTop = elem.offset().top;
	window.scrollTo(0,elemTop-100);
	//闪烁效果
	function showError(){
		if(elem.hasClass("error")){ 
			elem.removeClass("error")
		}else{
			elem.addClass("error");
		}
	}
	var i=1;
	setTimeout(function(){
		i++;
		showError();
		if(i<times){
			setTimeout(arguments.callee,200)
		}
	},300)

	showMsg(opt.msg)
}

//错误提示（顶部）
function showMsg(msg,type){
	var typeStyle = "msg_error";
	if(type){
		typeStyle = "msg_suc";
	}
	var tmp = '<div class="modal "><div class="msg '+typeStyle+'">'+msg+'</div><span class="msg_close">x</span></div>'
	if($(".modal").length){
		return;
	}
	$("body").append(tmp);
	setTimeout(function(){
		$(".modal").remove();
	},2000)
	$(".modal").click(function(){
		$(this).hide();
		return false;
	})
}


//弹窗dialog
function Dialog(opt){
	this.title = opt.title || "小荷友情提醒您";
	this.content = opt.content || "";
	this.overlay = opt.overlay || true;
	this.callback = opt.callback;
	this.cancelback = opt.cancelback;
	this.leftTxt = opt.leftTxt || "取消";
	this.rightTxt = opt.rightTxt || "确定";
	this.style =  opt.style || "";
	this.box = null;
	this.open()
}
Dialog.prototype = {
	open:function(){
		this.creat();
		this.btnCancel()//绑定取消事件
		this.btnSubmit()
		//$("body").on('touchmove', disableScroll);
	},
	creat:function(){
		//this.box = $(".ui_dialog");
		if($(".ui_dialog").length){$(".ui_dialog").remove()}
		var tpl = '<div class="ui_dialog '+this.style+'">'+
					'<div class="hd">'+this.title+'<span class="cancel icon_close2"></span></div>'+
			  		'<div class="bd">'+this.content+'</div>'+
			  		'<div class="bd_btn"><a class="cancel">'+this.leftTxt+'</a><a class="submit">'+this.rightTxt+'</a></div>'+
			  '</div>';
		$("body").append(tpl);
		this.overlay && layer.open();
		this.box = $(".ui_dialog");
	},
	close:function(){
		this.box.remove();
		layer.close();
		//$("body").off('touchmove', disableScroll);
	},
	btnCancel:function(){
		var that = this;
		this.box.find(".cancel").on("click",function(){
			that.close();
			that.cancelback && that.cancelback();
		})
	},
	btnSubmit:function(){
		var that = this;
		this.box.find(".submit").on("click",function(){
			that.callback && that.callback();
		})
	}
}

//弹出层

function XhPop(opt){
	this.elem = opt.elem || "";
	this.content = opt.content;
	this.overlay = opt.overlay || true;
	this.closeBtn = opt.closeBtn || false;
	this.pop = null;
	this.open()
}
XhPop.prototype = {
	open:function(){
		this.creat();
		this.overlay && layer.open();
		this.setAsize();

		var that = this;
		that.pop.find(".J_cose").on("click",function(){
			that.close();
		})
	},
	creat:function(){
		var closeHtml = "";
		if(this.closeBtn){
			closeHtml = '<a class="icon_close pop_close J_cose"></a>'
		}
		$("body").append('<div class="xh_pop" id="'+this.elem+'">'+closeHtml+
							'<div class="pop_content">'+
								this.content+
							'</div>'+
						'</div>');
		this.pop = $("#"+this.elem+"");


	},
	setAsize:function(){
		var img = new Image,
			src = $(".xh_pop").find("img").attr("src");
			var	that = this;
			if(src){
				img.src = src;
				img.onload = function(){
				 	var height = that.pop.height(),
					winHeight =$(window).height();
					that.pop.css({"marginTop":-height/2});
				};
			}else{
				var height = this.pop.height();
				that.pop.css({"marginTop":-height/2});
			}
	},
	close:function(){
		this.pop.remove();
		layer.close();
	}
}

//遮罩
var layer = {
	open:function(){
		$("body").append('<div class="overlay"></div>');
	},
	close:function(){
		$(".overlay").remove();
	}
}

//loading...
var loading = {
	open:function(msg){
		var showmsg = msg || ""
		$("body").append('<div class="loading"><div class="box"><span class="load_img"></span><span class="load_msg">'+showmsg+'</span></div></div>');
	},
	close:function(){
		$(".loading").remove();
	}
}

function getCookie(name) {
    var c = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return c ? c[1] : undefined;
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

$.fn.checkbox = function(){
	this.on("click",function(){
		$(this).find(".icon_checkbox").toggleClass("checked");
	})
}

$.fn.telReplace = function(){
	this.on("keyup",function(){
		var thisVal = $(this).val(),
			len = thisVal.length;
		if(len==3 || len==8){
			$(this).val(thisVal+" ")
		}
	})
}

$.fn.toggleShow = function(){
	var that = this;
	that.find(".hd").on("click",function(){
		that.toggleClass("show");
	})
}



$(function(){
	//模拟radio
	var radioCheck = $(".J_radio_check li");
	if(radioCheck.length){
		radioCheck.on("click",function(){
			$(this).parents(".J_radio_check").find(".icon_radio_unchecked").removeClass("icon_radio_checked");
			$(this).find(".icon_radio_unchecked").addClass("icon_radio_checked");
			$(this).parent().find("input").val($(this).attr("data-val"));
		});
	}

	//购物车有商品时添加倒计时功能
	var timeOutDom = $(".J_time_out");
	if(timeOutDom.length){
		var timeout = parseInt(timeOutDom.attr("data-time"));
		if(timeout>0){
			new timeOut(timeout);
		}
	}

	//返回上一页
	var backurl = document.referrer;
	if(backurl){
		$(".J_back").attr("href",backurl);
	}

	if($(".download").length){
		$("body").css({"paddingTop":55})
	}


	/*
	$(window).on("scroll",function(){
		var scrollTop = $(window).scrollTop();
		if(scrollTop>200){
			$("body").addClass("fixed");
			$(".J_d_app").hide();
		}else{
			$("body").removeClass("fixed");
			$(".J_d_app").show();
		}
	})
	*/
})

$.fn.tab = function(){
	var that = this
	that.find(".tab_nav li").on("click",function(){
		$(this).addClass("current").siblings().removeClass("current");
		var index = $(this).index();
		that.find(".tab_content .item").eq(index).addClass("current").siblings().removeClass("current");
	})
}

$.fn.iosButton = function(callback,cancelback){
	var that = this;
	that.on("click",function(){
		if(that.hasClass("checked")){
			cancelback && cancelback();
			that.removeClass("checked");
		}else{
			callback && callback();
			that.addClass("checked");
		}

	})
}

Zepto.cookie = function(name, value, options) {
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
				var cookie = Zepto.trim(cookies[i]);
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

function disableScroll(e) {
	e.preventDefault();
}

function UpSide(opt){
	this.title = opt.title;
	this.content = opt.content;
	this.cancelback = opt.cancelback;
	this.default();
}

UpSide.prototype = {
	default:function(){
		this.open();
		var that = this;
		this.elem.find("#L_close").on("click",function(){
			that.close();
			that.cancelback && that.cancelback();
		})
	},
	open:function(){
		this.$body = $("body");
		var that = this;
		this.$body.append('<div class="up_side animate"><div class="hd pearl clearfix"><a href="javascript:;" id="L_close">< 返回</a>'+this.title +'</div><div class="bd">'+this.content+'</div></div>');
		setTimeout(function(){
			that.$body.on('touchmove', disableScroll);
			$(".up_side").addClass("show")
		},1)
		
		this.elem = $(".up_side");
	},
	close:function(callback){
		var that = this;
		//$(".index").removeClass("up_side_active");
		$(".up_side").removeClass("show");
		that.$body.off('touchmove', disableScroll);
		setTimeout(function(){
			$(".up_side").remove();
			callback && callback();
		},200)
		
	}
}

function timeUp(opt){
	var time = opt.time,
		callback = opt.callback,
		elem = opt.elem;
	setTimeout(function(){
		elem.html("重新发送"+time);
		time--;
		if(0<time){
			setTimeout(arguments.callee,1000)
		}else{
			callback && callback()
		}
	},1000)
}

function getCaptcha(){
$("#J_get_captcha").on("click",function(){
	if($(this).hasClass("disabled")){return;}
	var phoneExp = /0?(13|14|15|18|17)[0-9]{9}/,
		phone = $("#phone"),
		that = $(this);
	if(!phone.val()){
		errorShow({elem:phone,msg:"请输入手机号码"});
		return false;
	}else if(!phoneExp.test(phone.val())){
		errorShow({elem:phone,msg:"请输入正确手机号码"});
		return false;
	}else{
		that.addClass("disabled")
		$.post("/phone_gen_code/?_rand="+Math.random(),{
			_xsrf:getCookie("_xsrf"),
			source:"login",
			phone:phone.val()
		},function(data){
			var status = JSON.parse(data).status,
				msg = JSON.parse(data).msg;
			if(status===0){
				showMsg("验证码已发送至手机",1)
				timeUp({elem:that,time:60,callback:function(){
					that.removeClass("disabled");
					that.html("重发验证码");
				}})
			}else{
				showMsg(msg);
				that.removeClass("disabled");
			}
		})
	}
})
}

function phoneLogin(callback){
	$("#phone_login_btn").on("click",function(){
		var phoneExp = /0?(13|14|15|18|17)[0-9]{9}/,
			phone = $("#phone"),
			verifyCode = $("#verify_code"),
			that = $(this);
		if(!phone.val()){
			errorShow({elem:phone,msg:"请输入手机号码"});
			return false;
		}else if(!phoneExp.test(phone.val())){
			errorShow({elem:phone,msg:"请输入正确手机号码"});
			return false;
		}else if(!verifyCode.val()){
			errorShow({elem:verifyCode,msg:"请输入验证码"});
			return false;
		}else{
			that.val("正在提交...");
			$.post("/login_with_verify_code/?_rand="+Math.random(),{
				_xsrf:getCookie("_xsrf"),
				phone:phone.val(),
				verify_code:verifyCode.val(),
				source:""
			},function(data){
				var status = JSON.parse(data).status,
					msg = JSON.parse(data).msg,
					url = JSON.parse(data).referer || "";
				if(status===0){
					showMsg("登录成功",1);
					callback && callback();
				}else{
					showMsg(msg);
					that.val("提交");
				}
			})
			return false;
		}
	})
}

function defaultLogin(callback){
	$("#login").on("submit",function(){
		var phoneExp = /0?(13|14|15|18|17)[0-9]{9}/,
			emailExp = /\w+((-w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+/,
			username = $("#username"),
			pwd = $("#password");
			if(!username.val()){
				errorShow({elem:username,msg:"请输入手机号或邮箱"});
				return false;
			}else if(!phoneExp.test(username.val()) && !emailExp.test(username.val())){
				errorShow({elem:username,msg:"请输入正确的手机号或邮箱"});
				return false;
			}else if(!pwd.val()){
				errorShow({elem:pwd,msg:"请输入密码"});
				return false;
			}else{
				$.getJSON("/get_random_key/?_rand="+Math.random(),function(data){
					$("#login_btn").val("正在提交...");
					var sta = data.status,
						key = data.key;
					if(sta===0){
						$.post("/login?_rand="+Math.random(),{
							_xsrf:getCookie("_xsrf"),
							porm:username.val(),
							password:hex_md5(key+hex_md5(pwd.val()))//md5 两次加密传输数据
						},function(data){
							var status = JSON.parse(data).status,
								msg = JSON.parse(data).msg,
								url = JSON.parse(data).referer || "";
							if(status===0){
								callback && callback();
								showMsg("验证成功",1);
							}else{
								showMsg(msg);
								$("#login_btn").val("提交");
							}
						})
					}else{
						showMsg(msg);
						return false;
					}
				})
				return false;
			}
	})
}

function XHLogin(option){
	var opt = option || "",
		callback = opt.callback,
		url = opt.url;
	var content = '<div class="tab">'+
						'<div class="tab_nav">'+
							'<ul>'+
								'<li class="current">手机验证码登录/注册</li><li>普通登录</li>'+
							'</ul>'+
						'</div>'+
						'<div class="tab_content">'+
							'<div class="item current phone_verify">'+
								'<form>'+
								'<ul class="clearfix">'+
									'<li class="J_no_phone"><input type="text" id="phone" name="phone" maxlength="50" placeholder="请输入手机号码" class="txt">'+
									'<a id="J_get_captcha" class="btn get_captcha">获取验证码</a></li>'+
									'<li ><input type="text" id="verify_code" name="verify_code" maxlength="50" placeholder="请输入手机验证码" class="txt"></li>'+
								'</ul>'+
								'<div class="submit_box">'+
									'<input id="phone_login_btn" type="submit" value="提交" class="btn btn_green">'+
								'</div>'+
								'</form>'+
							'</div>'+
							'<div class="item">'+
								'<form name="Argu" id="login">'+
								'<ul>'+
									'<li><span class="re_ico"></span><span class="re_b"><input type="text" class="txt" placeholder="请输入邮箱或者手机号" maxlength="50" name="porm" id="username"/></span></li>'+
									'<li class="pwd"><span class="re_ico i2"></span><span class="re_b"><input type="password" class="txt" placeholder="请输入密码" maxlength="50" name="password" id="password"/></span></li>'+
								'</ul>'+
								'<div class="submit_box">'+
									'<input id="login_btn" type="submit" value="提交" class="btn btn_green">'+
									'<p><a class="btn J_to_reg" href="/register/">没有账号？去注册>></a></p>'+
									'<p><a class="btn" href="/forget_password/">找回密码</a></p>'+
								'</div>'+
								'</form>'+
							'</div>'+
						'</div>'+
					'</div>'
	var upside = new UpSide({title:"会员登录",content:content})
	$(".tab").tab()//初始化选项卡
	getCaptcha()//绑定获取验证码事件
	phoneLogin(function(){
		if(url){
			upside.close(function(){
				window.location.href = url;
			});
		}else{
			upside.close(function(){
				window.location.reload();
			});
		}
		
	})//绑定手机登录事件
	defaultLogin(function(){
		if(url){
			upside.close(function(){
				window.location.href = url;
			});
		}else{
			upside.close(function(){
				window.location.reload();
			});
		}
	})//绑定普通登录事件
}

function verPhone(title,tips){
	var title = title || "验证手机",
		tips = tips || "",
		userTpl = ""
	if(tips){
		userTpl +=tips;
	}
	userTpl += '<div class="li phone_box"><input type="text" id="phone" class="txt" placeholder="请输入您的手机号码" maxlength="13"/><i></i></div>'+
				   '<div class="li clearfix"><input type="text" id="verify_code" class="txt t2 fl" placeholder="请输入验证码"/><a href="javascript:;"  id="J_get_captcha" class="btn btn_green fr J_get_captcha" style="width:115px">获取验证码</a></div>'+
				   '<div class="li"><input type="button"  id="phone_login_btn" class="btn btn_green submit J_submit" value="提交"/></div>';
	var userDialog = new Dialog({
		title:title,
		content:userTpl,
		style:"new_user"
	})
	getCaptcha()//绑定获取验证码事件
	phoneLogin(function(){
		window.location.reload();
	});
}

//微信检测
function isWeixin(){  
	var ua = navigator.userAgent.toLowerCase();  
	if(ua.match(/MicroMessenger/i)=="micromessenger") {  
		return true;  
	} else {  
		return false;  
	}  
}  



