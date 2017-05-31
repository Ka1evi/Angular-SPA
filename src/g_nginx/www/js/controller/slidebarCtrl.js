/**
 * Created by root on 2017/4/12.
 */

angularApp.register.controller('slidebarCtrl', ['$state', '$stateParams', '$scope', 'projectInfo', 'promise', '$q', '$timeout', '$rootScope', function ($state, $stateParams, $scope, projectInfo, promise, $q, $timeout, $rootScope) {

    var projectId,   //当前项目的id
        modules,     //模块名
        allProject, //所有项目,数组形式，里面是json
        username,//用户名
        currentName,//当前项目名称
        params, //请求参数
        url,    //请求url
        path;   //对应模块的路径
    var nameArr = [];//要删除的模块名称，是数组
    var addressTemp = [];//存储邮箱地址的容器
    var username = projectInfo.getUserName();
    allProject = projectInfo.getAllProject();
    if (username != null) {
        $scope.currentUser = username;
    }

    $scope.$on("$stateChangeSuccess", function () {

        //var fromPage=projectInfo.getFromPage();
        //if( null != fromPage && 'project'==fromPage){ //当来的页面是project.html
        console.log(projectInfo)
        currentName = projectInfo.getProjectName();
        var modelId = projectInfo.getModelId();
        modules = projectInfo.getModels();

        if (currentName != null) {
            $scope.vm = {
                projectName: currentName
            }
        }
        if (modelId != null) {
            projectId = modelId;
        }
        if (modules != null) {
            $scope.modules = modules;
        }
        //}
    });

    //查看当前项目的结果信息
    $scope.toCurrentResult = function () {

        if (!currentName) {
            return;
        }

        params = angular.extend({'opr': 'proquery'}, {'id': projectId});
        path = env[env['get']]['project']; //获取选择项目的路径
        url = path['project'];

        promise(params, url).then(function (result) {
            if (result.flag) {
                var projectDetail = result.data;
                console.log(projectDetail);
                $state.go('slidebar.currentProject', {'projectDetail': projectDetail})
            } else {
                alert(result.info);
            }
        })
    }

    //新增项目
    $scope.addItem = function () {

        var projectName = angular.element('#inputProjectName').val();
        var projectDesc = angular.element('#inputProjectInfo').val();
        params = angular.extend({"opr": "proadd"}, {'user': username, 'name': projectName, 'desc': projectDesc});
        path = env[env['get']]['project'];
        url = path['project'];

        promise(params, url).then(function (result) {

            if (result.flag) {
                if (0 == result.data.status) {
                    allProject = result.data.data;//更新所有项目
                    projectInfo.setAllProject(allProject);
                    $rootScope.$broadcast('updateItem', {'detailData': allProject});//向下广播项目已经更新，以便更新project.html页面的项目下拉框
                    setStyle('slidebarAlert', 'slidebarIcon', '#alertInfo', true, $scope, "新增项目成功！");
                } else {
                    setStyle('slidebarAlert', 'slidebarIcon', '#alertInfo', false, $scope, "新增项目失败！");
                }
            } else {
                alert(result.info);
            }
            //清空新增项目的表单数据
            $scope.name = '';
            $scope.desc = '';

            //重置新增项目的表单验证状态
            $scope.addProject.$setPristine();
        });
    }

    $scope.resetProject = function () {

        //清空新增项目的表单数据
        $scope.name = '';
        $scope.desc = '';

        //重置新增项目的表单验证状态
        $scope.addProject.$setPristine();
    }

    //新增模块
    $scope.addModule = function () {

        if (!currentName) {
            setStyle('slidebarAlert', 'slidebarIcon', '#alertInfo', false, $scope, "请选择项目！");

            setTimeout(function () {
                //清空新增模块的表单数据
                $scope.inputModelName = '';
                $scope.inputProjectInfo = '';
                //重置新增模块的表单验证状态
                $scope.addModel.$setPristine();
            },1500)
            return;
        }

        var moduleName = angular.element('#inputModelName').val();

        params = angular.extend({"opr": "addmodel"}, {'id': projectId, 'addmodel': moduleName});
        path = env[env['get']]['model'];
        url = path['model'];
        //url='http://127.0.0.1:5002/cgi-bin/model.do';

        promise(params, url).then(function (result) {

            if (result.flag) {
                if (0 == result.data.status) {
                    $scope.modules = result.data.model;
                    projectInfo.setModules($scope.modules); //更新项目中的模块
                    setStyle('slidebarAlert', 'slidebarIcon', '#alertInfo', true, $scope, "新增模块成功！");
                } else {
                    setStyle('slidebarAlert', 'slidebarIcon', '#alertInfo', false, $scope, "新增模块失败！");
                }
            } else {
                alert(result.info);
            }

            //清空新增模块的表单数据
            $scope.inputModelName = '';
            $scope.inputProjectInfo = '';

            //重置新增模块的表单验证状态
            $scope.addModel.$setPristine();
        });
    }

    $scope.resetModel = function () {

        //清空新增模块的表单数据
        $scope.inputModelName = '';
        $scope.inputProjectInfo = '';

        //重置新增模块的表单验证状态
        $scope.addModel.$setPristine();
    }

    $scope.toProject = function () {
        allProject = projectInfo.getAllProject();
        $state.go('slidebar.project', {'detailData': allProject});
    }

    $scope.toCase = function () {
        //var modelName=angular.element('#case').text(); //获取项目下模块名称
        var modelName = '用例模版';
        params = angular.extend({"opr": "cmquery"}, {'page': 0, 'pid': projectId});
        path = env[env['get']]['case_model'];
        url = path['case_model'];
        //url='http://127.0.0.1:5002/cgi-bin/case_model.do';

        promise(params, url).then(function (result) {

            if (result.flag) {
                console.log(result.data)
                var data = result.data;
                $state.go('slidebar.useCase', {'detailCase': data, 'modelName': modelName, 'pid': projectId});
            } else {
                alert(result.info);
            }
        })
    }

    /**
     * 跳转相应模块
     *  参数：1、id:模块id
     *       2、name:模块名称
     */
    $scope.toModules = function (name) {

        params = angular.extend({"opr": "casequery"}, {'pmodel': name, 'pid': projectId, 'page': 0});
        path = env[env['get']]['model'];
        url = path['case'];
        //url='http://127.0.0.1:5002/cgi-bin/case.do';


        promise(params, url).then(function (result) {

            if (result.flag) {
                console.log(result)
                var data = result.data;
                $state.go('slidebar.model', {'detailCase': data, 'modelName': name, 'pid': projectId});
            } else {
                alert(result.info);
            }
        })


    }

    //删除模块
    $scope.delModule = function (name) {
        nameArr = [];
        nameArr.push(name);
    }

    //确认删除模块
    $scope.ensure = function () {
        params = angular.extend({"opr": 'deletemodel'}, {'id': projectId, 'deletemodel': nameArr[0]});
        path = env[env['get']]['model'];
        url = path['model'];
        //url='http://127.0.0.1:5002/cgi-bin/model.do';

        promise(params, url).then(function (result) {

            if (result.flag) {
                if (0 == result.data.status) {
                    $scope.toCase(); //删除模块后，默认显示用例模版页面
                    //angular.element('#focusCase').trigger('click');
                    $scope.modules = result.data.model;
                    projectInfo.setModules(result.data.model);
                    setStyle('slidebarAlert', 'slidebarIcon', '#alertInfo', true, $scope, "删除模块成功！");
                } else {
                    setStyle('slidebarAlert', 'slidebarIcon', '#alertInfo', false, $scope, "删除模块失败！");
                }
            } else {
                alert(result.info);
            }
        })
    }

    //定时任务
    $scope.timing = function () {
        var times = angular.element("#time").val();
        params = angular.extend({"opr": 'setting'}, {'timing': times});
        path = env[env['get']]['setting'];
        url = path['setting'];
        //url="http://127.0.0.1:5002/cgi-bin/setting.do";

        promise(params, url).then(function (result) {

            if (result.flag) {
                if (0 == result.data.status) {
                    setStyle('slidebarAlert', 'slidebarIcon', '#alertInfo', true, $scope, "定时任务设置成功！");
                } else {
                    setStyle('slidebarAlert', 'slidebarIcon', '#alertInfo', false, $scope, "定时任务设置失败！");
                }
            } else {
                alert(result.info);
            }
        })
    }

    //设置发邮件时先查找所有的用户邮箱
    $scope.findFriend = function () {

        params = {'opr': 'user_email'};
        path = env[env['get']]['setting'];
        url = path['setting'];
        //url="http://127.0.0.1:5002/cgi-bin/setting.do";

        promise(params, url).then(function (result) {
            if (result.flag) {
                $scope.friendInfo = result.data.data;
            } else {
                alert(result.info);
            }
        })
    }

    //勾选要发送的邮箱
    $scope.friendCount = 0;

    $scope.chooseEmail = function (name, address) {

        var doc = document.getElementById(name);
        var index = addressTemp.indexOf(address)
        if (doc.checked == true && (index = -1)) {  //选中但没有找到,加入
            $scope.friendCount--;
            addressTemp.push(address);
        } else if (doc.checked == false && (index != -1)) { //没有选择但找到，说明之前是选中的，删除
            $scope.friendCount++;
            addressTemp.splice(index, 1);
        }
        console.log(addressTemp);
    }

    //勾选邮箱完成
    $scope.sendEmail = function () {
        params = angular.extend({'opr': 'to_email_address'}, {'user': username, 'to_email': addressTemp});
        path = env[env['get']]['setting'];
        url = path['setting'];
        //url="http://127.0.0.1:5002/cgi-bin/setting.do";

        //没有勾选直接返回
        if (addressTemp.length == 0) {
            return;
        }

        promise(params, url).then(function (result) {

            if (result.flag) {
                if (0 == result.data.status) {
                    setStyle('slidebarAlert', 'slidebarIcon', '#alertInfo', true, $scope, "设置收件人成功！");
                } else {
                    setStyle('slidebarAlert', 'slidebarIcon', '#alertInfo', false, $scope, "设置收件人失败！");
                }
            } else {
                alert(result.info);
            }
        }).then(function () {
            addressTemp = [];

            //清空新增模块的表单数据
            $scope.friendCount = '';

            //重置新增模块的表单验证状态
            $scope.setMail.$setPristine();
        })
    }

    $scope.resetMail = function () {

        //清空新增项目的表单数据
        $scope.friendCount = '';

        //重置新增项目的表单验证状态
        $scope.setMail.$setPristine();
    }

    //exit
    $scope.exit = function () {

        // 退出清空projectInfo服务的数据，防止退出再登陆时数据还存在

        var projectInfoKey = Object.keys(projectInfo)
        for (var attr in Object.keys(projectInfo)) {
            var key = projectInfoKey[attr]
            var fn = projectInfo[key]
            if (key.includes('set')) {
                fn("");
            }
        }

        $state.go('login');
        // angular.element('.modal-backdrop').remove();//移除模态框遮罩层
    }

    //format time
    $('#time').timeDropper({format: "HH:mm", mousewheel: true, autoswitch: true});

    //settings bg
    $.backstretch("img/bg-white.jpg", {transitionDuration: 200});

    //监听项目删除事件，当删除项目时更新当前项目下拉框的信息
    $scope.$on('updateCurrentName', function (e, data) {

        var delProjectName = data.itemName;
        if (delProjectName == currentName) {
            projectInfo.setProjectName("");
            $scope.modules = {};
            $scope.vm = {
                projectName: ""
            };
            currentName = ""
        }
    })

}]);