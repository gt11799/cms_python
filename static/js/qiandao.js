$(function () {
	$("#sign").on("click",function(){
		var login = true,
			qiandao = $("#J_qiandao").data("login");
		if (qiandao==1) {
			login = false;
		}

		if(login==false){
			var dialog = new Dialog({
				title:"您尚未登录",
				content:"只有登录后，才能使用签到功能",
				rightTxt:"去登录",
				style:"fast_checkout",
				callback:function(){
					window.location.href = "/login/?from=/qiandao/";
				},
			})
			return;
		}

		if($(this).find(".disabled").length){
			alert("亲，你已经签到过了哦，请明天再来吧！");
			return;
		}
		var that = $(this);
		that.find("i").addClass("disabled").html("正在签到");
		$.getJSON("/sign/?_random="+Math.random(),{
			_xsrf:getCookie("_xsrf")
		},function(data){
			var status = data.status,
				msg = data.msg,
				coinNum = data.coin_num || "0";
			if(status===0){
				that.find("i").html("已签到");
				showfla();
				that.append('<span class="coin_num">+'+coinNum+'</span>');
				$(".coin_num").animate({"bottom":60,"fontSize":"60px","marginLeft":"-26px"},{duration: 500, complete:function(){
					var _that = $(this);
					setTimeout(function(){_that.hide();},800);
					that.addClass("has").attr("href","/qiandao/");
				}});
			}else{
				alert(msg)
				that.addClass("has").attr("href","/qiandao/");
			}
		})
	})
})

function showfla(){
	var i = 0 ;
	$("body").append('<span class="flash_coin_dui"></span>');
	setTimeout(function(){
		$("body").append('<span class="flash_coin fc'+i+'"></span>');
		i++;
		if(i<10){
			setTimeout(arguments.callee,100);
		}
	},100);
	setTimeout(function(){
		$(".flash_coin_dui").remove();
	},2000)
}
