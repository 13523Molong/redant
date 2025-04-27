var user_login_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".login-box .do-login").click(function () {
            var login_name = $(".login-box input[name=login_name]").val();
            var login_pwd = $(".login-box input[name=login_pwd]").val();

            if (login_name === undefined || login_name.length < 1) {
                common_ops.alert("请输入正确的登录用户名");
                return;
            }

            if (login_pwd === undefined || login_pwd.length < 1) {
                common_ops.alert("请输入正确的登录密码");
                return;
            }

            // 使用AJAX提交
            // $.post("http://172.30.235.74:5000/login", { 'login_name': login_name, 'login_pwd': login_pwd }, function (res) {
            //     var callback = null;
            //     if (res.code === 200) {
            //         callback = function () {
            //             window.location.href = common_ops.buildUrl("/");
            //         }
            //     }
            //     common_ops.alert(res.msg, callback);
            // });  
            $.ajax({
                url: "http://172.30.255.74:8009/login",
                type: "POST",
                contentType: "application/json", // 设置内容类型为 JSON
                data: JSON.stringify({ 'login_name': login_name, 'login_pwd': login_pwd }), // 序列化为 JSON
                dataType: 'json',
                success: function (res) {
                    var callback = null;
                    if (res.code === 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });
        });
    }
};

$(document).ready(function () {
    user_login_ops.init();
});

