;
var bind_ops = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        var that = this;
        //下拉选框组件
        $(".wrap_food_set select[name=key]").select2({
            language: "zh-CN",
            width: '100%'
        });


//        表单值的获取
        $(".wrap_food_set .save").click(function(){
//            模块序列号
            var id_target = $(".wrap_food_set input[name=id]");
            var id = id_target.val();
            
//            模块名称
            var name_target = $(".wrap_food_set input[name=name]");
            var name = name_target.val();
            
            // 箱体选择
            var box_target = $(".wrap_food_set select[name=key]");
            var box = box_target.val();

//            进行参数有效性的校验
             if (parseInt(box) < 1) {
                common_ops.tip("请选择分类~~", box_target);
                return;
            }

            if(!id || id.length<1){
                common_ops.tip("页面出错",id_target)
                return false;
            }
              if(!name || name.length<1){
                common_ops.tip("页面出错",name_target)
                return false;
            }
            
            var data = {
                id:id,
                name:name,
                box:box
            };

//            进行AJAX提交
            $.ajax({
                 url: common_ops.buildUrl("/eye/bind"),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/eye/index");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }

            })

        })
    }
};

$(document).ready(function(){
    bind_ops.init();
});