/**
 * Created by root on 2018/5/26 0026.
 */
$(function () {

    // 登录表单

    $("#loginForm").formValidator({
        username: {
            rule: "username",
            maxLength: 16,
            minLength: 6
        },

        password: {
            rule: "password"
        },

        vcode: {
            minLength: 4,
            maxLength: 4
        }
    }, {
        url: "/user/login/",
        success: function (data) {
            if (data.status) {
                location.href = "/blog/index/"
            } else {
                console.log(data)
            }
        },
        error: function (status) {
            console.log("ajaxSubmit.error", status);
        }
    }, {
        normal: "* 必填项"
    });


    // 注册表单
    $("#registerForm").formValidator({
        username: {
            rule: "username",
            ajax: "/user/valid_username?username=username",
            maxLength: 16,
            minLength: 6,
            message: {
                error: "错误：当前用户名已存在。"
            }
        },

        password: {
            rule: "password"
        },

        confirmPassword: {
            rule: "confirmPassword",
            equalTo: "password"
        },

        email: {
            rule: "email"
        },

        vcode: {
            minLength: 4,
            maxLength: 4
        }
    }, {
        url: "/user/register/",
        success: function (data) {
            if (data.status) {
                layer.msg("注册成功,即将跳转到登录页面!", {
                    time: 2000 //2秒关闭（如果不配置，默认是3秒）
                }, function () {
                    window.location.href = "/user/login/"
                })
            }
            console.log("ajaxSubmit.data", data);
        },
        error: function (status) {
            console.log("ajaxSubmit.error", status);
        }
    }, {
        normal: "* 必填项"
    });


});