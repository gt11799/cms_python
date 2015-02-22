//首页一系列对奇
(function($){
    $(function(){
        var scrollTop,
            nav = $("#nav"),
            ladyTop = $("#ladys").length ? $("#ladys").offset().top : 0,
            childrenTop = $("#children").length ? $("#children").offset().top : 0,
            crazyTop = $("#crazy").length ? $("#crazy").offset().top : 0,
            todayTop = $('#today').offset().top,
            wrapOverlayTop = $(".wrap_overlay").offset().top,
            leftSideTop  = 344, //left_side距离屏幕顶的距离
            headTop =  0;
            if($("#slider").length){
                headTop = $("#slider").offset().top
            }

        $(window).on("scroll",function(){
            scrollTop = $(this).scrollTop();

            if(scrollTop>headTop){
                nav.addClass("fixed").css({"top":0});
            }else{
                nav.css({"top":-36}).removeClass("fixed");
            }
            autoAlign(scrollTop);

            if(!$("#ladys").length){return}
            if(scrollTop>(ladyTop-leftSideTop) && scrollTop<(childrenTop-leftSideTop)){
                $(".left_side").find(".lady").addClass("on").siblings().removeClass("on")
            }else if(scrollTop>(childrenTop-leftSideTop) && scrollTop<(crazyTop-leftSideTop)){
                $(".left_side").find(".boy").addClass("on").siblings().removeClass("on")
            }else if(scrollTop>(crazyTop-leftSideTop)){
                 $(".left_side").find(".last").addClass("on").siblings().removeClass("on")
            }else if(scrollTop>(todayTop-leftSideTop)){
                $(".left_side").find(".today").addClass("on").siblings().removeClass("on")
            }else{
                $(".left_side li").removeClass("on")
            }

            
        })

        autoAlign(0)

        function autoAlign(scrolltop){
            var scrollTop = scrolltop;
            //console.log(wrapOverlayTop)
            if(scrollTop>220){
                $(".left_side,.side_panel").css({"marginTop":-80,"top":"50%"})
                 $(".float_md_l,.float_md_r").css({"marginTop":-100,"top":"50%"})
                // $(".index_qiandao").css({"marginTop":130,"top":"50%"})
                 //$('.kefu_for_other').css({'marginTop':174,'top':'50%'});//236
            }else{
                $(".left_side,.side_panel").css({"marginTop":0,"top":(wrapOverlayTop+22)})//80
                 $(".float_md_l,.float_md_r").css({"marginTop":0,"top":(wrapOverlayTop+17)})
                // $(".index_qiandao").css({"marginTop":0,"top":(wrapOverlayTop+296)})
                 //$('.kefu_for_other').css({'marginTop':0,'top':(wrapOverlayTop+309)});//371
            }
        }

        $("#J_product_list .J_end_time").each(function(i){
            var that = $(this);
            new xhTimeOut({
                elem:that,
                maxtime:that.data("time")
            })
        });

    })
    
    //加入收藏
    $(function(){
        var cookie_f = $.cookie("favorite_tips");
        if(!cookie_f){
            $(".header").before('<div class="favorite_tips"><div class="content">CTRL+D 收藏"小荷特卖"，xiaoher.com <a href="javascript:;" class="fc36c close J_close_f">不再提示</a></div></div>');
        }
        $(".J_close_f").on("click",function(){
            $.cookie("favorite_tips", "hidden",{expires:30,path: '/'});
            $(".favorite_tips").remove();
        })

        analyze();//优惠劵派送
    })
})(jQuery)


//首页弹窗广告
if(!$.cookie('index_pop')){
    var couponImage = new Image();
    couponImage.onload = function(){
        var d = dialog({
            title: false,
            fixed:true,
            skin : 'coupon_pop',
            backdropOpacity : 0.9,
            zIndex : 10000,
            padding:"0",
            lock:true,
            opacity:0.3,
            content:$('.index_pop .coupon_ad')[0]
        });
        d.showModal();
        $(".coupon_ad .J_close,.coupon_ad .J_btn").on("click",function(){
            d.close();
            return false;
        });
        $.cookie('index_pop', 1 ,{
            expires : 30,
            path : '/'
        });
    }
    couponImage.src = $('.coupon_ad img').attr('src');
}

