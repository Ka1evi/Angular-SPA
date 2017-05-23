/**
 * Created by root on 2017/4/12.
 */

angularApp.register.controller('projectCtrl', ['$scope', '$http', 'projectInfo', '$state', '$stateParams', 'promise', '$timeout', '$rootScope', function ($scope, $http, projectInfo, $state, $stateParams, promise, $timeout, $rootScope) {
    var params;
    var path = env[env['get']]['project']; //获取选择项目的路径
    var url = path['project'];
    var vm = $scope.vm = {};
    console.log($stateParams.detailData)
    vm.projectInfo = $stateParams.detailData;

    //跳转url
    $scope.jump = function () {

        var projectId = angular.element('#projectId').text();  //获取项目的id
        console.log(vm.projectName.name)
        projectInfo.setProjectName(vm.projectName.name);    //设置项目名
        projectInfo.setModelId(projectId);                  //设置项目id

        if (projectId != null) {
            params = angular.extend({'opr': 'proquery'}, {'id': projectId});

            promise(params, url).then(function (result) {
                if (result.flag) {
                    var projectDetail = result.data;
                    var model = projectDetail.model;
                    console.log(projectDetail);
                    projectInfo.setModules(model);          //设置项目下的模块
                    projectInfo.setFromPage('project');     //设置来的页面
                    $state.go('slidebar.currentProject', {'projectDetail': projectDetail})
                } else {
                    alert(result.info);
                }
            })
        }
    }

    //删除项目
    $scope.deleteProject = function (id) {
        if ('' == id) {
            return;
        }
        params = angular.extend({'opr': 'prodelete'}, {'id': id});

        promise(params, url).then(function (result) {
            if (result.flag) {
                if (0 == result.data.status) {
                    var allProject = result.data.data;//更新所有项目
                    vm.projectInfo = allProject;
                    projectInfo.setAllProject(allProject);
                    $rootScope.$broadcast('updateCurrentName', {'itemName': vm.projectName.name});
                    $scope.msg = "项目删除成功！";
                    setStyle('itemAlert', 'itemIcon', true);
                    $timeout(function () {
                        $('#projectAlert').modal('hide');
                    }, 1000);
                } else {
                    $scope.msg = "项目删除失败！";
                    setStyle('itemAlert', 'itemIcon', false);
                    //angular.element(".alert").addClass("alert-danger");
                    //angular.element('.icon').addClass('glyphicon-ban-circle');
                    $timeout(function () {
                        $('#projectAlert').modal('hide');
                    }, 1000);
                }
            } else {
                alert(result.info);
            }
        })
    }

    //监听新增项目事件，更新下拉框
    $scope.$on('updateItem', function (e, data) {

        vm.projectInfo = data.detailData;
    })

}]);

/**
 * 切换提示样式
 * id_alert:弹框文字的id
 * id_icon:图标的id
 *
 */
function setStyle(id_alert, id_icon, flag) {
    if (flag) {
        document.getElementById(id_alert).className = "alert alert-success col-sm-8 icon-space fade in";
        document.getElementById(id_icon).className = "icon glyphicon glyphicon-ok-circle";
    } else {
        document.getElementById(id_alert).className = "alert alert-danger col-sm-8 icon-space fade in";
        document.getElementById(id_icon).className = "icon glyphicon glyphicon-ban-circle";
    }
}