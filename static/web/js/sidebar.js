$(function(){

	$(".J_show_side_content").on("click",function(){
		$(this).addClass("current").siblings().removeClass("current").find(".tips").hide();
		$(this).find(".tips").hide();
		var sideContent = $("#J_sidebar_content"),
			tpl = $(this).find(".content"),
			index = $(this).index(".J_show_side_content");
		 showSideContent(index);	
	})

	$("#J_sidebar").on("click",function(e){
		e.stopPropagation();
	})

	$("body").on("click",function(){
		var sideContent = $("#J_sidebar_content");
		if(sideContent.hasClass("show")){
			hideSideContent();
		}
	})

	showCart(); //获取购物车内容
	showWish(); //获取心愿单内容

	var noLogin = $("#J_sidebar_js").data("nologin");

	if(noLogin!=1){
		getUnpay();
	}

	$.xhSetTimeout(function(){
		$("#J_sidebar").addClass("show");
	},500);

	$(".J_contact").showContact(); //初始化客服
	$("#J_sidebar .bar").xhHover({sub:"tips",cssCondition:"current"}) //初始化hover效果
	$.scrollToFix({elem:"J_backtop",time:600})  //绑定回顶部效果

})

function showSideContent(index,autoClose){
	var sideContent = $("#J_sidebar_content");
	sideContent.addClass("show").find(".J_s_content").eq(index).fadeIn().siblings().hide();
	if(autoClose){
		$.xhSetTimeout(function(){
			hideSideContent();
		},2000);
	}
	sideContent.find(".J_colse").on("click",function(){
		hideSideContent();
	});
}

function hideSideContent(){
	$("#J_sidebar_content").removeClass("show");
	$(".J_show_side_content").removeClass("current");
}

function showCart(){
	$.get("/cart_goods/?_rand="+Math.random(),function (data) {
		var status = data.status,
			barCart = $(".J_bar_cart"),
			contentCart = $(".J_content_cart");

		if(status==0){
			var	cart = data.cart,
				cartContent = cart.cart,
				len = cartContent.length,
                num = cart.sum_num,
				price = cart.sum_price,
				ttl = cart.ttl;
			var tpl = "";
			for(var i=0;i<len;i++){
				i == len-1 ?  tpl+='<dl class="side_cart_list clearfix last">' : tpl+='<dl class="side_cart_list clearfix">';
				tpl+='<dt><a href="/detail/'+cartContent[i].event_id+'/'+cartContent[i].id+'"><img src="'+cartContent[i].image[0]+'?imageView/1/w/120/h/156/q/100/interlace/1" width="60"/></a></dt>'
				+'<p><a href="/detail/'+cartContent[i].event_id+'/'+cartContent[i].id+'">'+cartContent[i].goods_name+'</a></p><div class="dd_wrap clearfix"><dd class="cart_size">尺码&nbsp;&nbsp;'+cartContent[i].mark+'</dd>'
				+'<dd class="d1">数量&nbsp;&nbsp;'+cartContent[i].num+'</dd><dd class="red"> ¥'+cartContent[i].price+'</dd></div>'
				+'<p class="delete"><a href="#" class="J_del fr" data-product='+cartContent[i].id+' data-size='+cartContent[i].mark+' id="sidebar_del_'+i+'""><img src="/static/web/images/cart/delete.png" /></a></p>'
				+'</dl>'
				;
				if(i>3){
					tpl+='<p><a href="/cart/v2" style="display:block; text-align:center; background:#f5f5f5; padding:5px; margin-bottom:10px">查看全部</a></p>';
					break;
				}
			}

			tpl += '<div class="submit clearfix"><p class="total fl red">总额：¥'+price+'</p><p class="fr"><a class="btn btn_primary" href="/cart/v2">去购物车结算</a></p></div>'

			contentCart.find(".bd").html(tpl);

			if(typeof(cartTimer)!="undefined"){
				cartTimer.clear();  //这个全局timer 我也不想的
			}

			if(!barCart.find(".tips .icon_time").length){
				barCart.find(".tips").prepend('<i class="icon_time"></i>');
				$("#J_sidebar_content .J_cart_time").before('<i class="icon_time"></i>')
			}
			
			cartTimer = new xhTimeOut({
				elem:$(".J_cart_time"),
				maxtime:ttl,
				mselem:$(".J_sidebar_cart_ms"),
				callback:function(){
					window.location.reload();
				},
				timebacktt:600,
				timeback:function(){
					setTimeout(function(){
						$(".J_bar_cart .tips").show().addClass("show");
					},1000)
				}
			})
			$(".J_cart_num").html(num);
			$(".header .cart_info .icon").html('<span class="point">'+num+'</span>');
			if(!$(".cart_body").length && !$(".J_unpay_num").length){
				$.xhSetTimeout(function(){
					showSideContent(1);
				},1000)
			}
		}else{
			contentCart.find(".bd").html('<div class="no"><div class="no_goods_icon"></div><p>您的小荷购物车还是空的，</p><p>快去抢购喜欢的商品吧~</p></div>')
		}
	})
}