//加入心愿单
(function($){
    $('.J_add_wish').on("click",function(){
        var _this = $(this),
        noLogin = false,
        phone = _this.find('input[type=hidden]').attr("data-phone"),
        type = _this.attr("data-type"),
        tp1 = '';

        if(_this.find('input[type=hidden]').val()!='False'){
            noLogin = true;
        }
        if(noLogin==true){  
           showPhoneLogin();
           return false;
           // showLoginDialog(phone);
          // window.location.href = '/login'
        }

        if(type == "activity"){
            tp1 += '<div class="alertwrap">您已经将该活动加入心愿单，不能重复加入哦！</div>';
        }else{
            tp1 += '<div class="alertwrap">您已经将该商品加入心愿单，不能重复加入哦！</div>';
        }
        loading.open();
        $.post("/add_user_wish_list?_rand="+Math.random(),{
            wish_list_id : _this.find('input[type=hidden]').attr('data-id')
        },function(data){

            if(data.status===0){
                //刷新侧栏心愿单
                showWish(); 
                var d = dialog({
                    title:"温馨提示",
                    content: '<div class="alertwrap"><p class="success"><span class="success_icon"></span>您已经成功加入心愿单！</p><div class="tips"><p>小荷特卖会在开团前第一时间发送：短信通知至'+data.phone+'</p></div><p>已订阅的的开团提醒</p></div>',
                    okValue:"确定",
                    skin:"normal",
                    ok : function(){
                        //window.location.reload();
                    }
                });
                d.showModal();
            }else if(data.status==2){
                var d = dialog({
                    title:"温馨提示",
                    content:tp1,
                    skin:"normal",
                    okValue:"确定",
                    ok:function(){
                      //  window.location.reload();
                    }
                });
                d.showModal();
            }else{
                showMsg(data.msg || "出错了，请联系客服解决哦");
            }
            loading.close();
        });  
    });
})(jQuery);

//优惠劵派送
function analyze(){
    var html ='';
    $.get('/get_request_Coupon/?channel=',function(data){
        data = JSON.parse(data);  
        if(data){
            //<h2>'+data['activity_name']+'</h2>
            html += '<div class="get_coupon index_get_coupon"><div class="hd" style="padding:4px 0 0"></div><div class="bd">';
            switch(data["coupon_type"]){
                case 0:
                    html += '<div class="coupon clearfix">'
                    break;
                case 1:
                    html += '<div class="coupon xh clearfix">'
                    break;
                case 2:
                    html += '<div class="coupon mq clearfix">'
                    break;
                default:
                    html += '<div class="coupon py clearfix">'
            }
            html += '<ul>'+
                        '<li class="from J_source">来源：'+data['activity_desc']+'</li>'+
                        '<li class="date">有效期：'+data["avail_from"]+' - '+data["avail_to"]+'</li>'+
                        '<li class="juan">现金券</li>'+
                    '</ul>'+
                    '<div class="content clearfix">'+
                        '<div class="m">'+
                            '<span class="ico">￥</span>'+
                            '<span class="money J_amount">'+data['amount']+'</span>'+
                            '<span class="yuan">元</span>'+
                        '</div>'+
                    '</div>'+
                    '<input type="hidden" class="J_coupon_type" value="'+data['coupon_type']+'"/>'+
                    '<input type="hidden" class="J_inteval_days" value="'+data['inteval_days']+'"/>'+
                    '<input type="hidden" class="J_activity_id" value="'+data['id']+'"/>'+
                    '<div class="btn_box ">'+
                        '<p>*定单满<i class="J_limited_order_price">'+data['limited_order_price']+'</i>元即可使用</p>'+
                        '<p class="tips">*每张现金券只能在一个订单内使用</p>'+
                    '</div>'+
                    '</div>'+
                    '<div class="sub_box" style="margin-top:-10px"><a id="J_get_coupon" class="btn btn_green">立即领取</a></div>'+
                    '</div>'+
                    '<a href="javascript:;" class="icon_close2 J_colse"></a>'+
                    '</div>';

            var d = dialog({
                title: false,
                fixed:true,
                zIndex:1987,
                skin:"normal",
                content:html
            });

            d.showModal();
            
            $(function(){
                $("#J_get_coupon").on("click",function(){
                        $.post("/get_coupon/?_random="+Math.random(),{
                        _xsrf:Base.getCookie("_xsrf"),
                        inteval_days:$(".J_inteval_days").val(),
                        limited_order_price:$(".J_limited_order_price").html(),
                        source:$(".J_source").html(),
                        amount:$(".J_amount").html(),
                        activity_id:$(".J_activity_id").val(),
                        coupon_type:$(".J_coupon_type").val()
                    },function(data){
                        var status = data.status;
                        if(status===0){
                            $(".get_coupon").html('<div class="coupon_suc" style="text-align:center;padding-top:20px"><img src="/static/images/smile.png"><p style="padding:10px; color:#df4461; font-size:18px">恭喜！</p><p style="padding:10px; color:#666; font-size:14px">现金券已经领取，结算时即可使用。</p><p><a href="javascript:;" class="J_colse" style="color:#36c">马上去购物>></a></p></div>');
                        }else{
                            alert("失败了");
                        }
                    })
                })

                $("body").on("click",".J_colse",function(){
                    d.close();
                })
            })
        }
    })
}