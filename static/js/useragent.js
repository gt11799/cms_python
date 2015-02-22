var cookie_d = $.cookie("download_tips_2014102516"),
	cookie_favorite =  $.cookie("add_favorite_2014102516")
	atWeixin = isWeixin();

if(/AppleWebKit.*Mobile/i.test(navigator.userAgent) || (/MIDP|SymbianOS|NOKIA|SAMSUNG|LG|NEC|TCL|Alcatel|BIRD|DBTEL|Dopod|PHILIPS|HAIER|LENOVO|MOT-|Nokia|SonyEricsson|SIE-|Amoi|ZTE/.test(navigator.userAgent))){
	if(window.location.href.indexOf("?mobile")<0){
		try{
			if(/Android/i.test(navigator.userAgent)){
				if(!cookie_d){
					if(atWeixin){
						$("body").prepend('<div class="download"><div class="J_d_app"><a href="http://a.app.qq.com/o/simple.jsp?pkgname=com.xiaoher.app"><span class="xiaoher_icon"></span><p class="t">小荷特卖</p><p>优质精品，限时特卖APP</p></a><a href="http://www.xiaoher.com/app_download/?app_type=android" class="btn_d">下载</a><a href="javascript:;" class="close J_colse_d"></a></div></div>');
					}else{
						$("body").prepend('<div class="download"><div class="J_d_app"><a href="http://www.xiaoher.com/app_download/?app_type=android"><span class="xiaoher_icon"></span><p class="t">小荷特卖</p><p>优质精品，限时特卖APP</p></a><a href="http://www.xiaoher.com/app_download/?app_type=android" class="btn_d">下载</a><a href="javascript:;" class="close J_colse_d"></a></div></div>');
					}
				}
			}else if(/iPhone|iPod|iPad/i.test(navigator.userAgent)){
				if(!cookie_d){
					$("body").prepend('<div class="download"><div class="J_d_app"><a href="http://www.xiaoher.com/app_download/?app_type=ios"><span class="xiaoher_icon"></span><p class="t">小荷特卖</p><p>优质精品，限时特卖APP</p></a><a href="http://www.xiaoher.com/app_download/?app_type=ios" class="btn_d">下载</a><a href="javascript:;" class="close J_colse_d"></a></div></div>');
				}else{
					if(!cookie_favorite && $(".index").length){
						$("body").prepend('<div class="ios_add_favorite"><span class="ui-add2desktop-close J_add_close"><b></b></span><img src="/static/images/iphone_icon_144x144.png" width="60"/>先点击<span class="adddesktop_icon"></span>，<br/>再点添加到“书签”<span class="ios_add_arrow"></span></div>');
					}
				}
			}
		}catch(e){}
	}
}


$("body").on("click",".J_colse_d",function(){
	$.cookie("download_tips_2014102516", "hidden",{expires:1,path: '/'});
	$(".download").remove();
	$("body").css({"paddingTop":0})
})

$("body").on("click",".J_add_close",function(){
	$.cookie("add_favorite_2014102516", "hidden",{expires:60,path: '/'});
	$(".ios_add_favorite").remove();
}) 
