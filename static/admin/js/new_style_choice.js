
$(function(){

	$('#btn_online').on('click',function(){
		action(1);
		return false;
	});


	//下线
	$('#btn_offline').on('click',function(){
		action(2);
		return false;
	});

	//批量下载
	$("#btn_img_batch_d").on("click",function(){
		batch_download();
	});

	if($(".J_scroll_fix").length){
		var scrollfix = $(".J_scroll_fix");
			scrollfixTop = scrollfix.offset().top,
			scrollfixHeigth = scrollfix.outerHeight(),
			scrollfixWidth = scrollfix.outerWidth();

		$(window).scroll(function(){
			if($(window).scrollTop()>(scrollfixTop)){
				scrollfix.css({"position":"fixed","top":"0","zIndex":999});
			}else{
				scrollfix.css({"position":"static","marginLeft":0});
			}
		});
	}

	//修改商品属性体积
	function modifyVolume( d ){

		var data = {
			goods_id : d.goods_id
		}
		var volume = $.trim(d['volume'][0]);
		if(volume==='大'){
			data.vol_is_big = 1;
		}else if(volume==='小'){
			data.vol_is_big = 0;
		}else{
			var v = d['volume'][0].split('*');
			data.vol_length = v[0];
			data.vol_width = v[1];
			data.vol_height = v[2].split('cm')[0];
		}

		$.ajax({
			type:"post",
			url:"/admin/company/goods/volume_update/",
			data:data,
			success:function(data){
				if(data.status!==0){
					showMsg(data.msg || "后台报错，体积同步失败！" , 3);
				}
			},
			error:function(){
				showMsg("载入出错啦，请刷新页面试试",2);
			}
		})
	}


	//修改尺码
	$('#img_list .size').on('click',function(){
	    var _this = $(this),
	    goods_id =  _this.parents('li').find('input[type=hidden]').val();
	   var d =  art.dialog({
	        title : '修改尺码',
	        content : '<iframe id="size_box" name="size_box" src="/company/size/add?name=' + goods_id + '&type=1" style="border:none; width:1200px; height:350px;"></iframe>',
	        ok : function(){

	        	var sizeData = window.frames["size_box"].getSizeData();
	            $.post("/admin/company/goods/size_update/",{
	                goods_id : goods_id,
	                size : JSON.stringify(sizeData)
	            },function(data){
	                app.loading.close();
	                if(data.status==0){	
	                	
	                	if(sizeData['size'][0]['volume'].length){
	                		modifyVolume({
		                		goods_id : goods_id,
		                		volume : sizeData['size'][0]['volume']
		                	});
	                	}else{
	                		modifyVolume({
		                		goods_id : goods_id,
		                		volume : ['小']
		                	});
	                	}
	                    showMsg("操作成功！",1);
	                    d.close();
	                }else{
	                    showMsg(data.msg || '亲，后台报错了~',3);
	                }
	            });
	            return false;
	        },
	        cancel : function(){

	        },
	        okVal : '保存',
	        button: [
	            {
	                name: '完成',
	                callback: function () {
	                    setDone('size_make',goods_id);
	                    return false;
	                },
	                focus: true
	            }
	        ]
	    });
	    return false;
	});

	//修改材质
	$('#img_list .caizhi').on('click',function(){

	    $('.fabric').find('')
	    var _this = $(this),
	    parent =  _this.parents('li');
	    goods_id = parent.find('input[type=hidden]').val(),
	    fabric = parent.attr('data-fabric'),
	    material_label = parent.attr('data-material-label');

	    $('.fabric input[name=fabric][value=' + material_label +']').attr('checked','checked');
	    $('.fabric #fabric').val(fabric);

	    var pop = art.dialog({
	        title : '修改材质',
	        content : $('.fabric')[0],
	        ok : function(){
	            $.post("/admin/company/goods/fabric_update/?_xsrf="+getCookie("_xsrf"),{
	                goods_id : goods_id,
	                material_label:$("input[name=fabric]:checked").val(),
	                fabric:$("#fabric").val(),
	            },function(data){
	                app.loading.close();
	                if(data.status==0){
	                    showMsg("操作成功！",1);
	                    pop.close();
	                    window.location.reload();
	                }else{
	                    showMsg(data.msg,3);
	                }
	            });
	            return false;
	        },
	        okVal : '保存',
	        cancel : function(){
	        },
	        button: [
	            {
	                name: '完成',
	                callback: function () {
	                    setDone('fabric_make',goods_id);
	                    return false;
	                },
	                focus: true
	            }
	        ]
	    });
	    return false;
	});

	//批量修改 完成
	$('.do_area .btn_done').on('click',function(){
	    setDone( $(this).attr('data-label'));
	    return false;
	});


	//修改来源
	$('.img_list li .edit_source').on('click',function(){

		//var _this = $(this);

		var _this = $(this);
			sub_url = _this.attr('data-sub-source').split(','),//将字符串按","划分成一个数组
			sub_tpl = '<br /><p style="font-size:14px;">宝贝辅URL：<input style="width:300px;" class="txt J_sub_source" value="" /></p>';
		
		if(sub_url.length){
			sub_tpl = '';
			$.each(sub_url,function(k,v){//遍历数组sub_url，将值依次赋给p标签的value
				sub_tpl+= '<br /><p style="font-size:14px;">宝贝辅URL：<input style="width:300px;" class="txt J_sub_source" value="' + v + '" /></p>';
			});
		}

		var pop = art.dialog({
			title : '修改来源',

			content : '<p style="font-size:14px;">宝贝主URL：<input style="width:300px;" id="E_source" class="txt" value="' + _this.attr('data-source') +  '" /></p>' + sub_tpl,
			ok : function(){	

				if(!$('#E_source').val()){
					showMsg('亲，请输入商品来源!',3);
					return false;
				}

				var sub_url = [];
				$.each($('.J_sub_source'),function(){//遍历获取到的class="J_sub_source"的input标签
					if($(this).val()){
						sub_url.push($(this).val());//将input标签的值依次赋给数组sub_url
					}
				});

				app.loading.open("正在提交...");
			    $.ajax({
			        url :'/admin/company/goods/set_goods_source/?_xsrf='+ getCookie('_xsrf'),
			        type : "post",
			        data :{
			        	goods_id : _this.parents('li').find('input[type=hidden]').val(),
			        	url : $('#E_source').val(),
			        	sub_url :sub_url.join(',')//将数组转化成以","分隔的字符串
			        },
			        success: function(data){
			            app.loading.close();
			            if(data.status==0){
			                showMsg('操作成功！');
			                pop.close();
			               window.location.reload();
			            }else{
			                showMsg(data.msg,3);
			            }
			        }
			    });
				return false;
			}
		});
		return false;
	});

	
	//修改宝贝URL
	$('.img_list li .fuurl').on('click',function(){

		var _this = $(this);
		var pop = art.dialog({
			title : '修改URL',
			content : '<p style="font-size:14px;">买手名称：&nbsp;&nbsp;&nbsp;<input id="buyer" class="txt" style="width:300px;" value="' + $('.company_name').text() + '" /></p>' + 
				'<br /><p style="font-size:14px;">宝贝辅URL：<input class="txt" style="width:300px;" id="sub_url" /></p>',
			ok : function(){

				 if(!$('#buyer').val()){
	                showMsg('亲，请输入买手名称!',3);
	                return false;
	            }
	            if(!$('#sub_url').val()){
	                showMsg('亲，请输入URL!',3);
	                return false;
	            }
	            app.loading.open("正在提交...");
	            $.post("/admin/company/goods/modify_task/?_xsrf="+getCookie("_xsrf"),{
	                brand_id: getQueryString('activity_id'),
	                sub_url : $('#sub_url').val(),
	                buyer : $('#buyer').val(),
	                goods_id : _this.parents('li').find('input[type=hidden]').val()
	            },function(data){
	                app.loading.close();
	                if(data.status==0){
	                	pop.close();
	                    showMsg("操作成功！",1);
	                }else{
	                    showMsg(data.msg,3);
	                }
	            });
	            return false;
			}
		});
		return false;
	})


	
	//修改价格、库存
	$('.price_area .txt,.size_area .txt').on('change',function(){
	    var _this = $(this),
	    	good_id = _this.parents('li').find('input[type=hidden]').val();

	    if(!_this.attr('disabled')){
	    	changeGoodInfo(_this, good_id, _this.attr('data-type'));
	    }

	}).on('click',function(e){
	    e.stopPropagation();
	});


	//批量设置折扣
	$('#discount').change(function(){

	    var _check = $(this);
	    if(_check.val()==='0') return false;
	    var checkList = $('.img_list .isChecked');

	    if(!checkList.length){
	        showMsg('至少选择一条数据！',3);
	        _check.val('0');
	        return false;
	    }

	    $.each(checkList,function(){
	        var _this = $(this);
	        price = Math.ceil(_this.find('.J_market_price').val()*_check.val());
	        _this.find('.J_price').val(price);
	        setTimeout(function(){
	            _this.find('.J_price').change();
	        },200);
	    });
	});

	//批量库存
	$('#btn_stock').on('click',function(){

	    if(!$('#txt_stock').val()) return false;
	    var checkList = $('.img_list .isChecked');
	     if(!checkList.length){
	        showMsg('至少选择一条数据！',3);
	        return false;
	    }
	    $.each(checkList,function(){
	        var _this = $(this);
	         _this.find('.size_area .txt[data-type=stock]').val($('#txt_stock').val());
	        setTimeout(function(){
	            _this.find('.size_area .txt').change();
	        },200);
	    });
	    return false;
	});


	//使用建议价格
	$('#J_suggest').on('click',function(){
		suggestAndConfirmPrice('suggest');
		return false;
		 
	});

	//确认小荷价
	$('#J_confirm').on('click',function(){
		suggestAndConfirmPrice('confirm');
		return false;
	});

});




