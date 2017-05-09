/**
 * Created by root on 2017/4/18.
 */

angularApp.register.controller('loginCtrl', ['$state', '$scope', '$http', 'promise', 'projectInfo', function($state, $scope, $http, promise, projectInfo) {

	var params;
	var path=env[env['get']]['login']; //获取登录模块的路径
	var url =path['login'];

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
					alert(result.data.msg);
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
					alert('注册成功');
				} else {
					alert('注册失败');
				}

			} else {
				alert(result.info);
			}
		})
	}

    //绑定模态框关闭事件
	angular.element('#register').on('hide.bs.modal', function() {
		angular.element('#register').find('input').val('');
	})

	$.backstretch("img/login-bg.jpg", {
		transitionDuration: 200
	});
}])