/**
 * Created by root on 2017/4/18.
 */

angularApp.register.controller('loginCtrl', ['$state', '$scope', '$http', 'promise', 'projectInfo', '$timeout',function($state, $scope, $http, promise, projectInfo,$timeout) {

    var params;
    var path=env[env['get']]['login']; //获取登录模块的路径
    var url =path['login'];
    // var form=document.getElementById('registerForm');

    //登录
    $scope.toSlidebar = function(obj) {
        var username = angular.element('#inputUserName').val();
        var userpwd = angular.element('#inputPassword').val();

        params = angular.extend({
            'opr': 'login'
        }, {
            'name': username,
            'pwd': userpwd
        });

        promise(params, url).then(function(result) {

            if(result.flag) {
                if(0 == result.data.status) {
                    var allProject = result.data.data; //获取的是数组
                    projectInfo.setUserName(username);
                    projectInfo.setAllProject(allProject);
                    console.log(allProject)
                    $state.go('slidebar.project', {'detailData': allProject});
                } else {
                    $scope.alertInfo = true;
                    $scope.msg="用户名或密码错误！";
                    setStyle('loginAlert','loginIcon',false);
                    //document.getElementById('loginAlert').className = "alert alert-danger col-sm-2 icon-space fade in";
                    //document.getElementById('loginIcon').className = "icon glyphicon glyphicon-ban-circle";
                    //angular.element('.alert').addClass('alert-danger');
                    //angular.element('.icon').addClass('glyphicon-ban-circle');
                    $timeout(function(){
                        $scope.alertInfo = false;
                    },1000)
                }

            } else {
                alert(result.info);
            }
        });
    }

    //注册

    $scope.toRegister = function() {
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

        promise(params, url).then(function(result) {

            if(result.flag) {

                if(0 == result.data.status) {
                    $scope.alertInfo = true;
                    $scope.msg="注册成功！";
                    setStyle('loginAlert','loginIcon',true);
                    //document.getElementById('loginAlert').className = "alert alert-success col-sm-8 icon-space fade in";
                    //document.getElementById('loginIcon').className = "icon glyphicon glyphicon-ok-circle";
                    $timeout(function(){
                        $scope.alertInfo = false;
                    },1000)
                } else {
                    $scope.alertInfo = true;
                    $scope.msg="注册失败！";
                    setStyle('loginAlert','loginIcon',false);
                    //document.getElementById('loginAlert').className = "alert alert-danger col-sm-8 icon-space fade in";
                    //document.getElementById('loginIcon').className = "icon glyphicon glyphicon-ban-circle";
                    //angular.element('.alert').addClass('alert-danger');
                    //angular.element('.icon').addClass('glyphicon-ban-circle');
                    $timeout(function(){
                        $scope.alertInfo = false;
                    },1000)
                }

            } else {
                alert(result.info);
            }
        }).then(function(res){

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

/**
 * 切换提示样式
 * id_alert:弹框文字的id
 * id_icon:图标的id
 *
 */
function setStyle(id_alert,id_icon,flag) {
    if(flag){
        document.getElementById(id_alert).className = "alert alert-success pull-right col-sm-2 icon-space fade in";
        document.getElementById(id_icon).className = "icon glyphicon glyphicon-ok-circle";
    }else{
        document.getElementById(id_alert).className = "alert alert-danger pull-right col-sm-2 icon-space fade in";
        document.getElementById(id_icon).className = "icon glyphicon glyphicon-ban-circle";
    }
}