//获取选中的ID
function getSelectItem(){

	var selectItems = $('.activity_wrap .img_list>li.isChecked'),
		data = {
			ids: [],
			isDone : false,
			brand_ids:[],
			items : selectItems
		}
	$.each(selectItems,function(){
		var _this = $(this);
		if(_this.find('.btn_finish').length && !data.isDone){
			data.isDone =true;
		}
		data.ids.push(_this.find('input[type=hidden]').val());
		data.brand_ids.push(_this.find('input[type=hidden]').attr("data-brand-id"));
	});
	return data;
}

//设置完成 -- 批量/单个
/**
* @label 类型
* 
*/
function setDone(label, id, unfinish){

    var data = {},
        ids = getSelectItem()['ids'];

    if(!id && !ids.length){
        showMsg('至少选择一个商品！',3);
        return false;
    }

    if(label=='size_make'){
        data.size_make = 'done';
    }
    if(label=='fabric_make'){
        data.fabric_make = 'done';
    }
    if(label=='image_make'){
    	data.image_make = 'done';
    	if(unfinish) data.image_make = '';
    }
    
    if(id){
        data.goods_id = id;
    }else{
        data.goods_id = ids.join(',');
    }

    //图片裁切
	if(label=='image_make'){
		imageMake(data);
		return false;
	}

    app.loading.open("正在提交...");
    $.ajax({
        url :'/admin/company/goods/make_attr_done/?_xsrf='+ getCookie('_xsrf'),
        type : "post",
        data :data,
        success: function(data){
            app.loading.close();
            if(data.status==0){
                showMsg('操作成功！');
                setTimeout(function(){
                	window.location.reload();
                },500);
            }else{
                showMsg(data.msg,3);
            }
        }
    });
}


