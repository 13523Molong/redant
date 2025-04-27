
// var map_api_ops = {
//     init: function () {
//         this.eventBind();
//     },
//     eventBind: function () {
//         document.querySelector(".wrap_account_set .save").addEventListener('click', function () {
//             // 小车编号
//             var carID_target = document.querySelector(".wrap_account_set input[name=carID]");
//             var carID = carID_target.value;
//             // 经度
//             var longitude_target = document.querySelector(".wrap_account_set input[name=longitude]");
//             var longitude = longitude_target.value;
//             // 纬度
//             var latitude_target = document.querySelector(".wrap_account_set input[name=latitude]");
//             var latitude = latitude_target.value;

//             // 参数校验部分
//             if (carID.length < 1) {
//                 common_ops.tip("请输入小车编号", carID_target);
//                 return false;
//             }

//             if (longitude.length < 1) {
//                 common_ops.tip("请输入符合规范的经度", longitude_target);
//                 return false;
//             }

//             if (latitude.length < 1) {
//                 common_ops.tip("请输入符合规范的纬度", latitude_target);
//                 return false;
//             }

//             // 完成基本验证之后待发送数据
//             var data = new FormData();
//             data.append('carID', carID);
//             data.append('longitude', longitude);
//             data.append('latitude', latitude);
//             console.log("data:", data);
//             var xhr = new XMLHttpRequest();
//             xhr.open('POST', common_ops.buildUrl("/give_point/api"), true);
//             xhr.onreadystatechange = function () {
//                 if (xhr.readyState == 4) {
//                     console.log("xhr response:", xhr.responseText);
//                     if (xhr.status == 200) {
//                         try {
//                             var res = JSON.parse(xhr.responseText);
//                             var callback = null;
//                             if (res.code == 200) {
//                                 callback = function () {
//                                     console.log(res);
//                                     // window.location.href = common_ops.buildUrl("/give_point/index");
//                                 }
//                             }
//                             common_ops.alert(res.msg, callback);
//                         } catch (e) {
//                             console.error("Error parsing JSON:", e);
//                             common_ops.alert("服务器响应格式错误");
//                         }
//                     } else {
//                         common_ops.alert("请求失败，状态码：" + xhr.status);
//                     }
//                 }
//             };
//             xhr.send(data);
//         });
//     }
// };

// document.addEventListener('DOMContentLoaded', function () {
//     map_api_ops.init();
// });
