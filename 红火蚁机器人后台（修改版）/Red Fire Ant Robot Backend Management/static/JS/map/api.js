// ;
// var map_api_ops = {
//     init: function () {
//         this.eventBind();
//     },
//     eventBind: function () {
//         $(".wrap_account_set .save").click(function () {
//             //            var btn_target = $(this);
//             //小车编号
//             var carID_target = $(".wrap_account_set input[name=carID]");
//             var carID = carID_target.val();
//             // //工作地点
//             // var position_target = $(".wrap_account_set input[name=position]");
//             // var position = position_target.val();
//             //工作状态
//             var workstate_target = $(".wrap_account_set input[name=workstate]");
//             var workstate = workstate_target.val();
//             //时间戳
//             var time_target = $(".wrap_account_set input[name=time]");
//             var time = time_target.val();
//             // 经度
//             var longitude_target = $(".wrap_account_set input[name=longitude]");
//             var longitude = longitude_target.val();
//             //纬度
//             var latitude_target = $(".wrap_account_set input[name=latitude]");
//             var latitude = latitude_target.val();
//             //是否复查
//             var is_sanitized_target = $(".wrap_account_set input[name=is_sanitized]");
//             var is_sanitized = is_sanitized_target.val();
//             //图片
//             var image_target = $(".wrap_account_set input[name=image]");
//             console.log("image_target:", image_target)
//             var image = image_target.val()
//             //参数校验部分
//             if (carID.length < 1) {
//                 common_ops.tip("请输入小车编号", carID_target)
//                 return false;
//             }

//             // if (position.length < 1) {
//             //     common_ops.tip("请输入符合规范的地点", position_target)
//             //     return false;
//             // }

//             if (workstate.length < 1) {
//                 common_ops.tip("请输入符合规范的工作状态", workstate_target)
//                 return false;
//             }


//             if (time.length < 1) {
//                 common_ops.tip("请输入符合规范的时间戳", time_target)
//                 return false;
//             }

//             if (longitude.length < 1) {
//                 common_ops.tip("请输入符合规范的经度", longitude_target)
//                 return false;
//             }

//             if (latitude.length < 1) {
//                 common_ops.tip("请输入符合规范的纬度", latitude_target)
//                 return false;
//             }

//             if (is_sanitized.length < 1) {
//                 common_ops.tip("请输入符合规范的复查数据（0/1）", is_sanitized_target)
//                 return false;
//             }

         


//             //完成基本验证之后待发送数据
//             var data = {
//                 // position: position,
//                 workstate: workstate,
//                 time: time,
//                 longitude: longitude,
//                 latitude: latitude,
//                 carID: carID,
//                 image: image,
//                 is_sanitized: is_sanitized,
//             };
//             console.log("data:",data)

//             $.ajax({
//                 url: common_ops.buildUrl("/map/api"),
//                 type: 'POST',
//                 data: data,
//                 dataType: 'json',
//                 success: function (res) {
//                     var callback = null;
//                     if (res.code == 200) {
//                         callback = function () {
//                             console.log(res)
//                             window.location.href = common_ops.buildUrl("/map/index");

//                         }
//                     }
//                     common_ops.alert(res.msg, callback);
//                 }


//             })



//         });
//     }
// };

// $(document).ready(function () {
//     map_api_ops.init();
// });

var map_api_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        document.querySelector(".wrap_account_set .save").addEventListener('click', function () {
            // 小车编号
            var carID_target = document.querySelector(".wrap_account_set input[name=carID]");
            var carID = carID_target.value;
            // 工作状态
            var workstate_target = document.querySelector(".wrap_account_set input[name=workstate]");
            var workstate = workstate_target.value;
            // 时间戳
            var time_target = document.querySelector(".wrap_account_set input[name=time]");
            var time = time_target.value;
            // 经度
            var longitude_target = document.querySelector(".wrap_account_set input[name=longitude]");
            var longitude = longitude_target.value;
            // 纬度
            var latitude_target = document.querySelector(".wrap_account_set input[name=latitude]");
            var latitude = latitude_target.value;
            // 是否复查
            var is_sanitized_target = document.querySelector(".wrap_account_set input[name=is_sanitized]");
            var is_sanitized = is_sanitized_target.value;
            // 图片
            var image_target = document.querySelector(".wrap_account_set input[id=imageInput]");
            console.log("image_target:", image_target);
            var image = image_target.files[0];

            // 参数校验部分
            if (carID.length < 1) {
                common_ops.tip("请输入小车编号", carID_target);
                return false;
            }

            if (workstate.length < 1) {
                common_ops.tip("请输入符合规范的工作状态", workstate_target);
                return false;
            }

            if (time.length < 1) {
                common_ops.tip("请输入符合规范的时间戳", time_target);
                return false;
            }

            if (longitude.length < 1) {
                common_ops.tip("请输入符合规范的经度", longitude_target);
                return false;
            }

            if (latitude.length < 1) {
                common_ops.tip("请输入符合规范的纬度", latitude_target);
                return false;
            }

            if (is_sanitized.length < 1) {
                common_ops.tip("请输入符合规范的复查数据（0/1）", is_sanitized_target);
                return false;
            }

            if (!image) {
                common_ops.tip("请选择图片文件", image_target);
                return false;
            }

            // 完成基本验证之后待发送数据
            var data = new FormData();
            data.append('carID', carID);
            data.append('workstate', workstate);
            data.append('time', time);
            data.append('longitude', longitude);
            data.append('latitude', latitude);
            data.append('is_sanitized', is_sanitized);
            data.append('image', image);

            console.log("data:", data);

            var xhr = new XMLHttpRequest();
            xhr.open('POST', common_ops.buildUrl("/map/api"), true);
            xhr.onreadystatechange = function () {
                if (xhr.readyState == 4) {
                    console.log("xhr response:", xhr.responseText);
                    if (xhr.status == 200) {
                        try {
                            var res = JSON.parse(xhr.responseText);
                            var callback = null;
                            if (res.code == 200) {
                                callback = function () {
                                    console.log(res);
                                    window.location.href = common_ops.buildUrl("/map/index");
                                }
                            }
                            common_ops.alert(res.msg, callback);
                        } catch (e) {
                            console.error("Error parsing JSON:", e);
                            common_ops.alert("服务器响应格式错误");
                        }
                    } else {
                        common_ops.alert("请求失败，状态码：" + xhr.status);
                    }
                }
            };
            xhr.send(data);
        });
    }
};

document.addEventListener('DOMContentLoaded', function () {
    map_api_ops.init();
});
