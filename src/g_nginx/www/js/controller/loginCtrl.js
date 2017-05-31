/**
 * Created by root on 2017/4/18.
 */

angularApp.register.controller('loginCtrl', ['$state', '$scope', '$http', 'promise', 'projectInfo', '$timeout', function ($state, $scope, $http, promise, projectInfo, $timeout) {

    var params;
    var path = env[env['get']]['login']; //获取登录模块的路径
    var url = path['login'];
    // var form=document.getElementById('registerForm');

    //登录
    $scope.loginKeyup = function (e) {
        var keycode = window.event ? e.keyCode : e.which;//获取按键编码
        if (keycode == 13) {
            $scope.toSlidebar();
        }
    }

    $scope.toSlidebar = function (obj) {
        var username = angular.element('#inputUserName').val();
        var userpwd = angular.element('#inputPassword').val();

        params = angular.extend({
            'opr': 'login'
        }, {
            'name': username,
            'pwd': userpwd
        });

        promise(params, url).then(function (result) {

            if (result.flag) {
                if (0 == result.data.status) {
                    var allProject = result.data.data; //获取的是数组
                    projectInfo.setUserName(username);
                    projectInfo.setAllProject(allProject);
                    console.log(allProject)
                    $state.go('slidebar.project', {'detailData': allProject});
                    angular.element('.modal-backdrop').remove();//移除模态框遮罩层
                } else {
                    setStyle('loginAlert', 'loginIcon', '#loginTips', false, $scope, "用户名或密码错误!");
                }
            } else {
                alert(result.info);
            }
        });
    }

    //注册
    $scope.toRegister = function () {
        var registerName = angular.element('#registerName').val();
        var registerPwd = angular.element('#registerPwd').val();
        var registerEmail = angular.element('#registerEmail').val();

        params = angular.extend({
            'opr': 'useradd'
        }, {
            'name': registerName,
            'pwd': registerPwd,
            'email': registerEmail
        });

        promise(params, url).then(function (result) {

            if (result.flag) {

                if (0 == result.data.status) {
                    setStyle('loginAlert', 'loginIcon', '#loginTips', true, $scope, "注册成功!");
                } else {
                    setStyle('loginAlert', 'loginIcon', '#loginTips', false, $scope, "注册失败!");
                }

            } else {
                alert(result.info);
            }
        }).then(function (res) {

            //清空表单数据
            $scope.user = '';
            $scope.password1 = '';
            $scope.password2 = '';
            $scope.email = '';

            // form.reset();
            $scope.register.$setPristine();//重置表单验证状态
        })
    }

    $scope.toReset = function () {

        //清空表单数据
        $scope.user = '';
        $scope.password1 = '';
        $scope.password2 = '';
        $scope.email = '';

        // form.reset();

        //重置表单验证状态
        $scope.register.$setPristine();
    }

    $.backstretch("img/login-bg.jpg", {
        transitionDuration: 200
    });

}])