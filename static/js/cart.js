$(function(){
	//选择支付方式时 update运费
	$(".payaway .J_radio_check li").on("click",function(){
		getGoodsForList()
	})
	var type_url = $("#cart_type").val();

	$(".cart_item .J_del").click(function(){
		var that = $(this),
			goodsId = that.attr("data-product"),
			goodsSize = that.attr("data-size");
		var dialog = new Dialog({
			title:"删除商品",
			content:"确定从购物车中删除该商品吗？",
			callback: function(){
				loading.open();
				$.post("/"+type_url+"/del/?_rand="+Math.random(),{
					_xsrf:getCookie("_xsrf"),
					goods_id:goodsId,
					size:goodsSize
				},function(data){
					var status = JSON.parse(data).status;
					if(status==0){
						if($(".cart_item").length<2){
							window.location.reload(); //购物车为空时刷新页面
						}
						that.parents(".cart_item").remove();
						dialog.close();
						getGoodsForList();
					}else{
						showMsg(JSON.parse(data).msg);
					}
					loading.close();
				});
			}
		});
	});

	//订单数减操作
	$(".J_num_cart_reduce").click(function(){
		if($(this).hasClass("disable")){return}
		
		var orderTxt = $(this).siblings(".J_num_cart_txt"),
			orderNum = parseInt(orderTxt.html()),
			goodsId = $(this).parents(".J_pro_num_btn_cart").attr("data-product"),
			goodsSize = $(this).parents(".J_pro_num_btn_cart").attr("data-size");
		if(orderNum==1){$(this).addClass("disable"); return}
		loading.open();
		var that = $(this);
		$.post("/"+type_url+"/change/?_rand="+Math.random(),{
				_xsrf:getCookie("_xsrf"),
				goods_id:goodsId,
				num:(orderNum-1),
				size:goodsSize
			},function(data){
				var status = JSON.parse(data).status;
				if(status==0){
					orderNum--;
					orderTxt.html(orderNum);
					if(orderNum<2){that.addClass("disable")}
					$(".J_num_cart_add").removeClass("disable");
					getGoodsForList();
				}else{
					showMsg(JSON.parse(data).msg);
				}
				loading.close();
		})
	})

	//订单数加操作
	$(".J_num_cart_add").click(function(){
		if($(this).hasClass("disable")){return}
		loading.open();
		var orderTxt = $(this).siblings(".J_num_cart_txt"),
			orderNum = parseInt(orderTxt.html()),
			goodsId = $(this).parents(".J_pro_num_btn_cart").attr("data-product"),
			goodsSize = $(this).parents(".J_pro_num_btn_cart").attr("data-size");

		var that = $(this);
		$.post("/"+type_url+"/change/?_rand="+Math.random(),{
				_xsrf:getCookie("_xsrf"),
				goods_id:goodsId,
				num:(orderNum+1),
				size:goodsSize
			},function(data){
				var status = JSON.parse(data).status;
				if(status==0){
					orderNum++;
					orderTxt.html(orderNum);
					if(orderNum > 1){that.siblings(".J_num_cart_reduce").removeClass("disable")}
					timeOut(1200);
					getGoodsForList()
				}else{
					showMsg(JSON.parse(data).msg);
					that.addClass("disable");
				}
				loading.close();
		})
	})

	$(".JB_cash").iosButton(function(){
		var that = $(".JB_cash"),
			phone = that.data("phone"),
			phoneExp = /0?(13|14|15|18|17)[0-9]{9}/;

		var tpl = '<form>'+
					'<ul class="clearfix" style="padding:10px">';

		if(phoneExp.test(phone)){
			tpl += '<li class="J_no_phone clearfix" style="position:relative; margin-bottom:10px;"><input type="text" id="phone" name="phone" maxlength="50" placeholder="请输入手机号码" value="'+phone+'" class="txt disabled" readonly style="border:1px solid #c1c1c1;width:96%; padding:0 5px; height:40px; line-height:40px;">';
		}else{
			tpl += '<li class="clearfix" style="position:relative; width:100%; margin-bottom:10px;"><input type="text" id="phone" name="phone" maxlength="50" placeholder="请输入手机号码" class="txt" style="border:1px solid #c1c1c1;width:96%; padding:0 5px; height:40px; line-height:40px;">';
				
		}
		tpl +='<a id="J_get_captcha" class="btn get_captcha" style="  padding:0 10px; height:40px; line-height:40px; position:absolute; right:0; top:0">获取验证码</a></li>'+
				'<li ><input type="text" id="verify_code" name="verify_code" maxlength="50" placeholder="请输入手机验证码" class="txt" style="border:1px solid #c1c1c1; width:96%; padding:0 5px; height:40px; line-height:40px;"></li>'+
					'</ul>'+
					'<div class="submit_box">'+
						'<input id="phone_login_btn" type="submit" value="提交" class="btn btn_green" style="padding:10px 40px;  margin-left:10px">'+
					'</div>'+
				'</form>';

		var cashUpSide = new UpSide({
			title:"钱包支付",
			content:tpl,
			cancelback:function(){
				$(".JB_cash").removeClass("checked");
				$("#J_phone").val("");
				$("#J_phone_code").val("");
			}
		})
		getCaptcha();//绑定获取验证码事件
		phoneLogin(function(){
			$("#J_phone").val($("#phone").val());
			$("#J_phone_code").val($("#verify_code").val());
			getGoodsForList();
			cashUpSide.close();
		})

	},function(){
		var paidByHercoin= 0;
		if($(".JB_coin").hasClass("checked")){
			paidByHercoin = 1
		}
		getPriceList(0,paidByHercoin,$("#payaway").val());
		$("#wallet_pwd").val("")
	})

	$(".JB_coin").iosButton(function(){
		var piadByWallet= 0;
		if($(".JB_cash").hasClass("checked")){
			piadByWallet = 1
		}
		getPriceList(piadByWallet,1,$("#payaway").val())
	},function(){
		var piadByWallet= 0;
		if($(".JB_cash").hasClass("checked")){
			piadByWallet = 1
		}
		getPriceList(piadByWallet,0,$("#payaway").val());
		$("#J_phone").val("");
		$("#J_phone_code").val("");
	})


	//取消使用优惠劵
	$("#J_cancel_coupon").on("click",function(){
		var that = $(this),
			couponId = that.data("id");
		var dialog = new Dialog({
			title:"取消优惠券",
			content:"确定取消使用优惠劵吗？",
			callback: function(){
				loading.open();
				$.post("/cancel_cart_coupon/?_rand="+Math.random(),{
					_xsrf:getCookie("_xsrf"),
					coupon_id:couponId
				},function(data){
					var status = JSON.parse(data).status;
					if(status==0){
						showMsg("已取消优惠劵",1);
						dialog.close();
						setTimeout(function(){
							window.location.reload(); 
						},1000)
					}else{
						showMsg("取消失败，请刷新页面试试");
					}
					loading.close();
				});
			}
		})
	})

	//返回上一页url
	// var cartItem = $(".cart_item");
	// if(cartItem.length){
	// 	//console.log(cartItem.length)
	// 	var url = cartItem.eq(0).find("a").attr("href"); 
	// 	$(".J_back_href").attr("href",url);
	// }
	
})

function getGoodsForList(){
	var piadByWallet= 0,
		paidByHercoin= 0,
		payway  = $("#payaway").val(),
		paymentMethod = $("#payaway").val();
	if($(".JB_cash").hasClass("checked")){
		piadByWallet = 1
	}
	if($(".JB_coin").hasClass("checked")){
		paidByHercoin = 1
	}

	getPriceList(piadByWallet,paidByHercoin,paymentMethod)
}

function getPriceList(piadByWallet,paidByHercoin,paymentMethod) {
	var piadByWallet = piadByWallet,
		paidByHercoin=paidByHercoin,
		paymentMethod = paymentMethod || 0;
	loading.open();
	$.post("/order_consume_detail/?source=cart&_rand="+Math.random(),{
			_xsrf:getCookie("_xsrf"),
			paid_by_wallet:piadByWallet,
			paid_by_hercoin:paidByHercoin,
			payment_method:paymentMethod
		},function(data){
			$(".J_price_list").html(JSON.parse(data).data);
			$(".J_yf").html($(".J_yunfei").html());
			loading.close();
	})
}