function imageMake(data){
	$.ajax({
        url :'/admin/company/goods/make_image_done/',
        type : "post",
        data :data,
        success: function(data){
            app.loading.close();
            if(data.status==0){
                showMsg('操作成功！');
                setTimeout(function(){
                	window.location.reload();
                },500);
            }else{
            	showMsg('亲，你没有权限哦~',3);
            }
        }
    });
}

/**
* 商品上下线
* @type 1--上线；2--下线
*/
function action(type){

	var activity_id = getQueryString('id'),
		data = getSelectItem(),
		post_data = {
			activity_id : activity_id,
			goods_id : data['ids'].join(',')
		};

	if(!data['ids'].length){
		showMsg('至少选择一个商品！',3);
		return false;
	}

	/*
	if(type==1 && data['items'].find('.is_unverify').length){
		showMsg('请确认小荷价！',3);
		return false;
	}*/

	if(type==1 && data['isDone']){
		showMsg('未完成的商品，不能上线',3);
		return false;
	}

	if(type==1){
		post_data.action = 'push';
	}

	if(type==2){
		post_data.action = 'pull';
		post_data.activity_id = $('#activity_input').val();
	}

	app.loading.open("正在提交...");
	$.ajax({
		url :'/admin/company/push_and_pull_goods/?_xsrf='+ getCookie('_xsrf'),
		type : "post",
		data : post_data,
		success: function(data){
			app.loading.close();
			if(data.status==0){
				showMsg('操作成功！');
				setTimeout(function(){
					window.location.reload();
				},1000);
				
			}else{
				showMsg(data.msg,3);
			}
		}
	});

}

