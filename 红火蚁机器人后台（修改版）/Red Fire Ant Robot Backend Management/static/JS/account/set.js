;
var account_set_ops = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        $(".wrap_account_set .save").click(function(){
//            var btn_target = $(this);
        //用户名
        var nickname_target = $(".wrap_account_set input[name=nickname]");
        var nickname = nickname_target.val();
        //手机
        var mobile_target = $(".wrap_account_set input[name=mobile]");
        var mobile = mobile_target.val();
        //邮箱
        var email_target = $(".wrap_account_set input[name=email]");
        var email = email_target.val();
        // 登录名
        var login_name_target = $(".wrap_account_set input[name=login_name]");
        var login_name = login_name_target.val();
        //密码
        var login_pwd_target = $(".wrap_account_set input[name=login_pwd]");
        var login_pwd = login_pwd_target.val();

//参数校验部分

        if(nickname.length<1){
            common_ops.tip("请输入符合规范的姓名", nickname_target)
            return false;
        }

        if(mobile.length<1){
            common_ops.tip("请输入符合规范的手机", mobile_target)
            return false;
        }


        if(email.length<1){
                    common_ops.tip("请输入符合规范的邮箱", email_target)
                    return false;
                }

        if(login_name.length<1){
            common_ops.tip("请输入符合规范的登录用户名", login_name_target)
            return false;
        }

        if(login_pwd.length<6){
            common_ops.tip("请输入符合规范的登录密码", login_pwd_target)
            return false;
        }





        //完成基本验证之后待发送数据
        var data = {
            nickname:nickname,
            email:email,
            mobile:mobile,
            login_name:login_name,
            login_pwd:login_pwd,
            id:$(".wrap_account_set input[name=id]").val()
        };


        $.ajax({
            url:common_ops.buildUrl("/account/set"),
            type:'POST',
            data:data,
            dataType:'json',
            success:function(res){
                var callback = null;
                    if(res.code==200){
                        callback = function(){
                            window.location.href = common_ops.buildUrl("/account/new_index");

                        }
                    }
                    common_ops.alert(res.msg,callback);
            }


        })



        });
    }
};

$(document).ready(function(){
    account_set_ops.init();
});