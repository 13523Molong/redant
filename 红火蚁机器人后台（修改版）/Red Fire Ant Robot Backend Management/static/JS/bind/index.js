;
var account_index_ops = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        var that = this;
        $(".wrap_search .search").click(function(){
            $(".wrap_search").submit();
        });

        $(".remove").click(function(){
            that.ops("remove",$(this).attr("data"),$(this).attr("module_data"),$(this).attr("module_name"));
        });

        $(".recover").click(function(){
            that.ops("recover",$(this).attr("data"),$(this).attr("module_data"),$(this).attr("module_name"));
        });
    },
    ops:function(act,id,module_id,module_name){
        var callback = {
            'ok':function(){
                $.ajax({
            url:common_ops.buildUrl("/eye/ops"),
            type:'POST',
            data:{
                act:act,
                id:id,
                module_id:module_id,
                module_name:module_name
            },
            dataType:'json',
            success:function(res){
                var callback = null;
                    if(res.code==200){
                        callback = function(){
                            window.location.href = window.location.href;

                        }
                    }
                    common_ops.alert(res.msg,callback);
            }


        })
            },
            'cancel':null
        }
        common_ops.confirm((act == "remove" ? "确定取消绑定？":"确定开始绑定？"),callback);


    }
};


$(document).ready(function(){
    account_index_ops.init();
});