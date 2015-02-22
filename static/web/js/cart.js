$(function(){
	//初始化支付方式选项卡
	$(".tab").tab(); 

	//初始化支付方式radio
	setRadio("J_radio_1"); 

	//地址hover
	$(".J_address ul li").hover(function(){
		$(this).addClass("hover");
	},function(){
		$(this).removeClass("hover");
	})

	//选择支付方式
	$(".J_payway").on("click",".payway_item",function(){
		getGoodsForList();
	})

	//选择地址
	$(".J_address ul li").on("click",function(){
		if($(this).hasClass("J_add_addr")){return}
		$(this).addClass("select").siblings().removeClass("select");
		cartLog(0);
	})

	//激活优惠劵
	$(".J_jihuo_coupons .txt").on("focus",function  () {
		var that = $(this)
		that.siblings("a").removeClass("disabled").addClass("btn_green");
	})

	//显示3元运费补贴
	$(".J_butie").on("click",function(){
		var d = dialog({
			title:false,
			content:'<a class="J_close_butie" href="javascript:;"><img src="/static/web/images/cart/show_butie.jpg"></a>',
			padding:0,
			skin:"normal",
			autofocus:true,
			fixed:true
			//quickClose:true
		})

		d.showModal();

		$(".J_close_butie").on("click",function(){
			d.close().remove();
		})
	})


	$(".J_jihuo_coupons .txt").on("blur",function  () {
		var that = $(this)
		if(that.val().length==0){
			that.siblings("a").removeClass("btn_green").addClass("disabled");
		}
	})

	$(".J_jihuo_coupons").find("a").on("click",function(){
		if($(this).hasClass("disabled")){return;}
		$.post("/redeem_coupon/?_rand="+Math.random(),{
			_xsrf:Base.getCookie("_xsrf"),
			gift_code:$(".J_jihuo_coupons .txt").val()
		},function(data){
			var status = data.status,
			msg  = data.msg || "兑换失败，请检查兑换是否正确";
			if(status===0){
				showMsg("兑换成功");
				window.location.reload();
			}else{
				showMsg(msg,"coupons_code");
			}
		})
	})

	//显示福利
	$(".J_fuli_item .J_show").on("click",function(){
		var fuli = $(this).parents(".fuli");
		if(fuli.hasClass("show")){
			fuli.removeClass("show")
		}else{
			fuli.addClass("show")
		}
		//初始化钱包支付
		if(fuli.hasClass("J_xiaoher_cash")){
			var phone = fuli.data("phone"),
				phoneExp = /0?(13|14|15|18)[0-9]{9}/;
			if(phoneExp.test(phone)){
				fuli.find("#phone").val(phone).addClass("disabled").attr("readonly",true);
			}

			getCaptcha($("#J_get_captcha"));
			phoneLogin($("#phone_login_btn"),function(){
				$("#J_use_cash").val("1");
				$("#wallet_code").val($("#verify_code").val());
				getGoodsForList(function(){
					setTimeout(function(){
						var tpl = $(".J_cash_used").html() + ' <a class="J_cancel_cash" href="javascript:;">取消使用<a/>';
						fuli.find(".J_used_cash").html(tpl);
						fuli.find(".item_content").hide(500,function(){
							fuli.removeClass("show");
						});
					},1000)
				})
			});
			//取消使用荷币
			$(".J_fuli_item").on("click",".J_cancel_cash",function(){
				$("#J_use_cash").val(0);
				var that = $(this);
				getGoodsForList(function(){
					showMsg("取消成功！");
					that.parents(".J_used_cash").html("");
				});
			})
		}
	})
	
	$(".tab .tab_content li").on("click",function(e){
		e.stopPropagation();
	 	$(".tab .tab_content li").removeClass("current");
		$(this).addClass("current");
		getGoodsForList();
	})

	//显示全部地址
	$(".J_show_addr").on("click",function(){
		var len = $(".J_address .address_list li").length,
			height = $(".J_address .address_list li").outerHeight(true),
			i = Math.ceil(len/3);
		$(".J_address .address_list").css({"height":height*i});
		$(this).remove();
	})

	var type_url = "cart"; //曾经是有缺货预定的

	//新增地址
	$(".J_add_addr").on("click",function(){
		// var d = dialog({
		// 	title:"新增收货地址",
		// 	content:"<iframe sr></iframe>"
		// })
		// d.show()
	})

	//使用荷币
	$(".J_user_xiaohercoin").on("click",function(){
		$("#J_user_coin").val(1);
		var that = $(this);
		getGoodsForList(function(){
			showMsg("使用成功！");
			setTimeout(function(){
				var tpl = $(".J_coin_used").html() + ' <a class="J_cancel_coin" href="javascript:;">取消使用<a/>';
				that.parents(".J_fuli_item").find(".J_used_coin").html(tpl);
				that.parents(".item_content").hide(500,function(){
					that.parents(".fuli").removeClass("show");
				});
			},1000)
		});
	})

	//取消使用荷币
	$(".J_fuli_item").on("click",".J_cancel_coin",function(){
		$("#J_user_coin").val(0);
		var that = $(this);
		getGoodsForList(function(){
			showMsg("取消成功！");
			that.parents(".J_used_coin").html("");
		});
	})

	//使用优惠劵
	$(".J_fuli_item").on("click",".J_use_coupon",function(){
		var  that = $(this),
			id = that.data("id");
		$.post("/cart_bonus/",{
			_xsrf:Base.getCookie("_xsrf"),
			coupon_id:id
			},function(data){
			var status = data.status,
				msg = data.message || "";
			if(status===0){
				getGoodsForList(function(){
					showMsg("使用成功！");
					setTimeout(function(){
						var tpl = '<span class="used_conpon">'+$(".J_coupon_used").html() + ' <a class="J_cancel_coupon" href="javascript:;" data-id="'+id+'">取消使用<a/></span>';
						that.parents(".J_fuli_item").find(".J_used_coupon").html(tpl);
						that.parents(".item_content").hide(500,function(){
							that.parents(".fuli").removeClass("show");
						});
					},1000)
				});
			}else{
				showMsg("失败了"+msg)
			}
		})
	})

	//取消使用优惠劵
	$(".J_fuli_item").on("click",".J_cancel_coupon",function(){
		var that = $(this),
			couponId = that.data("id");
		var d = dialog({
			title:"取消优惠券",
			content:"确定取消使用优惠劵吗？",
			okValue:"确定",
			cancelValue:'取消',
			ok: function(){
				loading.open();
				$.post("/cancel_cart_coupon/?_rand="+Math.random(),{
					_xsrf:Base.getCookie("_xsrf"),
					coupon_id:couponId
				},function(data){
					var status = data.status;
					if(status==0){
						showMsg("已取消优惠劵");
						d.close();
						getGoodsForList(function(){
							that.parents(".J_fuli_item").find(".J_used_coupon").html("");
						});
					}else{
						showMsg("取消失败，请刷新页面试试");
					}
					loading.close();
				});
			},cancel:function(){}
		})
		d.show();
	})
		

	//删除地址
	$(".J_address_del").click(function(e){
		e.stopPropagation();
		var that = $(this),
			id = that.parents("li").attr("id"); 
		var d = dialog({
			title: '提示',
			content:'您确定要删除这个收货地址吗？',
			okValue:"确定",
			cancelValue:"取消",
			ok : function(){
				$.post("/delete_address/?_random="+Math.random(),{
					_xsrf:Base.getCookie("_xsrf"),
					address_id:that.data("id")
				},function(data){
					var data = $.parseJSON(data);
					if(data.status==0){
						that.parents("li").remove();
						showMsg("地址已删除成功！");
					}else{
						showMsg("删除失败，请重试！")
					}
				});
			},
			cancel:function(){}
		});
		d.show(document.getElementById(id));
		return false;
	});

	$('.cart_item .J_del').click(function(){
		var that = $(this),
			goodsId = that.attr("data-product"),
			goodsSize = that.attr("data-size"),
			id = that.attr("id");

		var d = dialog({
			title: '提示',
			content:"确定从购物车中删除该商品吗？",
			okValue : '确定',
			cancelValue:'取消',
			cancel:true,
			ok : function(){
				loading.open();
				$.post("/"+type_url+"/del/?_rand="+Math.random(),{
					_xsrf:Base.getCookie("_xsrf"),
					goods_id:goodsId,
					size:goodsSize
				},function(data){
					var status = data.status,
						marketPrice = data.sum_price;
					if(status==0){
						if($(".cart_item").length<2){
							window.location.reload(); //购物车为空时刷新页面
							return;
						}
						getGoodsForList();
						that.parents(".cart_item").remove();
					}else{
						showMsg(data.msg);
					}
					loading.close();
				});
			}
		});
		d.show(document.getElementById(id))
		return false;
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
				_xsrf:Base.getCookie("_xsrf"),
				goods_id:goodsId,
				num:(orderNum-1),
				size:goodsSize
			},function(data){
				var status = data.status,
					marketPrice = data.sum_price;
				if(status==0){
					orderNum--;
					orderTxt.html(orderNum);
					if(orderNum<2){that.addClass("disable")}
					$(".J_num_cart_add").removeClass("disable");
					getGoodsForList();
				}else{
					showMsg(data.msg);
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
				_xsrf:Base.getCookie("_xsrf"),
				goods_id:goodsId,
				num:(orderNum+1),
				size:goodsSize
			},function(data){
				var status = data.status,
					marketPrice = data.sum_price;
				if(status==0){
					orderNum++;
					orderTxt.html(orderNum);
					if(orderNum > 1){that.siblings(".J_num_cart_reduce").removeClass("disable")}
					getGoodsForList();
				}else{
					showMsg(data.msg);
					that.addClass("disable");
				}
				loading.close();
		})
	})


	// $(".J_use_fuli :checkbox").on("change",function(){
	// 	getGoodsForList()
	// })

	//返回上一页url
	// var cartItem = $(".cart_item");
	// if(cartItem.length){
	// 	//console.log(cartItem.length)
	// 	var url = cartItem.eq(0).find("a").attr("href"); 
	// 	$(".J_back_href").attr("href",url);
	// }
	$("a").attr("onclick","return cartLog(this)")
	// $("a").on("click",function(){
	// 	var that = $(this);
	// 	 cartLog(that)
	// })
	
});

