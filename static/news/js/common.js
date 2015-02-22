// $(function(){
// 	$('.header_nav ul li').not(":first").hover(function(){
// 		var span = $(this).children('.over');
// 		$('.nav_listbottom').css("visibility","visible");
// 	},function(){
	
// 		$('.overlayer').hide();
// 		$('.nav_listbottom').css("visibility","hidden");
// 	})




$(function(){
	$('.header_nav ul li').not(":first").hover(function(){
		var span = $(this).children('.over');
		$('.nav_listbottom').css("visibility","visible");
	},function(){
		var listbottom = document.getElementsByClassName('.nav_listbottom');
		if(listbottom.onmouseover !=null ){
			var inx1=$(this).index(this);
			$(this).eq(inx1).show();} else {
				$('.overlayer').hide();
				$('.nav_listbottom').css("visibility","hidden");
			}
		})




	// 返回顶部
	$(".J_backtop").on("click",function(){
		$("body,html").animate({"scrollTop":0},600);
	})

	/*$('.header_nav ul li').not(":first").click(function(){
		e.stopPropagation();
		$(this).addClass('on').siblings().removeClass('on');
		return false;
	})*/
});


//分页
function pageRender(args){
	var queryStr = window.location.search;
	if(!queryStr){
		queryStr = '?' + args.fieldDef;
	}else{
		queryStr = queryStr.replace(/\&page=\d+/g,'');
	}
	//有些参数是可选的，比如lang，若不传有默认值
	kkpager.generPageHtml({
		pno : getQueryString('page') || 1,
		//总页码
		total : args.pageCount,
		//总数据条数
		totalRecords : args.recordNum,
		//链接前部
		hrefFormer :'',
		//链接尾部
		hrefLatter :'',
		getLink : function(n){
			if(args.fieldDef){
				return this.hrefFormer + this.hrefLatter + queryStr +  '&page=' + n;
			}else{
				return this.hrefFormer + this.hrefLatter + "?page=" + n;
			}
		},
		lang : {  
			firstPageText : '首页',  
			lastPageText : '尾页',  
			prePageText : '<',  
			nextPageText : '>',  
			totalPageBeforeText : '共',  
			totalPageAfterText : '页',  
			totalRecordsAfterText : '条数据',  
			gopageBeforeText :"转到",  
			gopageButtonOkText : '确定',  
			gopageAfterText : '页',  
			buttonTipBeforeText : '第',  
			buttonTipAfterText : '页'  
		}
	});
}

//返回URL参数值
function getQueryString(name) {
	var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");

	var u = window.location.search.substr(1);
	encodeURI(u);
	var r = decodeURI(u).match(reg);
	if (r != null) return unescape(r[2]); return null;
}

