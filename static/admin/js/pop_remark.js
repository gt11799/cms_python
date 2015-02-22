

function popEditRemark(txta){

	txta.on('click',function(){

		var isEdit = []; //判定是否发生修改成功，若成功，关闭窗口时刷新页面。
		var thisId = $(this).attr('pop-id');

		app.loading.open("正在加载数据...");
		$.ajax({
			url: "/admin/get_order_series_mark/?order_no=" + $(this).attr('order-no'), //+ $(this).attr('order-no'),

			success: function(data){
			  app.loading.close();
			  if(!data.status==0){
			  	showMsg('修改失败! 错误代码：' + data.msg,3);
			  }else{
			  		
			  		var dom = $('<div style="max-height:700px; overflow-y:auto;">' + 
			  			'<table class="remarks_table table_list">' +
					  		'<tr><th class="type" width="120">相关备注类型</th><th width="300">备注内容</th><th width="100">相关号</th><th width="100">操作</th></tr>' + 
					  	'</table>' +
					  '</div>'),
			  		table = dom.find('.remarks_table'),

			  		order_remark = data['orderMark']['reserved_2'] || '';

			  		//订单审核
			  		$('<tr class="orderMark"><td class="tit">订单审核：</td><td>' + 
			  			'<textarea class="txta" data-type="0" data-id="' + data['orderMark']['order_id'] + '">' + order_remark + '</textarea>' + 
			  			'</td><td>' + data['orderMark']['order_id'] + '</td><td><a class="btn btn_green">提交</a></td></tr>').appendTo(table);

			  		//商品审核
			  		$.each(data['orderGoodsMark'],function(k,v){
			  			var tit = '',
			  				remark = v['status_explain'] || '';
			  			if(k===0){
			  				tit = '商品审核：';
			  			}
			  			$('<tr class="orderGoodsMark"><td class="tit">' + tit 
			  				+ '</td><td><textarea class="txta" data-type="1" data-id="' 
			  				+ v['order_goods_id'] + '">' + remark + '</textarea></td><td class="">' 
			  				+ v['order_goods_id'] + '</td><td><a class="btn btn_green">提交</a></td></tr>').appendTo(table);
			  		});

			  		//购物车历史详情
			  		$.each(data['purchaseMark'],function(k,v){

			  			var tit = '',
			  				remark = v['purchase_mark'] || '';
			  			if(k===0){
			  				tit = '采购历史详情：';
			  			}
			  			$('<tr class="orderGoodsMark"><td class="tit">' + tit 
			  				+'</td><td><textarea class="txta" data-type="2" data-id="' 
			  				+ v['purchase_id'] + '">' + remark + '</textarea></td><td>' + v['purchase_id'] 
			  				+ '</td><td><a class="btn btn_green">提交</a></td></tr>').appendTo(table);
			  		});

			  		//库存
			  		$.each(data['stockMark'],function(k,v){

			  			var tit = '',
			  				remark = v['remark'] || '';
			  			if(k===0){
			  				tit = '库存：';
			  			}
			  			$('<tr class="orderGoodsMark"><td class="tit">' + tit 
			  				+'</td><td><textarea class="txta" data-type="3" data-id="' 
			  				+ v['stock_id'] + '">' + remark + '</textarea></td><td>' + v['stock_id'] 
			  				+ '</td><td><a class="btn btn_green">提交</a></td></tr>').appendTo(table);
			  		});

			  		var coupon_mark = data['orderMark']['reserved_3'] || '';

			  		//消费现金券
			  		if(data['orderMark'].length){
			  			$('<tr class="orderMark"><td class="tit">消费现金券：</td><td>' + 
			  			'<textarea class="txta" data-type="4" data-id="' + data['orderMark']['order_id'] + '">' + coupon_mark + '</textarea>' + 
			  			'</td><td>' + data['orderMark']['order_id'] + '</td><td><a class="btn btn_green">提交</a></td></tr>').appendTo(table);
			  		}
			  		

			  		art.dialog({
						id : 'pop',
						title : '添加备注',
						fixed:true,
						lock : true,
						opacity:0.5,
					  	background : '#000',
					  	top:150,
					  	content:dom[0],
					  	close : function(){
					  		if(isEdit.length){
					  			app.loading.open('正在请求数据...');
					  			window.location.reload();
					  		}
					 	}
				 	});

				  	//高亮显示当前页面编辑的备注
				  	$('.table_list').find('.txta[data-id="' + thisId + '"]').eq(0).focus();

				  	$('.table_list .btn_green').each(function(){
				  		var _this = $(this);
				  		_this.click(function(){
				  			var txta = _this.parent().siblings().find('.txta');
					  		if(confirm('确定要修改过吗？')){
						 		remark_action(txta.attr('data-type'),txta.attr('data-id'),txta.val(),isEdit);
						 	}
				  			return false;
				  		})
				  		
				  	});


					/*$('.table_list .txta').on('change',function(){
					 	if(confirm('确定要修改过吗？')){
					 		remark_action($(this).attr('data-type'),$(this).attr('data-id'),$(this).val(),isEdit);
					 	}
						return false;
					});*/
			  	}
			}
		});

	});
}



//弹窗修改备注
function remark_action(type,id,explain,isEdit){

	var url='',
		data = [];
		
	//订单审核 - 备注
	if(type==='0'){
		url = '/admin/update_order_extra_info/';
		data = {
			_xsrf : getCookie('_xsrf'),
			order_id : id,
			explain : explain
		}
	}
	//商品审核
	if(type==='1'){
		url = '/admin/update_order_gooods_extra_info/';
		data = {
			_xsrf : getCookie('_xsrf'),
			order_goods_id : id,
			status_explain : explain
		}
	}


	//采购历史详情 - 备注
	if(type==='2'){
		url = '/admin/update_purchase_extra_info/';
		data = {
			_xsrf : getCookie('_xsrf'),
			purchase_id : id,
			purchase_mark : explain
		}
	}

	//库存 - 备注
	if(type==='3'){
		url = '/admin/stockmanagement/remark/';
		data = {
			_xsrf : getCookie('_xsrf'),
			id : id, 
			remark : explain
		}
	}


	//消费消费券 - 备注
	if(type==='4'){
		url = '/admin/update_order_extra_info/';
		data = {
			_xsrf : getCookie('_xsrf'),
			order_id : id,
			coupon_explain : explain
		}
	}

	app.loading.open("正在提交...");

	$.ajax({
		url: url,
		type : "post",
		data : data,
		success: function(data){
		  app.loading.close();
		  if(!data.status==0){
		  	showMsg('修改失败! 错误代码：' + data.msg,3);
		  }else{
		  	if(!isEdit.length) isEdit[0] = 'ture';
		  	showMsg('操作成功！',1);
		  }
		}
	});
}
