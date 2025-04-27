;
var map_set_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".wrap_account_set .save").click(function () {
            //            var btn_target = $(this);
            //小车编号
            var carID_target = $(".wrap_account_set input[name=carID]");
            var carID = carID_target.val();
            //工作地点
            var position_target = $(".wrap_account_set input[name=position]");
            var position = position_target.val();
            //工作状态
            var workstate_target = $(".wrap_account_set input[name=workstate]");
            var workstate = workstate_target.val();
            // //时间戳
            // var time_target = $(".wrap_account_set input[name=time]");
            // var time = time_target.val();
            // // 经度
            // var longitude_target = $(".wrap_account_set input[name=longitude]");
            // var longitude = longitude_target.val();
            // //纬度
            // var latitude_target = $(".wrap_account_set input[name=latitude]");
            // var latitude = latitude_target.val();

            //参数校验部分
            if (carID.length < 1) {
                common_ops.tip("请输入小车编号", carID_target)
                return false;
            }

            if (position.length < 1) {
                common_ops.tip("请输入符合规范的地点", position_target)
                return false;
            }

            if (workstate.length < 1) {
                common_ops.tip("请输入符合规范的工作状态", workstate_target)
                return false;
            }


            // if (time.length < 1) {
            //     common_ops.tip("请输入符合规范的时间戳", time_target)
            //     return false;
            // }

            // if (longitude.length < 1) {
            //     common_ops.tip("请输入符合规范的经度", longitude_target)
            //     return false;
            // }

            // if (latitude.length < 1) {
            //     common_ops.tip("请输入符合规范的纬度", latitude_target)
            //     return false;
            // }





            //完成基本验证之后待发送数据
            var data = {
                position: position,
                workstate: workstate,
                // time: time,
                // longitude: longitude,
                // latitude: latitude,
                // id: $(".wrap_account_set input[name=id]").val(),
                carID: carID
            };


            $.ajax({
                url: common_ops.buildUrl("/map/set"),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/map/index");

                        }
                    }
                    common_ops.alert(res.msg, callback);
                }


            })



        });
    }
};

$(document).ready(function () {
    map_set_ops.init();
});