/*
类目管理js
欧志活
*/

$(document).ready(function(){
    
    //初始化获取数据
    function setLeimu(pid,level,name,id){
        var pid = pid,
            name = name,
            id = id,
            level = level,
            leimu = getLeimu(0);
        if(leimu.length){
            for(var i=0,len = leimu.length; i<len; i++ ){
                    tpl = '<div class="folding">'+
                          '<div class="all_leimu">'+
                          '<ul  class="ul_line" data-level="'+leimu[i].level+'">'+
                          '<li class="slin"><input type="checkbox"  class="J_CatOpt checkbox"></li>'+
                          '<li class="slin sicon"><div class="icon_btn arrow"></div></li>'+
                          '<li class="mlin">'+
                          '<div class="input-box"><input type="text"  class="input-text J_CatName" autocomplete="off" value="'+leimu[i].name+'"  maxlength="20"></div>'+
                          '</li>'+
                          '<li class="move_box">'+
                          '<a href="#" class="move-top  J_CatMoveTop no-move-top">上移</a>'+
                          '<a class="move-up  J_CatMoveUp no-move-up" href="#">上移</a>'+
                          '<a class="move-down J_CatMoveDown" href="#">下移</a>'+
                          '<a href="#" class="move-btm  J_CatMoveBtm">下移</a>'+
                          '</li>'+
                          '<li class="set_time">'+leimu[i].create_time+'</li>'+
                          '<li class="work"><a class="J_CatDelete" href="#">删除</a></li>'+
                          '</ul></div>'+
                          '</div>'

                    $("#add_table").append(tpl); 
                    add_sibling(leimu[i]._id,leimu[i].level);
          
            }

            
        }
    }
    setLeimu(0,1);

    //点击添加手工分类方法
    function addLeimu(index,val,pid,level){
        var index = getLeimu(0); //测试
        var tpl ='<div class="folding">'+
                  '<div class="all_leimu">'+
                  '<ul>'+
                  '<li class="slin"><input type="checkbox"  class="J_CatOpt checkbox"></li>'+
                  '<li class="slin sicon"><div class="icon_btn arrow"></div></li>'+
                  '<li class="mlin">'+
                  '<div class="input-box"><input type="text"  class="input-text J_CatName" autocomplete="off" value=""  maxlength="20"></div>'+
                  '</li>'+
                  '<li class="move_box">'+
                  '<a href="#" class="move-top  J_CatMoveTop no-move-top">上移</a>'+
                  '<a class="move-up  J_CatMoveUp no-move-up" href="#">上移</a>'+
                  '<a class="move-down J_CatMoveDown" href="#">下移</a>'+
                  '<a href="#" class="move-btm  J_CatMoveBtm">下移</a>'+
                  '</li>'+
                  '<li class="set_time"></li>'+
                  '<li class="work"><a class="J_CatDelete" href="#">删除</a></li>'+
                  '</ul></div>'+
                  '<div class="child_leimu">'+
                  '<div class="leimu_'+index+'">'+
                  '<ul class="ul_line">'+
                  '<li class="slin">&nbsp;</li>'+
                  '<li class="slin">&nbsp;</li>'+
                  '<li class="mlin">'+
                  '<div class="next_icon"></div>'+
                  '<input type="text" class="add-cat add_leimu" value="添加子分类"/>'+
                  '<a id="add_leimu" class="btn_small add_lumu" title="添加子目录" style="font-size:12px;" href="#">+</a>'+
                  '</li>'+
                  '<li class="move_box"></li>'+
                  '<li class="set_time"></li>'+
                  '<li class="work"><a class="line_del" href="#">删除</a></li>'+
                  '</ul>'+
                  '</div>'+
                  '</div>'
        $("#add_table").append(tpl);
        //add_sibling(index)

    }
    

	//点击添加手工分类事件
	$("#J_add").click(function(){
        addLeimu();
	})

    //添加同类目录
    function add_sibling(pid,level){
        var _this=$(this),
             pid = pid,
             level = level,
             tpl; 
        _this.val('');
        var leimu =getLeimu(pid,level);
        console.log("**********"+leimu)
        if(leimu.length){
           for(var i=0,len = leimu.length; i<len; i++ ){
              tpl='<div class="leimu_'+level+' b_lin">'+
                  '<ul class="">'+
                  '<li class="slin">&nbsp;</li>'+
                  '<li class="slin">&nbsp;</li>'+
                  '<li class="mlin">'+
                  '<div class="next_icon"></div>'+
                  '<input type="text" class="add-cat add_leimu" value="'+leimu[i].name+'"/>'+
                  '<a id="add_leimu" class="btn_small add_lumu" title="添加子目录" style="font-size:12px;" href="#">+</a>'+
                  '</li>'+
                  '<li class="move_box"></li>'+
                  '<li class="set_time"></li>'+
                  '<li class="work"><a class="line_del" href="#">删除</a></li>'+
                  '</ul>'+
                  '</div>'

              if((leimu[i].level-1) == $(".ul_line").attr("data-level")){
                $(".ul_line").after(tpl);
              }else if(leimu[i].level > 1){
                $(".leimu_"+(leimu[i].level-1)).after(tpl);
              }
              add_sibling(leimu[i]._id,leimu[i].level);
           }
           
        }

        
        if(_this.val('')){
               _this.parents('.leimu_'+level).append(tpl);
        }
    }
   
    //添加同目录事件
    $("#add_table").on("focus",".add_leimu",function(){
         add_sibling();
    	
    })

    //添加子目录
    function add_next(index,pid,name){
        _$div = $(this);
        var tpl = '<div class="leimu_'+index+'">'+
                  '<ul class="ul_line">'+
                  '<li class="slin">&nbsp;</li>'+
                  '<li class="slin">&nbsp;</li>'+
                  '<li class="mlin">'+
                  '<div class="next_icon"></div>'+
                  '<input type="text" class="add-cat add_leimu" value="添加子分类"/>'+
                  '<a id="add_leimu" class="btn_small add_lumu" title="添加子目录" style="font-size:12px;" href="#">+</a>'+
                  '</li>'+
                  '<li class="move_box"></li>'+
                  '<li class="set_time"></li>'+
                  '<li class="work"><a class="line_del" href="#">删除</a></li>'+
                  '</ul>'+
                  '</div>'
        _$div.parents('.ul_line').append(tpl);

    }

    //添加子目录一
   $("#add_table").on("click",".add_lumu",function(){
       var index=$(this).index()+1;
    	add_next(index)
    })
     
    
    

    //新增的删除功能
    /*$("#add_table").on("click",".div_Del",function(){
        if(!$(this).parents(".lumu_div").next().hasClass('cat-sub')){
            if($(this).parent().parent().parent().find('.lumu_div').length==1){
                 $(this).parent().parent().parent().remove();
            }else{
                $(this).parents('.lumu_div').remove();
            }
        }else{
            alert("含有子集，不可删除!")
            return false;
        }
    })
   
    //删除选中小分类
    $("#add_table").on("click",".line_del",function(){
        if(!$(this).parent().parent().next().hasClass('lumu_1')){
             $(this).parents(".cat-sub").remove();
        }else{
            alert("含有子集，不可删除!")
            return false;
        }
    })

    //删除选中分类
    $("#add_table").on("click",".J_CatDelete",function(){
        if($(this).parents(".folding").find('.J_Confirmed').length<1){
            $(this).parents(".folding").remove();
        }else{
            alert("含有子集，不可删除!")
            return false;
        }    
    	
    })



    //伸展显示效果
    $("#add_table").on("click",".icon_btn",function(){
    	if($(this).hasClass('arrow')){ //隐藏子集
    		$(this).removeClass("arrow").addClass("arrow_hidden");
    		$(this).parents(".folding").find('.cat-sub').slideUp("fast");
    	}else{ //显示子集
    		$(this).removeClass("arrow_hidden").addClass("arrow");
    		$(this).parents(".folding").find('.cat-sub').slideDown("fast");
    		
    	}
    	
    })
     
    //展开功能
    $(".J_CollapseAll").click(function(){
    	$("#add_table .icon_btn").each(function(){	
    		$("#add_table .icon_btn").removeClass("arrow_hidden").addClass("arrow");
    		$("#add_table").find('.folding .cat-sub').slideDown("fast");
    	})
    })
    //收起功能
    $(".J_FoldingAll").click(function(){
    	$("#add_table .icon_btn").each(function(){	
    		$("#add_table .icon_btn").removeClass("arrow").addClass("arrow_hidden");
    		$("#add_table").find('.folding .cat-sub').slideUp("fast");
    	})
    })*/



    //初始化input状态
    $('input[type=checkbox]').removeAttr('checked');
    //全选功能
    $('.quanxuan').click(function(){
    	if($(this).is(':checked')){
    		$('#add_table .J_CatOpt').attr("checked",true);
            $('.del_w').removeClass('color_f').addClass('color_g');
    	}else{
    		$('#add_table .J_CatOpt').removeAttr("checked");
            $('.del_w').removeClass('color_g').addClass('color_f');
    	}

    })

   


    //单选或者多选,多选框取消选中状态
    $('#add_table').on('change','.J_CatOpt',function(){
    	var _this = $(this);
    	if(!_this.is(':checked')){
    		$('.quanxuan').removeAttr("checked");
    	}
    })

    //批量删除功能
    $('.del_w').click(function(){
    	var box_list=$('#add_table .J_CatOpt');
    	box_list.each(function(){
    		if($(this).is(':checked')){
                if($(this).parents('.folding').find('.J_Confirmed').length <1){
    			     $(this).parents(".folding").remove();
                }else{
                    alert("含有子集，不可删除!")
                    return false;
                }   
    		}else{
                 return false;
            }
    	})
    })

  


   //获取类目接口
    function getLeimu (pid,level) {
        var pid = pid,
            goods = "goods",
            leimu = ""    
        $.ajax({
            type:"get",
            //url:"/get_all_leimu/?leimu_type="+goods, 
            //url:"/get_leimu/?pid="+pid,
            url:"/get_leimu/?leimu_type="+goods,
            async:false,
            dataType:"json",
            data:{
                pid:pid,      
            },
            success:function(data){       
                leimu =data.leimu;
            },
            error:function(){
                alert("error")
            }
        })
        return leimu;
    }
    //getLeimu();
    
    //初始化数据加载
    /*function setLeimu(index,val,pid,level){
        var index = index,
            thisVal = val,
            cid = cid,
            level = level,
            leimu = getLeimu (thisVal,level);

    }*/


    
   
})



