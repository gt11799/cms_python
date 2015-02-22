function showLoginDialog(phone){
	var userPhone = phone || "",
		title = "输入手机号码，免费领取1件！",
		phoneExp = /0?(13|14|15|18)[0-9]{9}/,
		userPhoneVal = "";
		if(phoneExp.test(userPhone)){
			userPhoneVal = userPhone;
		}

	var userTpl = '<div class="li phone_box"><input type="text" id="phone" class="txt" placeholder="请输入您的手机号码" value="'+userPhoneVal+'" maxlength="13"/><i></i></div>'+
				   '<div class="li clearfix"><input type="text" id="code" class="txt t2 fl" placeholder="请输入验证码"/><a href="javascript:;" class="btn btn_green fr J_get_captcha" style="width:115px">获取验证码</a></div>'+
				   '<div class="li"><input type="button" class="btn btn_green submit J_submit" value="提交"/></div>';

	var userDialog = new Dialog({
		title:title,
		content:userTpl,
		style:"new_user"
	})

	//$("#phone").telReplace();

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
				_xsrf:getCookie("_xsrf"),
				porm:phone.val()
			},function(data){
				var status = JSON.parse(data).status,
					exists = JSON.parse(data).exists;
				if(status==0){
					//已经注册过的用户
					getCaptcha();
				}
			})
		}
	})

	$(".J_submit").on("click",function(){
		var that = $(this);
		if(that.hasClass("disabled")){return}
		if(!$("#phone").val()){
			showMsg("请输入手机号码");
			return;
		}else if(!$("#code").val()){
			showMsg("请输入验证码");
			return;
		}else{
			that.val("提交中...").addClass("disabled");
			$.post("/login_with_verify_code/?_rand="+Math.random(),{
				_xsrf:getCookie("_xsrf"),
				phone:$("#phone").val(),
				verify_code:$("#code").val(),
				source:"fresh_men"
			},function(data){
				var status = JSON.parse(data).status,
					msg = JSON.parse(data).msg || "",
					fresh_men = JSON.parse(data).fresh_men;
				if(status===0){
					if(fresh_men || 1){
						showMsg("验证成功！");
						setTimeout(function(){
							window.location.reload();
						},500)
					}else{
						showMsg("你已不符合本次的活动规则哦");
						userDialog.close();
						$(".J_new_user_box").remove();
					}
				}else{
					showMsg("验证失败"+msg);
					that.val("提交").removeClass("disabled");
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
			_xsrf:getCookie("_xsrf"),
			phone:$("#phone").val(),
			source:"new_user"
		},function(data){
			var status = JSON.parse(data).status,
				msg = JSON.parse(data).msg;
			if(status===0){
				showMsg("验证码已发送至手机",1);
				captchaDom.addClass("disabled");
				timeUp({elem:captchaDom,time:60,callback:function(){
					captchaDom.removeClass("disabled");
					captchaDom.html("重发验证码");
				}})
			}else{
				showMsg(msg || "验证码获取失败，请重试！");
				captchaDom.removeClass("disabled");
			}
		})
	}

