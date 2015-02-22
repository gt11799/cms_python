	function showSize(opt){
		$(".J_wrap_tableBox").remove();
		var tLeft = opt.thisLeft,
			tTop = opt.thisTop,
			tTmp = opt.tTmp,
			cTmp = opt.cTmp,
			tmp = '<div class="J_wrap_tableBox"><div class="J_wrap_tableInfo"><a class="J_close icon_close"></a><div class="J_arrow"></div><table width="100%" bordercolor="#CCCACC" border="0" cellspacing="0" cellpadding="0" id="J_wrap_sizeTemplate" class="J_wrap_sizeTable"><tbody id="J_tableBody">'+
					tTmp+'<tr>'+cTmp+'</tr>'+
				'</tbody></table></div></div>';	
		$(".goods_size").append(tmp);
		var boxHeight = $(".J_wrap_tableBox").height();
		$(".J_wrap_tableBox").css({top:(tTop-boxHeight-10)})
		$(".J_arrow").css({left:(tLeft+25)})
		$(".J_close").click(function(){
			$(".J_wrap_tableBox").remove();
		})
	}
	//检查是否有默认尺码
	function checkSize(){
		var sizeVal = $(".J_size_val"),
			selectItem = $(".J_chioce_size .select"); 
		if(selectItem.length){
			var thisVal= selectItem.attr("data-size");
			sizeVal.val(thisVal);
			
		}else sizeVal.val("");

	}
	//提交后清除已选尺码
	function clearSize(){
		$(".J_size_val").val("");
		$(".J_chioce_size li").removeClass("select");
		$(".J_wrap_tableBox").remove();
	}

	
	//加入购物车成功提示
	function successMsg(){
		var img = $("#slider").find("a").eq(0).html();
			$("body").append('<div class="msg_success">'+img+'</div>');
			$(".msg_success").animate({bottom:64,left:57,width:20,height:20},{duration:600,complete:function(){
				setCarNum();
				$(this).remove();
			}});
	}

	//加入购物车成功更改购物车数
	function setCarNum(){
		var cart = $(".J_cart_num");
		var cartNum = parseInt(cart.html()=="" ? 0 : cart.html() );
		cartNum++;
		cart.html(cartNum);
		$(".J_top_num").html(cartNum);
		cart.css({padding:"10px 12px",borderRadius:"42px"});
		setTimeout(function(){
			$(".J_cart_num").animate({padding:"0 3px",borderRadius:"6px"},600)
		},600)
	}

	function getLike(goods_id){
		$.post("/guess_you_like/?_rand="+Math.random(),{
			_xsrf:getCookie("_xsrf"),
			goods_id:goods_id
		},function(data){
			var status = JSON.parse(data).status,
				goods = JSON.parse(data).goods,
				len = goods.length;
			//console.table(goods)
			var tpl = '<div class="list like clearfix"><div class="hd">猜您喜欢</div><div class="bd"><ul class="clearfix">';
			for(var i=0;i<len;i++){
				tpl += '<li class="list_item"><a href="/detail/'+goods[i].activity_id+'/'+goods[i]._id+'" title="'+goods[i].name+'"><div class="image"><img data-url="'+goods[i].image[0]+'?imageView/1/w/250/h/300" class="load_image"/></div><div class="info clearfix"><h3>'+goods[i].name+'</h3><span class="price red">￥'+goods[i].price+'</span><del class="orig_price">￥'+goods[i].market_price+'</del></div></a></li>'
			}
			tpl += '</ul></div></div>';
			$(".goods_about").after(tpl);
			$('.load_image').imglazyload();
		})
	}