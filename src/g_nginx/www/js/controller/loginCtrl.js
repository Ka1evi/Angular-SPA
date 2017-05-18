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
                    $scope.msg="用户名或密码错误！";
					angular.element('.alert').addClass('alert-danger');
                    angular.element('.icon').addClass('glyphicon-ban-circle');
                    $scope.alertInfo = true;
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
        $scope.successed = false;
        $scope.failed = false;
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

                $scope.alertInfo = true;
				if(0 == result.data.status) {
					$scope.msg="注册成功！";
                    $timeout(function(){
                        $scope.alertInfo = false;
                    },1000)
				} else {
					$scope.msg="注册失败！";
                    angular.element('.alert').addClass('alert-danger');
                    angular.element('.icon').addClass('glyphicon-ban-circle');
                    $scope.alertInfo = true;
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

    //绑定模态框关闭事件
	/*angular.element('#register').on('hide.bs.modal', function() {
		
		$scope.register.$setPristine();//重置表单验证状态
		angular.element('#register').find('input').val('');
	})*/

	$.backstretch("img/login-bg.jpg", {
		transitionDuration: 200
	});
}])