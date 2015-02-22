	$(function(){
		var phone = "{{handler.get_user_porm()}}" || '';

		$("body").on("mouseover",".goodsList li",function(){
			var sizeBox = $(this).find(".J_size_box"),
				addCartHeight = sizeBox.height();
			sizeBox.css({"top":-addCartHeight});
			$(this).addClass("hover");
		})

		$("body").on("mouseout",".goodsList li",function(){
			$(this).find(".J_size_box").css({"top":0})
			$(this).removeClass("hover");
		})

		$("body").on("click",".J_select_size .size",function(){
			var that = $(this);
			if(that.hasClass("disabled")){return}
			that.addClass("select").siblings().removeClass("select");
			that.siblings(".J_size_val").val(that.data("val"));

		})


	//加入购物车
	$("body").on("click",".J_add_cart",function(e){
		e.stopPropagation();
		var that = $(this),
			id = that.data('id'),
			sizeVal = that.parents("li").find(".J_size_val").val(),
			position = $("#user_position").val() || "快捷加入购物车按钮";
		//alert(sizeVal)
		if(!sizeVal){
			showAddCart(that.parents("li").find(".J_select_size").attr("id"));
			return;
		}
		loading.open();
		$.post("/cart/add?_rand="+Math.random(),{
			_xsrf:Base.getCookie("_xsrf"),
			goods_id:id,
			size:sizeVal,
			num : 1
		},function(data){
			if(data.status===0){

				var tpl  = '<a href="javascript:;" class="close_cart_sucuss J_close_cart_sucuss"></a><table width="532">'+
								'<tr><td><img src='+that.parents("li").find("img").attr("src")+' width="180" height="220"/></td><td valign="top" style="padding-left:24px"><h1 style="font-size:16px; color:#333">已成功加入购物车!</h1><h2 style="font-size:14px; color:#666; margin:20px 0 14px">'+that.parents("li").find("h2").html()+'</h2><p style="font-size:14px; color:#666">尺码：'+sizeVal+'</p><p style="margin-top:36px"><a href="javascript:;" class="btn btn_default J_close_cart_sucuss" style="width:90px">继续购物</a><a href="/cart/v2" class="btn btn_green " style="width:90px; margin-left:30px">立即结算</a></p></td></tr>'+
							 '</table>'

				var d2 = dialog({
					title:false,
					content:tpl,
					skin:"sucuss_tocart",
					padding:"14px"
					//quickClose:true
				})

				d2.showModal();

				//绑定关闭事件
				$(".J_close_cart_sucuss").on("click",function(){
					d2.close().remove();
				})

				showCart(); //更新侧栏购物车
				showSideContent(1);

				_hmt.push(['_trackEvent','（PC）'+position+'加入购物车按钮', '加入购物车']);

			}else if(data.status<0){
				showLoginDialog(phone); //加入购物车前验证是否验证了手机
			}else{
				showMsg(data.msg || "出错了，请联系客服解决哦")
			}
			loading.close();
			return false;
		}); 
	})

	})


	function showAddCart(id){
		var d = dialog({
				title:false,
				content:'请选择尺码',
				align:"top",
				padding:"6px 40px",
				skin:"normal"
			})
			d.show(document.getElementById(id));
		setTimeout(function(){
			d.close().remove();
		},2000)
	}