function getGoodsForList(callback){
	var piadByWallet= $("#J_use_cash").val() || 0,
		paidByHercoin= $("#J_user_coin").val() || 0,
		paymentMethod = $(".J_radio_1.select").data("value") || 0;
	getPriceList(piadByWallet,paidByHercoin,paymentMethod,callback);
}

function getPriceList(piadByWallet,paidByHercoin,paymentMethod,callback) {
	var piadByWallet = piadByWallet,
		paidByHercoin=paidByHercoin,
		paymentMethod = paymentMethod;
	$.post("/order_consume_detail/?source=cart&_rand="+Math.random(),{
			_xsrf:Base.getCookie("_xsrf"),
			paid_by_wallet:piadByWallet,
			paid_by_hercoin:paidByHercoin,
			payment_method:paymentMethod
		},function(data){
			$(".J_price_list").html(data.data);
			callback && callback();
	});
	cartLog(0);
}

function setRadio(elem){
	var elem = $("."+elem+"");
		elem.on("click",function(){
			elem.removeClass("select");
			$(this).addClass("select");
		})
}

function cartLog(that){
	//return false;
	var leaveMethod = 0 ,//离开购物车方式
		complete = 0,
		paymentMethod = $(".J_radio_1.select").data("value") || 0 ,
		that = that;
	if(that!=0){
		if (that==2) {
			leaveMethod = 2;
		}else if(that!="javascript:;"){
			leaveMethod = 1;
		}else{
			leaveMethod = 0
		}
	}


	if($(".J_radio_1.i2").hasClass("select")){
		if($(".tab_nav li.current").index()==1){
			paymentMethod = 2
		}else if($(".tab_nav li.current").index()==2){
			paymentMethod =3 ;
		}
	}

	$.ajax({
		url:"/cart/addCartLog/?_rand="+Math.random(),
		type:"post",
		data:{
			_xsrf:Base.getCookie("_xsrf"),
			address_id:addressId = $(".J_address .address_list li.select").data("id") || 0,
			leave_method:leaveMethod,
			payment_method:paymentMethod
		},
		async:false,
		success:function(data){
			complete = 1
		}
	})
	if(complete == 1){
		return true;
	}
}