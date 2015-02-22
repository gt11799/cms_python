function postToQQWb(url){
	var _t = '给大家推荐“小荷特卖”。高级的品牌，划算的价格。超低价，衣服正品，很漂亮，快试试吧 ';
	var _url = url;
	var _appkey = "";//你从腾讯获得的appkey
	var _pic = 'http://xiaoher.com/static/images/share_xiaoherlogo.png?20140519';//（列如：var _pic='图片url1|图片url2|图片url3....）
	var _site = 'm.xiaoher.com';//你的网站地址
	var _u = 'http://v.t.qq.com/share/share.php?title='+_t+'&url='+_url+'&appkey='+_appkey+'&site='+_site+'&pic='+_pic;
	window.location.href=_u;
	// window.open( _u,'转播到腾讯微博', 'width=700, height=680, top=0, left=0, toolbar=no, menubar=no, scrollbars=no, location=yes, resizable=no, status=no' );
}

function postToQQSpace(url){
	var url = url;
	var showcount = '0';//是否显示分享总数,显示：'1'，不显示：'0' 
	var desc = '给大家推荐“小荷特卖”。高级的品牌，划算的价格。超低价，衣服正品，很漂亮，快试试吧 ';//默认分享理由(可选)
	var summary = '';//分享摘要(可选)
	var title = '小荷特卖正品保证';//分享标题(可选)
	var site = '小荷';//分享来源(可选)
	var pics = 'http://m.xiaoher.com/static/images/share_xiaoherlogo.png?20140519';//分享图片的路径(可选,多图片用|隔开)
	var _url = 'http://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?url='+url+'&showcount='+showcount+'&desc='+desc+'&summary='+summary+'&title='+title+'&site='+site+'&pics='+pics;
	window.location.href=_url;
	// window.open( _url,'转播到QQ空间', 'width=700, height=680, top=0, left=0, toolbar=no, menubar=no, scrollbars=no, location=yes, resizable=no, status=no' );
}


function postToSinaWb(url){
	var appkey = '';//申请的APPkey
	var title = '给大家推荐“小荷特卖”。高级的品牌，划算的价格。超低价，衣服正品，很漂亮，快试试吧 '; //默认分享理由(可选)
	var pic = 'http://xiaoher.com/static/images/share_xiaoherlogo.png?20140519'; //分享图片的路径(可选,多图片用|隔开)
	var ralateUid = '';  //关联微博号
	urlsina = 'http://service.weibo.com/share/share.php?url='+url+'&appkey='+appkey+'&title='+title+'&pic='+pic+'&ralateUid='+ralateUid+'&language='
	window.location.href=urlsina;
	// window.open( urlsina,'转播到Sina微博', 'width=700, height=680, top=0, left=0, toolbar=no, menubar=no, scrollbars=no, location=yes, resizable=no, status=no' );
}