function showWish(){
	$.get("/wishlists/display/wishlist_sider?_rand="+Math.random(), function (data) {
		var content = $(".J_content_wish");
		if(data.status==0){
			if(data.future.length){
				$('.J_wish_num').text(data.future.length).show();
				content.find(".J_being_no").remove();
				content.find(".J_being_has").show();
				wishTpl(data.future, content.find(".J_being_has"), 'being');
			}
			if(data.today.length){
				content.find(".J_today_no").remove();
				content.find(".J_today_has").show();
				wishTpl(data.today,content.find(".J_today_has"),'today');
			}
		}
	})
}

function wishTpl(data,wrap,type){

	var tpl = '';
	var isSingleFirst = true;
	var isActivityFirst = true;

	$.each(data, function(k,v){
		
		var timeTpl = '',
			btnTpl = '',
			titTpl = '',
			tipTxt = '许愿',
			saleOutClass = '';

		if(type!='today'){
			timeTpl = '<div class="being_time"><span>' + v.timestamp +'</span>开抢</div>';
		}

		if(type=='today' && v.type=='single'){
			btnTpl = '<p class="clearfix"><a style="padding:4px 12px;clear:both;" class="btn btn_green fr" href="/detail/'+ v.activity_id+'/' + v.goods_id +'" target="_blank">加入购物车</a>'; 
			if(isSingleFirst){
				titTpl = '<h3><span>单品疯抢</span></h3>';
				isSingleFirst = false;
			}
		}

		if(type=='today' && v.type=='activity'){
			btnTpl = '<p class="clearfix"><a style="padding:4px 12px;clear:both;" class="btn btn_green fr" href="/show/' + v.activity_id +'" target="_blank">立即抢购</a>'; 
			if(isActivityFirst){
				titTpl = '<h3><span>活动疯抢</span></h3>';
				isActivityFirst = false; 
			}
		}

		if(type=='today'){
			tipTxt = '参与';
			if(v.sale_out==true){
				saleOutClass = 'sale_out';
				btnTpl = '<p class="clearfix"><span style="padding:4px 12px;clear:both;" class="btn fr">已抢光</span>'; 
			}
		}

		if(type!='today' && v.type=='single' && isSingleFirst){
			titTpl = '<h3 class="disable"><span class="disable">单品预定</span></h3>';
			isSingleFirst = false;
		}

		if(type!='today' && v.type=='activity' && isActivityFirst){
			titTpl = '<h3 class="disable"><span class="disable">活动预定</span></h3>';
			isActivityFirst = false;
		}
	
		var singleTpl = 
			'<div class="item_1 ' + saleOutClass + '">' + titTpl + '<dl class="side_cart_list clearfix">' + 
				timeTpl + 
				'<dt><a href="/detail/' +  v['activity_id'] +'/' + v.goods_id + '" target="_blank">' + 
				'<img width="72" height="86" src="' + v.image+'?imageView/1/w/72/h/86/q/100/interlace/1' +'"></a>' + 
				'</dt>' + 
				'<div>' + 
				'<p class="wish_tit"><a href="/detail/' +  v['activity_id'] +'/' + v.goods_id + '" target="_blank" title="' + v.name + '">' + v.name +'</a></p>' + 
				'<p>已经有<i class="red">' + v.same_wish_number +'</i>人' + tipTxt +'</p>' + 
				'<p class="clearfix"><del class="fr">￥'+ v.market_price +'</del><b class="red fs16">￥'+ v.price +'</b></p>' +
				btnTpl +
				'</p>' + 
				'</div>' +
				'</dl></div>';

		var activityTpl = 
			'<div class="item_2 ' + saleOutClass + '">' + titTpl + '<dl class="side_cart_list clearfix act_tpl">' + 
				timeTpl +
				'<dt><a href="/show/' +  v['activity_id'] +'" target="_blank">' + 
				'<img width="250" height="102" src="' + v.image+'?imageView/1/w/250/h/102/q/100/interlace/1' +'"></a>' + 
				'</dt>' + 
				'<dd>' + 
				'<p class="wish_tit"><a class="link" href="/show/' +  v['activity_id'] +'" target="_blank" title="' +v.name + '">' + v.name +'</a><span class="fr fs12">已经有<i class="red">' + v.same_wish_number +'</i>人' + tipTxt +'</span></p>' + 
				btnTpl +
				'</dd>' + 
				'</dl></div>';

		if(v.type=='single'){
			tpl += singleTpl;
		}else{
			tpl += activityTpl;
		}

	});

	wrap.html(tpl);

	//今日预定 计时器
	$.each($('.being_time'),function(){
		var timer = new xhTimeOut({
			elem: $(this).find('span'),
			maxtime : Number($(this).find('span').text()),
			callback:function(){
			}
		})
	});

	//今日预定，活动不能点击
	$('.J_being_has .act_tpl').on('click',function(){
		return false;
	}).find('a').css('cursor','default');

	//抢光了
	$('.J_today_has .sale_out').on('click',function(){
		return false;
	}).find('a').css('cursor','default');

	
}

