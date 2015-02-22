$(function(){
		var len = parseInt($(".J_new_user_js").data("len"));
		if(len>1){
			var imgSrc =  $(".J_new_user_js").data("src").split(","),
			actId = $(".J_new_user_js").data("actid").split(","),
			imgList = "";
			for(i=0;i<len;i++){
				imgList += '<li><a href="javascript:;" data-href="/fuli/'+actId[i]+'"  class="J_new_user" style="background:url('+imgSrc[i]+') no-repeat center center; display:block; width:100%; height:334px;"></a></li>'
			}

			$("#slider").find(".bd ul").append('<li>'+imgList+'</li>');
			jQuery("#slider").slide({mainCell:".bd ul",titCell:".hd ul",effect:"leftLoop",autoPlay:true, interTime:6000,autoPage:"<li></li>"}).addClass("show");
			
		}else{
			var imgSrc =  $(".J_new_user_js").data("src"), 
				actId = $(".J_new_user_js").data("actid");
			$("#slider").find(".bd ul").append('<li><a href="javascript:;" data-href="/fuli/'+actId+'" class="J_new_user" style="background:url('+imgSrc+') no-repeat center center; display:block; width:100%; height:334px;"></a></li>');
			$("#slider").addClass("show");
		}

		
	var userPhone = $(".J_new_user_js").data("no") || "",
		title = "输入手机号码，参与活动！",
		position = $(".J_new_user_js").data("position"),
		condition = $(".J_new_user_js").data("condition"),
		phoneExp = /0?(13|14|15|18)[0-9]{9}/,
		userPhoneVal = "";
		if(phoneExp.test(userPhone)){
			userPhoneVal = userPhone;
		}

	var userTpl = '<div class="user_pop"><div class="act_title"></div><a href="javascript:;" class="pop_close J_pop_close">关闭</a><div class="li phone_box item clearfix" style="position:relative"><p class="fl"><input type="text" id="phone" class="txt" placeholder="请输入您的手机号码" value="'+userPhoneVal+'" /></p><a href="javascript:;" class="btn btn_green fr J_get_captcha" style="width:100px; margin-left:20px; position:absolute; right:0; top:10px">点击获取验证码</a></div>'+
				   '<div class="li clearfix item"><p><input type="text" id="code" class="txt t2 fl" placeholder="请输入验证码"/></p></div>';
		if(userPhone){
			title = "绑定手机，才能参与活动！";
			userTpl +=  '<div class="li"><input type="button" class="btn btn_green J_submit" value="验证手机"/></div></div>';
		}else{
			userTpl +=  '<div class="li"><input type="button" class="btn btn_green J_submit" value="提交"/></div></div>';
		}

	if(position=="xinshou"){
		showDialog(); //在新手区里面显示登录
	}

	$(".J_new_user").on("click",function(){
		var url = $(this).data("href")
		showDialog(url);
	})

function showDialog(url){
	var href = url;
	var userDialog = dialog({
		id:"new_user",
		title:title,
		content:userTpl,
		fixed:false,
		top:230,
		opacity:0.4,
		width:380
		//style:"new_user"
	})

	userDialog.show()

	new Base.placeholder($('.txt'));

	$(".J_pop_close").on("click",function(){
		userDialog.close().remove();;
	})

	$(".J_get_captcha").on("click",function(){
		if($(this).hasClass("disabled")){return;}
		var phone = $("#phone"),
			submit = $(".J_submit");
		if(!phone.val()){
			showMsg("请输入手机号码");
			return false;
		}else if(!phoneExp.test(phone.val())){
			showMsg("请输入正确手机号码");
			return false;
		}else{
			$.post("/check_account_exist/?_rand="+Math.random(),{
				_xsrf:Base.getCookie("_xsrf"),
				porm:phone.val()
			},function(data){
				var status = data.status,
					exists = data.exists;
				if(status==0){
					//已经注册过的用户
					getCaptcha();
				}
			})
		}
	})

	$(".J_submit").on("click",function(){
		if(!$("#phone").val()){
			showMsg("请输入手机号码");
			return;
		}else if(!$("#code").val()){
			showMsg("请输入验证码");
			return;
		}else{
			$.post("/login_with_verify_code/?_rand="+Math.random(),{
				_xsrf:Base.getCookie("_xsrf"),
				phone:$("#phone").val(),
				verify_code:$("#code").val(),
				source:"fresh_men"
			},function(data){
				var status = data.status,
					msg = data.msg || "",
					fresh_men = data.fresh_men;
				if(status===0){
					if(fresh_men || 1){
						window.location.href = href;
					}else{
						alert("你已经在小荷购买过东西了，不符合本次的活动规则哦");
						userDialog.close().remove();;
						$(".J_new_user_box").remove();
						
					}
				}else{
					showMsg("登录失败"+msg);
				}
			})
		}
	})
}

function getCaptcha(){
		var captchaDom = $(".J_get_captcha");
		if(captchaDom.hasClass("disabled")){return}
		captchaDom.addClass("disabled").html("验证码获取中");
		$.post("/phone_gen_code/?_rand="+Math.random(),{
			_xsrf:Base.getCookie("_xsrf"),
			phone:$("#phone").val(),
			source:"new_user"
		},function(data){
			var status = data.status,
				msg = data.msg;
			if(status===0){
				showMsg("验证码已发送至手机","succeed");
				captchaDom.addClass("disabled");
				timeUp({elem:captchaDom,time:60,callback:function(){
					captchaDom.removeClass("disabled");
					captchaDom.html("重发验证码");
				}})
			}else{
				showMsg(msg);
			}
		})
	}

	function timeUp(opt){
		var time = opt.time,
			callback = opt.callback,
			elem = opt.elem;
		setTimeout(function(){
			elem.html("验证码已发出（倒计时"+time+"）");
			time--;
			if(0<time){
				setTimeout(arguments.callee,1000)
			}else{
				callback && callback()
			}
		},1000)
	}

})
