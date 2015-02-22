
initPage();

function initPage(){
	$('.txt_brand_name').val(getQueryString('brand_name'));
	//列出品牌
	$.ajax({
	    url: '/admin/get_today_style_brand/',
	    type : "get",
	    success: function(data){
	      app.loading.close();
	      if(data['data'].length){
	        $.each(data['data'],function(k,v){
	            var option = $('<option value="' + v + '">' + v + '</option>');
	            $('#list').append(option);
	        });
	      }
	    }
	});


	//txt验证
	$('.table').on('blur','.txt',function(){
		var _this = $(this);
		if($.trim(_this.val())===''){
			_this.addClass('error');
		}else{
			_this.is('.error')&&_this.removeClass('error');
		}
	});
}

//获取数据
function getData(type){
	var items = $('.table').find('tr').not('.tbHead'),
		data = {"list" : []},
		isError = false;

	if($('.table .errow').length || !items.length){
		return false;
	}

	if(type=='add'){
		$.each(items,function(k,v){
			var _this = $(this),
			code = $.trim(_this.find('.txt_code').val()),
			color= $.trim(_this.find('.txt_color').val()),
			url  = $.trim(_this.find('.txt_url').val()),
			_id  = _this.attr('_id') || '',
			isNew = _this.find('.is_new').text();

			if(!code){
				_this.find('.txt_code').addClass('error');
				isError = true;
				return false;
			}
			if(!color){
				_this.find('.txt_color').addClass('error');
				isError = true;
				return false;
			}
			if(!url){
				_this.find('.txt_url').addClass('error');
				isError = true;
				return false;
			}
			data['list'].push({
				code : code,
				color : color,
				url : url,
				_id :_id,
				isNew : isNew  
			});
		});
	}else{
		$.each(items,function(k,v){
			var _this = $(this),
			_id = _this.attr('_id'),
			stock = _this.find('.txt_stock').val();

			if(!stock){
				_this.find('.txt_stock').addClass('error');
				isError = true;
				return false;
			}
			data['list'].push({
				_id : _id,
				stock : stock,
				is_stock: 1
			});
		});
	}

	if(isError){
		return false;
	}else{
		return data;
	}
}


//品牌名称检测
function check_brand_name(){
	var name = $.trim($('.txt_brand_name').val());
	if(name===''){
		showMsg('请输入品牌！',3);
		return false;
	}
	/*
	if(!$('#list option[value="' + name + '"]').length){
		showMsg('没有此品牌!',3);
		return false;
	}*/
	return name;
}

$('.txt_brand_name').on('change',function(){
	if(!check_brand_name()) $(this).val('');
	return false;
});