/**
 * Created by root on 2017/4/12.
 */

angularApp.register.controller('useCaseCtrl', ['$scope', '$http', 'projectInfo', '$stateParams', 'paging', 'promise', 'formSerialization', 'upload','$timeout', function ($scope, $http, projectInfo, $stateParams, paging, promise, formSerialization, upload,$timeout) {

    var currentName = projectInfo.getProjectName();
    if (currentName != null) {
        $scope.vm = {
            projectName: currentName
        }
    }

    if (!$stateParams.detailCase) {
        return;
    }
    var modelName = $stateParams.modelName; //获取模块名称
    var infoPart = $stateParams.detailCase.data;  //获取第一页模版数据
    var total = $stateParams.detailCase.total; //获取模版总数
    var projectId = $stateParams.pid;//当前项目id
    var username = projectInfo.getUserName();
    var idTemp = [];//用户改变页码前先保存当页选中的模版id
    $scope.operation = {};//是新增还是编辑
    $scope.case = {};   //编辑时回显数据用

    //初始化请求方法
    $scope.caseMethod = ['GET', 'POST'];
    $scope.met = 'GET';
    $scope.num = 0;  //初始化序号
    var path = env[env['get']]['case_model'];
    var url = path['case_model'];
    //var url='http://127.0.0.1:5002/cgi-bin/case_model.do';
    var paramsPaging = {'opr': 'cmquery', 'pid': projectId}; //分页所需的参数
    var params; //查询模版数据需要的参数
    var editorId;//编辑的模版id
    var form = document.getElementById('useCaseForm');//获取表单对象
    //文件上传路径
    var up_url = path['upload'];
    //文件导出路径
    var down_url = path['download'];
    var down_address = 'C:/downCase/';//导出路径

    $scope.hidden = false;

    $scope.total = total;
    console.log(projectId)
    paging(infoPart, 8, $scope, total, idTemp, url, paramsPaging); //一进入就开始分页

    //点击新增，先清空表单数据
    $scope.clearData = function () {

        $scope.case = {};//清空表单数据
        $scope.met = 'GET';
        $scope.useCaseForm.$setPristine();//重置表单验证状态
        console.log($scope.hidden)
        $scope.hidden = true;
        $scope.operation = '新增';//默认是新增模版
        //清空表单数据
        //angular.element('#useCaseForm').find('input').val('');
    }


    //新增、编辑模板后保存
    $scope.addTemplate = function (operator) {


        $scope.case = {};//清空表单数据
        $scope.met = 'GET';

        $scope.useCaseForm.$setPristine();//重置表单验证状态

        $scope.operation = '新增';

        var formData = formSerialization('useCaseForm');//获取表格数据
        //	var url='http://127.0.0.1:5000/cgi-bin/case_model.do';

        if ('新增' == operator) {
            params = angular.extend(formData, {'opr': 'cmadd'}, {'pid': projectId});
        } else if ('编辑' == operator) {
            params = angular.extend(formData, {'opr': 'cmupdate'}, {'pid': projectId, 'id': editorId});
        }

        promise(params, url).then(function (result) {

            if (result.flag) {
                if (0 == result.data.status) {
                    console.log(result)
                    infoPart = result.data.data;
                    $scope.total = result.data.total;
                    total = $scope.total;
                    paging(infoPart, 8, $scope, total, idTemp, url, paramsPaging);
                    $scope.msg = "新增成功！";
                    setStyle('useCaseAlert','useCaseIcon',true);
                    $timeout(function () {
                        $('#useCaseTips').modal('hide');
                    }, 1000);
                } else {
                    $scope.msg = "新增失败！";
                    //$scope.useCaseTips=true;
                    setStyle('useCaseAlert','useCaseIcon',false);
                    //angular.element('.alert').addClass('alert-danger');
                    //angular.element('.icon').addClass('glyphicon-ban-circle');
                    $timeout(function () {
                        $('#useCaseTips').modal('hide');
                    }, 1000);
                }

            } else {
                alert(result.info);
            }
        }).then(function (res) {

            //$scope.useCaseForm.$dirty
            $scope.case = {};//清空表单数据
            $scope.met = 'GET';

            $scope.useCaseForm.$setPristine();//重置表单验证状态
            $scope.hidden = false;  //新增、编辑之后隐藏表格
        })
    }

    //关闭表单模态框
    $scope.toReset = function () {

        //重置表单验证状态
        $scope.useCaseForm.$setPristine();
        //清空表单数据
        $scope.case = {};//清空表单数据
        $scope.met = 'GET';
    }


    //批量删除,获取勾选的序号对应的id
    $scope.del = function (id) {
        var doc = document.getElementById(id);
        var index = idTemp.indexOf(id)
        if (doc.checked == true && (index = -1 )) {  //选中但没有找到,加入
            idTemp.push(id);
        } else if (doc.checked == false && (index != -1)) { //没有选择但找到，说明之前是选中的，删除
            idTemp.splice(index, 1);
        }
    }

    //开始删除
    $scope.delete = function (id) {

        if (arguments.length == 1) {   //单个删除
            params = angular.extend({'opr': 'cmdelete'}, {'pid': projectId, 'id': id});
        } else if (arguments.length == 0) {  //批量删除
            params = angular.extend({'opr': 'cmdelete'}, {'pid': projectId, 'id': idTemp});
        }
        promise(params, url).then(function (result) {

            if (result.flag) {
                if (0 == result.data.status) {
                    infoPart = result.data.data; //重新获取的数据
                    total = result.data.total;
                    $scope.total = total;
                    idTemp = [];  //删除之后置为空
                    //刷新页面,重新判断勾选
                    $scope.isSelected = function (id) {
                        return idTemp.indexOf(id) != -1;
                    }
                    paging(infoPart, 8, $scope, total, idTemp, url, paramsPaging);
                } else {
                    $scope.msg = "删除失败！";
                    setStyle('useCaseAlert','useCaseIcon',false);
                    //angular.element('.alert').addClass('alert-danger');
                    //angular.element('.icon').addClass('glyphicon-ban-circle');
                    $timeout(function () {
                        $('#useCaseTips').modal('hide');
                    }, 1000);
                }

            } else {
                alert(result.info);
            }
        })
    }


    //根据模版名称模糊查询
    $scope.focus = function (text) {
        params = angular.extend({'opr': 'cmquery_by_name'}, {'pid': projectId, 'name': text, 'page': 0});
        //url='http://127.0.0.1:5000/cgi-bin/case_model.do';
        console.log(text)
        promise(params, url).then(function (result) {

            if (result.flag) {
                console.log(result)
                infoPart = result.data.data; //重新获取的数据
                total = result.data.total;
                $scope.total = total;
                idTemp = [];  //删除之后置为空
                //刷新页面,重新判断勾选
                $scope.isSelected = function (id) {
                    return idTemp.indexOf(id) != -1;
                }

                paging(infoPart, 8, $scope, total, idTemp, url, params);
            } else {
                alert(result.info);
            }
        })
    }

    //编辑用例
    $scope.editor = function (id) {

        $scope.operation = '编辑';
        //$scope.editor=true;
        $scope.hidden = true;
        //清空表单数据
        $scope.case = {};//清空表单数据
        $scope.met = 'GET';

        editorId = id;
        //先回显用例信息
        params = angular.extend({'opr': 'cmquery_by_id'}, {'id': id});

        promise(params, url).then(function (result) {


            if (result.flag) {
                console.log(result)
                /*var attrTemp=[];
                 attrTemp[0]=result.data.data;
                 $scope.cases=attrTemp;
                 $scope.met=result.data.data.method;*/

                $scope.case = result.data.data;
                $scope.met = result.data.data.method;
            } else {
                alert(result.info);
            }
        })
    }


    /*++++++++++++++  拖拽上传 +++++++++++++++++++++++*/

    var formData2 = new FormData();
    formData2.append("pid", projectId);
    formData2.append("pmodel", modelName);
    formData2.append("user", username);
    formData2.append("opr", 'upload');
    formData2.append("typ", 0)
    upload(up_url, formData2, $scope, idTemp, paramsPaging, url);
    /*++++++++++++++++++++++++++++++++++++++++++++++++++++++*/

    //关闭上传
    $scope.closeUp = function () {
        var others = document.getElementById('count');
        var canvas = document.querySelector('canvas');
        var context = canvas.getContext('2d');
        others.innerText = 0;
        context.clearRect(0, 0, 500, 20);
    }


    //导入文件
    /*
     $scope.upload=function(){

     var file=angular.element('#InputFile').get(0).files[0];

     var formData=new FormData();

     formData.append("pid",projectId);
     formData.append("pmodel",modelName);
     formData.append("user",username);
     formData.append("opr",'upload');
     formData.append("file",file);

     $http({
     url:up_url,
     headers: {
     'Content-Type': undefined
     },
     method:'post',
     data:formData

     }).then(function(res){

     var respond=res.data;
     if("success" == respond.msg){
     var results=respond.data;
     $scope.total=results.count;
     total=results.count;
     infoPart=results.list;
     paging(infoPart,8,$scope,total,idTemp,url,paramsPaging);
     }else{
     alert("上传失败");
     }

     }).catch(function(e){

     })

     }
     */

    //导出到文件
    $scope.download = function () {

        if (0 == idTemp.length) {
            return;
        }

        params = angular.extend({'opr': 'caseout'}, {'typ': 0, 'address': down_address, 'id': idTemp});

        promise(params, down_url).then(function (result) {


            if (result.flag) {
                var downloadFile = result.data;
                if (0 == downloadFile.status) {
                    var file_address = downloadFile.address + downloadFile.filename;
                    alert("文件导出成功,保存在:" + file_address);
                }

            } else {
                alert(result.info);
            }
        })
    }
}]);

/**
 * 切换提示样式
 * id_alert:弹框文字的id
 * id_icon:图标的id
 *
 */
function setStyle(id_alert,id_icon,flag) {
    if(flag){
        document.getElementById(id_alert).className = "alert alert-success col-sm-8 icon-space fade in";
        document.getElementById(id_icon).className = "icon glyphicon glyphicon-ok-circle";
    }else{
        document.getElementById(id_alert).className = "alert alert-danger col-sm-8 icon-space fade in";
        document.getElementById(id_icon).className = "icon glyphicon glyphicon-ban-circle";
    }
}