//修改商品相关信息
function changeGoodInfo(dom,good_id,type){
    var _data = {
        goods_id : good_id
    },

    //修改商品价格
    postUrl = '/admin/company/goods/set_goods_attr/';

    //库存
    if(type=='stock'){
        _data.stock = dom.val();
        _data.original_stock = dom.attr('prevval'),
        _data.size = dom.attr('data-size');
        postUrl = '/admin/company/goods/set_price_and_stock/';
    } 
    
    //小荷价
    if(type=='price'){
        _data.price = dom.val();
    }

    //吊牌价
    if(type=='market_price'){
        _data.market_price = dom.val();
    }

    //采购价
    if(type=='cost_price'){
    	if(confirm('你确认要修改采购价吗？这个修改会被记录。')){
    		_data.cost_price = dom.val();
    	}else{
    		dom.val(dom.attr('prevval'));
    		return false;
    	}
    }


    //如果不是特价活动，小荷价为0，出现警告图片
    var J_id = $('#J_from_product').attr('data-activity_id');
    if(dom.hasClass('J_price')){
    	if(J_id != 1267 || J_id != 5200){
		    if(_data.price > 0){
		    	dom.parents('.item').find('.J_warn').hide();
		    }else{
		    	dom.parents('.item').find('.J_warn').show();
		    }
		}
    }

    app.loading.open("正在提交...");

    $.ajax({
        url: postUrl,
        type : "post",
        data : _data,
        success: function(data){
            app.loading.close();
            if(data.status==0){
            	showMsg('操作成功！');
                if(type=='stock'){
                    dom.attr('prevval', _data.stock);
                }

                if(type=='price'){
                    dom.attr('prevval', _data.price);
                    dom.addClass('is_unverify'); //设置高亮
                }
                
                if(type=='market_price'){
                    dom.attr('prevval', _data.market_price);
                }

                if(type=='cost_price'){
                    dom.attr('prevval', _data.cost_price);
                    dom.parents('.item').find('.J_mproposal_price').val(data.proposal_price);
                }

            }else{
                dom.val(dom.attr('prevval'))
                showMsg(data.msg || '亲，后台报错了~',3);
            }
        }
    });
}


//使用建议价格，确认小荷价
function suggestAndConfirmPrice(type){

	var url = '/admin/company/goods/use_proposal_price/',
	selectItems = getSelectItem(),
	ids = getSelectItem()['ids'];
	
	if(!ids.length){
		showMsg('至少选择一个商品！',3);
		return false;
	}

	if(type=='confirm' && ids.length>1){
		showMsg('每次只能确认一个商品！',3);
		return false;
	}

	var _data = {
		goods_id :ids.join(',')
	}

	if(type=='confirm'){
		url = '/admin/company/goods/make_attr_done/';
		_data.price_verify = 1;
	}

	app.loading.open("正在提交...");

	$.post( url , _data ,function(data){
		app.loading.close();
		if(data.status==0){

			showMsg("操作成功！");
			if(type==='confirm'){
				selectItems['items'].removeClass('isChecked').find('.is_unverify').removeClass('is_unverify');
			}

			if(type==='suggest'){
				setTimeout(function(){
					window.location.reload();
				},1000)
			}

		}else{
			showMsg(data.msg || "修改失败!",3);
		}
	});

}


//批量下载图片
function batch_download(id){
	var good_ids = getSelectItem()['ids'] || id,
		clipboardVal = "";
	if(good_ids.length<1){
		showMsg("请至少选择一个",2)
		return;
	}
	app.loading.open("正在生成...");
	for(var i=0; i<good_ids.length; i++){
		var g_id = good_ids[i];
		$.ajax({
			url: "/company/get_goods_image/?goods_id=" + g_id,
			async:false,
			success: function(data){
				var img_urls = '';
				if(data.status==0){
					var imgs = data['goods']['image'];
					for(var j=0;j<imgs.length;j++){
						img_urls = img_urls.concat(imgs[j]+'?attname='+data['goods']['_id']+'.jpg', '\n');
					};
				};
				clipboardVal += img_urls;
				if(i==(good_ids.length-1)){
					var listDialog = new artDialog({
						title:"生成批量下载图片地址",
						content:'<textarea style="width:600px; height:300px" id="fz_text">'+clipboardVal+'</textarea>'
					})
					app.loading.close();
				}
			},
			error:function(){
				alert("出错了")
			}
		});
	};
	return clipboardVal;
}
