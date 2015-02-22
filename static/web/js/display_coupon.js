var couponjs = document.getElementById("display_coupon");
var channel = couponjs.getAttribute("channel")
$.get('/get_request_Coupon/?channel='+channel,function(data){
	analyze(data);
})

function analyze(data){
	var html ='';
	 if (typeof(JSON) == 'undefined'){  
	     data = eval("("+data+")");  
	}else{  
	     data = JSON.parse(data);  
	}   
	if(data){
		//<h2>'+data['activity_name']+'</h2>
		html += '<div class="get_coupon index_get_coupon"><div class="hd" style="padding:4px 0 0"></div><div class="bd">';
		switch(data["coupon_type"]){
			case 0:
				html += '<div class="coupon clearfix">'
				break;
			case 1:
				html += '<div class="coupon xh clearfix">'
				break;
			case 2:
				html += '<div class="coupon mq clearfix">'
				break;
			default:
				html += '<div class="coupon py clearfix">'
		}
		html += '<ul>'+
					'<li class="from J_source">来源：'+data['activity_desc']+'</li>'+
					'<li class="date">有效期：'+data["avail_from"]+' - '+data["avail_to"]+'</li>'+
					'<li class="juan">现金券</li>'+
				'</ul>'+
				'<div class="content clearfix">'+
					'<div class="m">'+
						'<span class="ico">￥</span>'+
						'<span class="money J_amount">'+data['amount']+'</span>'+
						'<span class="yuan">元</span>'+
					'</div>'+
				'</div>'+
				'<input type="hidden" class="J_coupon_type" value="'+data['coupon_type']+'"/>'+
				'<input type="hidden" class="J_inteval_days" value="'+data['inteval_days']+'"/>'+
				'<input type="hidden" class="J_activity_id" value="'+data['id']+'"/>'+
				'<div class="btn_box ">'+
					'<p>*定单满<i class="J_limited_order_price">'+data['limited_order_price']+'</i>元即可使用</p>'+
					'<p class="tips">*每张现金券只能在一个订单内使用</p>'+
				'</div>'+
				'</div>'+
				'<div class="sub_box" style="margin-top:-10px"><a id="J_get_coupon" class="btn btn_green">立即领取</a></div>'+
				'</div>'+
				'<a href="javascript:;" class="icon_close2 J_colse"></a>'+
				'</div>';

		var d = dialog({
			title: false,
			fixed:true,
			zIndex:1987,
			lock:true,
			opacity:.3,
			content:html
		});

		d.showModal();
		
		$(function(){
			$("#J_get_coupon").on("click",function(){
					$.post("/get_coupon/?_random="+Math.random(),{
					_xsrf:Base.getCookie("_xsrf"),
					inteval_days:$(".J_inteval_days").val(),
					limited_order_price:$(".J_limited_order_price").html(),
					source:$(".J_source").html(),
					amount:$(".J_amount").html(),
					activity_id:$(".J_activity_id").val(),
					coupon_type:$(".J_coupon_type").val()
				},function(data){
					var status = data.status;
					if(status===0){
						$(".get_coupon").html('<div class="coupon_suc" style="text-align:center;padding-top:20px"><img src="/static/images/smile.png"><p style="padding:10px; color:#df4461; font-size:18px">恭喜！</p><p style="padding:10px; color:#666; font-size:14px">现金券已经领取，结算时即可使用。</p><p><a href="javascript:;" class="J_colse" style="color:#36c">马上去购物>></a></p></div>');
					}else{
						alert("失败了");
					}
				})
			})

			$("body").on("click",".J_colse",function(){
				d.close();
			})
		})
	}
}

