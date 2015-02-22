function showCart(){
	$.get("/cart_goods/?_rand="+Math.random(),function (data) {
		var status = data.status;
		if(status==0){
			var	cart = data.cart,
				cartContent = cart.cart,
				len = cartContent.length,
				price = cart.sum_price;
			var tpl = "<ul>";
			for(var i=0;i<len;i++){
				i == len-1 ?  tpl+='<li class="clearfix last">' : tpl+='<li class="clearfix">';
				tpl+='<p class="fl" style="margin-right:10px"><a href="/cart/"><img src="'+cartContent[i].image[0]+'" width="60"/></a></p>'
				+'<span class="fr red">¥'+cartContent[i].price+'</span>'
				+'<p><a href="/show/'+cartContent[i].event_id+'/'+cartContent[i]._id+'">'+cartContent[i].goods_name+'</a></p><p>数量：x'+cartContent[i].num+' &nbsp;&nbsp; 尺码：'+cartContent[i].mark+'</p></li>';
				if(i>3){
					tpl+='<li><a href="/cart/v2" style="display:block; text-align:center; background:#f5f5f5; padding:5px">查看全部</a></li>';
					break;
				}
			}
			tpl +="</ul>";
			$(".J_cart_panel .J_cart_tips").html(''+len+'件商品,请尽快结算');
			$(".J_cart_panel .bd").html(tpl);
			$(".J_cart_panel .J_sum_price").html("¥"+price);
			//如果有商品显示则结算按钮
			$('.J_nogoods').css('display','block');
			$(".J_cart").append('<span class="point">'+len+'</span>');
			$(".header .cart_info .icon").html('<span class="point">'+len+'</span>');

		}
	})
}

$(function(){
	showCart()

	var noLogin = $("#side").data("nologin");
	if(noLogin!=1){
		$.get("/order_wait_for_pay/?_rand="+Math.random(),function (data) {
			var status = data.status;
			if(status==0){
				var	orders = data.orders,
					len = orders.length;
				if(!orders.length){
					return;
				}else{
					$(".J_unpay_panel .bd").html("");
					var	price = 0;
					for(var i=0;i<len;i++){
						var tpl = "<ul>",
							goodsLen = orders[i].goods.length;
						i == len-1 ?  tpl+='<li class="clearfix last">' : tpl+='<li class="clearfix">';
						tpl+='<p class="fl" style="margin-right:10px"><a href="/user_order_list_detail/?order_no='+orders[i].order_no+'" target="_blank">'
						+'<img src="'+orders[i].goods[0].image+'" width="70"/></a></p>'
						+'<span class="fr" style="margin:10px 10px 0"> x'+goodsLen+'</span>'
						+'<p><a href="/user_order_list_detail/?order_no='+orders[i].order_no+'" target="_blank">'+orders[i].goods[0].product_name+'</a></p>'
						+'<p style="margin-top:5px">待支付金额：<span class="red">¥'+orders[i].total_pay+'</span></p>'
						+'<p style="margin-top:10px"><span class="order_time"><span class="J_order_time'+i+' red"></span>后取消订单</span>'
						+'<a class="btn btn_green fr" href="/submit_payment/?order_no='+orders[i].order_no+'" target="_blank">立即支付</a></p></li>';
						if(i>1){
							tpl+='<li><a href="/user_order_list_unpay/" style="display:block; text-align:center; background:#f5f5f5; padding:5px">查看全部</a></li>';
							price += orders[i].total_pay;
						$(".J_unpay_panel .bd").append(tpl);
						Base.timeOut($(".J_order_time"+i+""),orders[i].ttl);
							break;
						}
						price += orders[i].total_pay;
						$(".J_unpay_panel .bd").append(tpl);
						Base.timeOut($(".J_order_time"+i+""),orders[i].ttl);
					}
					tpl +="</ul>";
					$(".J_unpay_panel .hd").html('您有'+len+'订单待支付,请尽快完成支付');
					
					$(".J_unpay_panel .J_sum_price").html("¥"+price);
					$(".J_unpay").append('<span class="point">'+len+'</span>');
				}
			}
		})
	}

	$(".J_show_cart").on("mouseover",function(){
		$(this).find(".cart_panel").show();
	});
	$(".J_show_cart").on("mouseout",function(){
		$(this).find(".cart_panel").hide();
	});

	$(".J_backtop").on("click",function(){
		$("body,html").animate({"scrollTop":0},600)
	})

	$("body").on("click",".J_show_contact",function(){

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

		return false;
	})
})