function getUnpay(){
	$.get("/order_wait_for_pay/?_rand="+Math.random(),function (data) {
		var status = data.status,
			unpayElem = $(".J_bar_unpay");
		if(status==0){
			var	orders = data.orders,
				len = orders.length;
			if(!orders.length){
				return;
			}else{
				$(".J_content_unpay .bd").removeClass("no").html("");
				var	price = 0;
				for(var i=0;i<len;i++){
					var tpl = "",
						goodsLen = orders[i].goods.length;
					i == len-1 ?  tpl+='<dl class="side_cart_list clearfix last">' : tpl+='<dl class="side_cart_list clearfix">';
					tpl+='<dt><a href="/user_order_list_detail/?order_no='+orders[i].order_no+'" target="_blank">'
					+'<img src="'+orders[i].goods[0].image+'" width="70"/></a></dt><p>'
					+'<a href="/user_order_list_detail/?order_no='+orders[i].order_no+'" target="_blank">'+orders[i].goods[0].product_name+'</a></p>'
					+'<dd class="d1"> 数量 &nbsp;'+goodsLen+'</dd>'
					+'<dd><span class="red">¥'+orders[i].total_pay+'</span></dd></dl>'
					+'<div class="submit clearfix"><p class="total fl red" style="font-size:13px"><span class="order_time"><span class="J_order_time'+i+' red"></span>后取消订单</span></p>'
					+'<p class="fr"><a class="btn btn_primary" href="/submit_payment/?order_no='+orders[i].order_no+'" target="_blank">立即支付</a></p></div>';
					if(i>1){
						tpl+='<p><a href="/user_order_list_unpay/" style="display:block; text-align:center; background:#f5f5f5; padding:5px">查看全部</a></p>';
						price += orders[i].total_pay;
						$(".J_content_unpay .bd").append(tpl);
						var timer2 = new xhTimeOut({
							elem:$(".J_order_time"+i+""),
							maxtime:orders[i].ttl,
							callback:function(){
								window.location.reload();
							}
						})
						break;
					}
					price += orders[i].total_pay;
					$(".J_content_unpay .bd").append(tpl);
					var timer2 = new xhTimeOut({
						elem:$(".J_order_time"+i+""),
						maxtime:orders[i].ttl,
						callback:function(){
							window.location.reload();
						}
					})
				}
				//unpayElem.find(".hd").html('您有'+len+'订单待支付,请尽快完成支付');
				//unpayElem.find(".tips").show().find(".J_txt").html('<span class="red">有'+len+'个待支付订单</span>');
				if(!$(".unpay_body").length){
					$.xhSetTimeout(function(){
						unpayElem.find(".tips").addClass("show");
						showSideContent(0);
					},1000);
				}
				$(".J_unpay_panel .J_sum_price").html("¥"+price);
				unpayElem.find(".bar_top_a").append('<i class="icon cart_num J_unpay_num">'+len+'</i>');

			}
		}else{

		}
	})
};

//侧边栏删除功能
$('.J_content_cart').on('click','.J_del', function(){
	
	var _this = $(this),
		goodsId = _this.attr("data-product"),
		goodsSize = _this.attr("data-size"),
		id = _this.attr("id");


	// var d = dialog({
	// 	id:"test",
	// 	title: '提示',
	// 	content:"确定从购物车中删除该商品吗？",
	// 	okValue : '确定',
	// 	cancelValue:'取消',
	// 	cancel:true,
	// 	align:'left',
	// 	zIndex:10000,
	// 	ok : function(){
			loading.open();
			$.post("/cart/del/?_rand="+Math.random(),{
				_xsrf:Base.getCookie("_xsrf"),
				goods_id:goodsId,
				size:goodsSize
			},function(data){
				var status = data.status,
					marketPrice = data.sum_price;
				if(status==0){
					showCart();
				}else{
					showMsg(data.msg);
				}
				loading.close();
			});
	// 	}
	// });

	// d.show(document.getElementById(id));

	return false;
});

