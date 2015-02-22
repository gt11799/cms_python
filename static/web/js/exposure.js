
(function($){

	function removeCookie(sKey, sPath, sDomain){
		if (!sKey) { return false; }
    	document.cookie = encodeURIComponent(sKey) + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT" + ( sDomain ? "; domain=" + sDomain : "") + ( sPath ? "; path=" + sPath : "");
    	return true;
	}


	function Exposure(args){
		
		var _args = $.extend({ 
			isInit : true   
		}, ( args || {} ) );

		var _self    = this,
			epuType  = 'goods',
			epuItems = '',
			cacheIds = [], 
			location = window.location.href,
			userId   = null;

		//如果是活动列表
		var cname = $('body').attr('class') || '';
		if(/index/.test(cname)){
			epuType = 'activities';
			if(/index_/.test(cname)){ //v2 v3 版本
				epuItems = $('.i_list li:has(>a)');
			}else{
				epuItems = $('.itemStyle:has(>a)');
			}
		}

		//商品列表
		if(location.indexOf('show')!=-1 || location.indexOf('search_category')!=-1 || location.indexOf('fuli')!=-1 || location.indexOf('/hs')!=-1){
			epuItems = $('.goodsList ul>li:has(>a)');
		}	

		var getEpuCookie = function(){
			return $.parseJSON($.cookie('exposure'));
		}

		var setEpuCookie = function( epu ){
			//epu.user_id = userId;
			$.cookie('exposure', JSON.stringify(epu) ,{
		    	expires : 10,
		    	path : '/'
		    
		    });
		}

		var getInitEpu = function(){

			return {
	   			time : new Date(),
	   			user_id : userId ,
	   			list : {
	   				activities : [],
	   				goods : []
	   			}
	   		}
		}

		var addEpuItem = function(obj, args){
			if(args.epuType=='activities'){
				if(args.type =='s'){
					obj.push({
			            aid : args.id,
			            s   : args.num
		        	});
				}
				if(args.type =='c'){
					obj.push({
			            aid : args.id,
			            c   : args.num
		        	});
				}
	   		}

	   		if(args.epuType=='goods'){
	   			if(args.type == 's'){
	   				obj.push({
			            gid : args.id,
			            aid : args.aid,
			            s   : args.num
		        	});
	   			}else{
	   				obj.push({
			            gid : args.id,
			            aid : args.aid,
			            c   : args.num
		        	});
	   			}
	   		}
		}

		var saveData = function(args ,callback){
			var epu =  getEpuCookie() || getInitEpu();
			var type =  args.epuType || epuType;
			
		   	if(type=='activities'){
	   			var activity = epu.list['activities'];
	   			if(activity.length){
	   				$.each(activity, function(k,v){
		   				if( v['aid'] == args.id ){
		   					v[args.type] = v[args.type] ? v[args.type] + 1 : 1;
		   					return false;
		   				}
		   				if(k===activity.length-1){
		   					addEpuItem(activity, {
		   						id : args.id, 
		   						num : 1,
		   						type : args.type,
		   						epuType : type
		   					});
		   				}
		   			});
	   			}else{
					addEpuItem(activity, {
						id : args.id, 
						num : 1,
						type : args.type,
		   				epuType : type
					});
	   			}
	   			epu.list['activities'] = activity;
	   			//console.log(activity);
	   		}

	   		if(type =='goods'){
	   			var goods = epu.list['goods'];
	   			if(goods.length){
	   				$.each( goods, function(k,v){
		   				if( v['gid'] == args.id ){
		   					v[args.type] = v[args.type] ? v[args.type] + 1 : 1;
		   					return false;
		   				}
		   				if(k===goods.length-1){
		   					addEpuItem(goods, {
		   						id : args.id, 
		   						num : 1, 
		   						aid : args.aid,
		   						type : args.type,
		   						epuType : type
		   					});
	   					}
		   			});
	   			}else{
   					addEpuItem(goods, {
   						id : args.id, 
   						num : 1, 
   						aid : args.aid,
   						type : args.type,
   						epuType : type
   					});
	   			}
	   			epu.list['goods'] = goods;
	   		}
		   	setEpuCookie(epu);
		}
	
		var getEpuId = function(urlStr){
			var ret = [];
			if(epuType=='goods'){
				ret.push(Number(urlStr.split('/')[3]));
				ret.push(Number(urlStr.split('/')[2]))
			}else{
				ret.push(Number(urlStr.split('/')[2]));
			}
			return ret;
		}
		
		var getClickEpu = function(){
			
			if(location.indexOf('/show')!=-1){
				saveData({
					type : 'c',
					id : location.match(/show\/\d+/g)[0].split('/')[1]*1,
					epuType : 'activities'
				});
			}

			if(location.indexOf('/fuli')!=-1){
				saveData({
					type : 'c',
					id : location.match(/fuli\/\d+/g)[0].split('/')[1]*1,
					epuType : 'activities'
				});
			}

			if(location.indexOf('detail')!=-1){
				saveData({
					type : 'c',
					epuType : 'goods',
					id : location.match(/\d+\/\d+/g)[0].split('/')[1]*1,
					aid : location.match(/detail\/\d+/g)[0].split('/')[1]*1
				});
			}
		}

		var checkFuliExp = function(){
			
			var isBanner = $('body #slider li').length,
				isFuli = location.indexOf('/fuli')!=-1;

			if(!isBanner && !isFuli) return false;

			var type = 's',id;
			if(isBanner){
				$.each($('#slider li a'),function(){
					var href = $(this).attr('href');
					if(href && href.match(/fuli\/\d+/g)){
						id = href.match(/fuli\/\d+/g)[0].split('/')[1]*1;
						return false;
					}
				});
			}

			if(isFuli){ 
				type='c';
				id = location.match(/fuli\/\d+/g)[0].split('/')[1]*1;
			} 
   			saveData({
	   			epuType : 'activities',
				id : id,
				type : type
			});
		}

		var checkSend = function(){

		   	if(!getEpuCookie()){
		   		setEpuCookie(getInitEpu());
		   	}

		   	checkFuliExp();
		   	data = {url:window.location.href,refer:document.referrer} //add by LYJ.

		   	$.ajax({
		   		url : '/ubsapi/',
		   		type : 'get',
		   		dataType : 'json',
		   		data: data,
		   		success : function(data){
		   			if(!data) return false;
		   		
			   		var epu =  getEpuCookie(),
			   			time = (new Date() - new Date(epu.time))/1000;
			   		userId = data.msg['user_id'];
			   		epu.user_id = data.msg['user_id'];
			   		if(data.msg['interval'] < time){
			   			epu.ch = getChannel();
						$.post("/ubsapi/", {
							data : JSON.stringify(epu)
						}, function(data){
							if($.parseJSON(data).status ===0){
								setEpuCookie(getInitEpu());
							}
						});
					}else{
						setEpuCookie(epu);
					}
		   		}
		   	});
		}

		
		function clearCookie(){
			var location = window.location.href;
			removeCookie('exposure','/show');
			removeCookie('exposure','/detail');
			removeCookie('exposure','/fuli');
			if(location.indexOf('detail')!=-1){
				var ret = location.replace(/#.*/g,'').split('/');
				removeCookie('exposure','/detail/' + ret[ret.length-2]+'/');
				removeCookie('exposure','/detail/' + ret[ret.length-2] + '/' + ret[ret.length-1]);
			}
		}

		function getChannel(){
			var referrer = document.referrer,
				channel = '';

			if(referrer.indexOf('children')!=-1){
				channel = 'children';
			}

			if(referrer.indexOf('lastday')!=-1){
				channel = 'lastday';
			}

			if(referrer.indexOf('ladys')!=-1){
				channel = 'ladys';
			}

			if(referrer.indexOf('sales')!=-1){
				channel = 'sales';
			}

			if(referrer.indexOf('search_category')!=-1){
				channel = 'search';
			}
			if(referrer.indexOf('/fuli')!=-1){
				channel = 'fuli';
			}

			if(referrer.indexOf('/show')!=-1){
				channel = 'show';
			}

			if(referrer.indexOf('/detail')!=-1){
				channel = 'detail';
			}

			if(referrer.indexOf('/hs/')!=-1){
				channel = 'hs';
			}

			if(referrer == 'http://www.xiaoher.com/'){
				channel = 'index';
			}

			return channel;
		}


		var init = function(){

			clearCookie();

			//点击曝光
			getClickEpu();

			//检查是否可发送曝光
			checkSend();
		
			$(window).on('scroll', function(){
				
				if(cacheIds.length == epuItems.length) return false;
				
				var sTop = $(this).scrollTop(),
					winH = $(window).height();
				$.each(epuItems, function(k,v){
					var _this = $(v);
					if(!_this.data('hasView')){
						var offsetTop = _this.offset().top  + _this.height();
						if( sTop + winH > offsetTop && sTop < offsetTop ){
							_this.data('hasView',true);
							var ids = getEpuId(_this.find('>a').attr('href'));
							var data = {
								id : ids[0],
								type : 's'
							}
							if(epuType == 'goods'){
								data.aid = ids[1]
							}
							saveData(data);
							cacheIds.push(ids[0]);
						}
					}
				});
			});

		}

		init();
	}

	function createExp(){
		if(!$('#slider').length){
			new Exposure();
		}else{
			var time = setInterval(function(){
				var l = $('#slider ul li').length;
				if(l){
					new Exposure();
					clearInterval(time);
				}
			},100);
		}
	}

	createExp();

	$.Exposure = Exposure;

})(jQuery);


