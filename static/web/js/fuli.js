$(function(){
	function loadJS(filename,css,dsrc,dlen,dno,dactid){
		 var _script=document.createElement('script');
			_script.setAttribute("type","text/javascript");
			_script.setAttribute("src", filename);
			_script.setAttribute("class", css || "");
			_script.setAttribute("data-src", dsrc || "");
			_script.setAttribute("data-len", dlen || "");
			_script.setAttribute("data-no", dno || "");
			_script.setAttribute("data-actid", dactid || "");
		document.getElementsByTagName("head")[0].appendChild(_script);
	}

	$.getJSON("/show_fuli/",function(data){
		var fuli = data.fuli,
			no = $(".J_fuli").data("no") || "",
			verify = data.verify;
		if(fuli!=false){
			var len = fuli.length,
				img = [],
				activityId = [],
				imgList = "";
			for(var i=0;i<len;i++){
				img.push(fuli[i].image);
				activityId.push(fuli[i].activity_id);
				var image = new Image(),
					imgHeight = 0;
					image.src = fuli[i].image;
				imgList += '<li><a href="/fuli/'+fuli[i].activity_id+'" class="J_new_user" style="background:url('+fuli[i].image+') no-repeat center center; display:block; width:100%; " target="_blank"></a></li>'
				image.onload=function(){
					 imgHeight = image.height;
					 $(".J_new_user").css({"height":imgHeight});

					 //加载下雪效果
					var ie = getInternetExplorerVersion();
					if(ie>10 || ie<0 && $("#slider").length){
					 	startSnow (); //初始化下雪效果
					}
				}
			}
			//alert(len)
			// if(verify==-2){  //未注册状态
			// 	loadJS("/static/js/md5.js");
			// 	loadJS("/static/web/js/new_user.js?v=2014110619","J_new_user_js",img.toString(),len.toString(),"",activityId.toString());
			// }else if(verify==-1){ //注册未验证手机状态
			// 	loadJS("/static/js/md5.js");
			// 	loadJS("/static/web/js/new_user.js?v=2014110619","J_new_user_js",img.toString(),len.toString(),no,activityId.toString());
			// }else{//已注册已验证手机状态
				$("#slider").find(".bd ul").append(imgList);
				$("#slider").addClass("show");
				if(len>1){
					loadJS("/static/web/js/jquery.SuperSlide.2.1.1.js");
					jQuery("#slider").slide({mainCell:".bd ul",titCell:".hd ul",effect:"leftLoop",autoPlay:true, interTime:6000,autoPage:"<li></li>"}).addClass("show");
				}
			// }
		}
	})
})
