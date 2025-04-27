;
var account_index_ops = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        var that = this;
//        开始运行任务时间的设定
        $("#field2").AnyTime_picker({
            format: "%H:%i:%s", labelTitle: "Time",
            labelHour: "Hour", labelMinute: "Minutes"
        } );
//         AnyTime.picker( "field1",{ format: "%W, %M %D in the Year %z %E", firstDOW: 1 } );
         AnyTime.picker( "field1",{ format: "%Y-%m-%d", firstDOW: 1 } );

//下拉选框组件
        $(".wrap_food_set select[name=key]").select2({
            language: "zh-CN",
            width: '100%'
        });


//        表单值的获取
        $(".wrap_food_set .save").click(function(){
//            任务id
            var id_target = $(".wrap_food_set input[name=id]");
            var id = id_target.val();

//            箱体id
            var obj_id_target = $(".wrap_food_set input[name=obj_id]");
            var obj_id = obj_id_target.val();

            var start_date_target = $(".wrap_food_set input[name=start_date]");
            var start_date = start_date_target.val();

            var start_time_target = $(".wrap_food_set input[name=start_time]");
            var start_time = start_time_target.val();

//            用户设定时间
            var time = start_date + " " + start_time

//            运行半径
            var radius_target = $(".wrap_food_set input[name=radius]");
            var radius = radius_target.val();

//            运行高度
            var height_target = $(".wrap_food_set input[name=height]");
            var height = height_target.val();

//            俯仰角
            var angle_target = $(".wrap_food_set input[name=angle]");
            var angle = angle_target.val();


//            拍摄速度
            var speed_target = $(".wrap_food_set input[name=speed]");
            var speed = speed_target.val();

//            拍摄次数
            var times_target = $(".wrap_food_set input[name=times]");
            var times = times_target.val();

//            运行模式
            var type_target = $(".wrap_food_set select[name=key]");
            var type = type_target.val();

            if (!id || id<0) {
                common_ops.tip("请输入任务序列号", id_target);

                return;
            }

            if (!obj_id || obj_id<0) {
                common_ops.tip("请输入环境集群序列号", obj_id_target);
                return;
            }

//            进行参数有效性的校验
             if (parseInt(type) < 1) {
                common_ops.tip("请选择分类~~", type_target);
                return;
            }

            if(!radius || radius.length<1){
                common_ops.tip("请输入运行半径",radius_target)
                return false;
            }
              if(!height || height.length<1){
                common_ops.tip("请输入运行高度",height_target)
                return false;
            }
              if(!speed || speed_target.length<1){
                common_ops.tip("请输入运行速度",speed_target)
                return false;
            }
              if(!angle || angle.length<1){
                common_ops.tip("请输入俯仰角",angle_target)
                return false;
            }
              if(!times || times.length<1){
                common_ops.tip("请输入运行次数",times_target)
                return false;
            }

            if (!time || time.length<1) {
                common_ops.alert("请设定运行时间");
                return;
            }




            var data = {
                id:id,
                time:time,
                radius:radius,
                angle:angle,
                height:height,
                type:type,
                times:times,
                speed:speed,
                obj_id:obj_id

            };

//            进行AJAX提交
            $.ajax({
                 url: common_ops.buildUrl("/command/add"),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/command/add");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }

            })

        })
    }

};

$(document).ready(function(){
    account_index_ops.init();
});