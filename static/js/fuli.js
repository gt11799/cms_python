function loadJS(filename,css,dsrc,dno,dactid,login,dlen){
	 var _script=document.createElement('script');
		_script.setAttribute("type","text/javascript");
		_script.setAttribute("src", filename);
		_script.setAttribute("class", css || "");
		_script.setAttribute("data-src", dsrc || "");
		_script.setAttribute("data-no", dno || "");
		_script.setAttribute("data-actid", dactid || "");
		_script.setAttribute("data-login", login || "");
		_script.setAttribute("data-len", dlen || "");
	document.getElementsByTagName("head")[0].appendChild(_script);
}
$(function(){
	$.getJSON("/show_fuli/",function(data){
		var fuli = data.fuli,
			no = $(".J_fuli").data("no") || "",
			login = $(".J_fuli").data("login") || 0,
			awardCoins = data.award_coins || 0;//判断安卓送N荷币
		//if(awardCoins!=0){
			//showfla();
			//$("body").append('<div class="download" style="height:22px;"><span style="color:#f00">安装赠送的'+awardCoins+'荷币已赠送</span><a href="javascript:;" class="close J_colse_d" style="top:4px">X</a></div>');
		//}
		if(fuli!=false){
			var len = fuli.length,
				img = [],
				activityId = [],
				imgList = "";

			for(var i=0;i<len;i++){
				img.push(fuli[i].image);
				activityId.push(fuli[i].activity_id);
				imgList += '<a href="/fuli/'+fuli[i].activity_id+'" class="J_new_user"><img src="'+fuli[i].image+'"></a>'
			}
			// if(data.verify==-2){
			// 	loadJS("/static/js/md5.js");
			// 	loadJS("/static/js/new_user.js?v=20140927","J_new_user_js",img.toString(),"",activityId.toString(),login,len);
			// }else if(data.verify==-1){
			// 	loadJS("/static/js/md5.js");
			// 	loadJS("/static/js/new_user.js?v=20140927","J_new_user_js",img.toString(),no,activityId.toString(),login,len);
			// }else{
				$("#slider").append(imgList);
				if($("#slider").find("a").length>1){
					$("#slider").slider( { autoPlay:true , viewNum:1});
				}
			// }
		}
	})

	$("body").on("click",".J_colse_d",function(){
		$(".download").remove();
	})
	
})
