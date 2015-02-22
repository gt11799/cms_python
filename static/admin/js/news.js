
//删除	
function deleteItems(id,type){
	popAjax({
		title : '提示',
		content: '是否确定删除？',
		url : '/zixun/admin/delete/',
		reload : true,
		getData　: function(){
			return {
	 			id : id,
	 			object : type
 			}
		} 
	});
}

//是否推荐	
function ifRecommed(id,status,type){
	var con = '是否点击推荐？';

	if(status==0){
		con = "是否取消推荐？"
	}
	popAjax({
		title : '提示',
		content: con,
		url : '/zixun/admin/recommend/',
		reload : true,
		getData　: function(){
			return {
	 			id : id,
	 			status : status,
	 			object : type
 			}
		} 
	});
}