
function XHFocus(args){

		
		var _args = $.extend({ 
			action : 'mouseover', 
			time : 5000,
			speed : 800,
			autoPlay : true,
			callback : null
		}, ( args || {} ) );

		var _self = this,
			_dom = _args.selector instanceof $ ? _args.selector : $( _args.selector ),
			index = 0,
			timer = false,
			listDom = $(_dom.find('ul'));
			menuDom = $('<div class="menu"></div>').appendTo(_dom),
			list = listDom.find('li');
		
		this.build = function(){
			$.each(list,function(k,v){

				/*
				var _this = $(this),
				imgUrl = _this.find('img').attr('src');
				_this.find('a').css({
					background : 'url(' + imgUrl + ') no-repeat center center'
				});
				_this.find('img').remove();

				if(k==0){
					_self.setHeigth(imgUrl);
				}*/
				
				var span = $('<span>');
				if(k==0) span.addClass('on');
				span.on(_args.action, function(){
					if(!list.is(':animated')){
						span.addClass('on').siblings().removeClass('on');
						index = k;
						_self.play();
					}
				});
				span.appendTo(menuDom);
			});
		
			_dom.addClass('xh_focus').hover(function(){
				timer && clearInterval(timer);
			},function(){
				_self.autoPlay();
			});
		}

		this.setHeigth = function(imgUrl){
			var image = new Image();
			image.onload = function(){
				_dom.height(image.height);
				_dom.find('li a').height(image.height);
			}
			image.src = imgUrl;
		}

		this.play = function(){
			list.stop(true).eq(index).fadeIn(_args.speed).siblings().fadeOut(_args.speed);
			menuDom.find('span').eq(index).addClass('on').siblings().removeClass('on');
		}

		this.autoPlay = function(){
			timer = setInterval(function(){
				index ++;
				if(index >=list.length) index = 0;
				_self.play();
			},_args.time )
		}

		this.init = function(){

			if(list.length<2){
				return false;
			}
			
			this.build();
			_args.autoPlay && this.autoPlay();
		}

		this.init();

	}