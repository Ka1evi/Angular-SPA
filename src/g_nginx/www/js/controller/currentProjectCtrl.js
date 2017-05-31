/**
 * Created by root on 2017/4/12.
 */

angularApp.register.controller('currentProjectCtrl', ['$scope', 'projectInfo', '$stateParams', function ($scope, projectInfo, $stateParams) {
    var currentName = projectInfo.getProjectName();
    if (currentName != null) {
        $scope.vm = {
            projectName: currentName
        }
    }

    Chart.defaults.global.colors = [
        {
            backgroundColor: '#46BFBD',
            pointBackgroundColor: '#46BFBD',
        },
        {
            backgroundColor: 'rgba(247,70,74,1)',
            pointBackgroundColor: 'rgba(247,70,74,1)',
        }
    ]

    $scope.labels = ["测试成功次数", "测试失败次数"];

    var projectDetail = $stateParams.projectDetail;
    if (projectDetail) {
        var desc = projectDetail.desc;
        var success = projectDetail.suc_num;
        var fail = projectDetail.fail_num;

        $scope.data = [success, fail];
        $scope.options = {
            legend: {
                display: true,
                position: "right"
            }
        }
        $scope.desc = desc;
    }

}]);
