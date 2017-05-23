/**
 * Created by root on 2017/4/12.
 */

angularApp.register.controller('modelCtrl', ['$scope', '$http', 'projectInfo','$stateParams','paging','promise','formSerialization','$timeout', function($scope, $http, projectInfo,$stateParams,paging,promise,formSerialization,$timeout) {

    var currentName = projectInfo.getProjectName();
    if(currentName != null) {
        $scope.vm = {
            projectName: currentName
        }
    }
    var username=projectInfo.getUserName();  //获取用户名result

    if(!$stateParams.detailCase){
        return;
    }
    var modelName=$stateParams.modelName; //获取模块名称
    var infoPart=$stateParams.detailCase.data;  //获取第一页模版数据
    var pageInfo=angular.fromJson(angular.toJson(infoPart));//实现数组的深拷贝,slice/concat方法不能实现深拷贝

    var total=$stateParams.detailCase.total; //获取模版总数
    var projectId=$stateParams.pid;//当前项目id
    var idTemp=[];//用户改变页码前先保存当页选中的模版id
    var path=env[env['get']]['model'];
    var	url =path['case'];
    var url_2=path['result'];
    //var url='http://127.0.0.1:5002/cgi-bin/case.do';  //对用例进行操作、查询用的url
    //var url_2='http://127.0.0.1:5002/cgi-bin/result.do';//执行用例的url
    var paramsPaging={'opr':'casequery','pid':projectId,'pmodel':modelName}; //分页所需的参数
    var params; //查询模版数据需要的参数
    var editorId;//编辑的模版id
    var form=document.getElementById('modelForm');//获取表单
    $scope.cp = $scope;//重新赋值作用域
    $scope.modelName=modelName;
    $scope.num=0;  //初始化序号
    $scope.hidden=false;

    //初始化用例级别
    $scope.rk='BVT用例';
    $scope.caseRank=['BVT用例','xx用例'];

    //初始化用例类型
    $scope.mType='用例模板';
    $scope.caseType=['用例模板','自定义用例'];

    //初始化请求方法
    $scope.met='GET';
    $scope.caseMethod=['GET','POST'];


    //初始化加密
    $scope.enc='NO';
    $scope.caseEncrypt=['YES','NO'];

    //初始化定时
    $scope.tim='NO';
    $scope.caseTiming=['YES','NO']

    //初始化操作下拉框
    $scope.trs=['用例名称','用例级别','请求数据','检查点','用例详情','定时任务','主机IP','请求URL','请求方法','请求类型'];
    $scope.theads=[
        {'eg':'timing','tname':'定时任务'},
        {'eg':'rank','tname':'用例级别'},
        {'eg':'ip','tname':'主机IP'},
        {'eg':'url','tname':'请求URL'},
        {'eg':'method','tname':'请求方法'},
        {'eg':'type','tname':'请求类型'}
    ]
    //确定刚进入页面要过滤掉的数据
    $scope.tbodyFilter=['用例级别','定时任务','主机IP','请求URL','请求方法','请求类型'];//要过滤掉的表头
    $scope.dataFilter=['rank','timing','ip','url','method','type'];    //要过滤的数据的key

    $scope.total=total;
    paging(infoPart,8,$scope,total,idTemp,url,paramsPaging,pageInfo); //一进入就开始分页

    console.log(pageInfo)

    //清空并重置表单
    function clearAndReset(){

        $scope.modelForm.$setPristine();//重置表单验证状态
        $scope.module={};//清空表单数据
        $scope.rk='BVT用例';
        $scope.enc='NO';
        $scope.tim='NO';
        $scope.cp.mType='用例模板';
        $scope.model={
            id:''
        }
    }

    //点击新增，查询所有用例模版信息
    $scope.getModel=function(){

        $scope.operation='新增';//默认是新增模版
        $scope.hidden=true;
        $scope.bar=false;
        $scope.toEdit=false;
        clearAndReset();

        console.log($scope.mType)

        params=angular.extend({'opr':'cmquery_id_name'},{'pid':projectId})
        var path1=env[env['get']]['case_model'];
        var url_1=path1['case_model'];

        promise(params,url_1).then(function(result){
            if(result.flag){
                console.log(result)
                $scope.caseModel=result.data.data;
            }else{
                alert(result.info);
            }
        })

    }

    //关闭表单模态框
    $scope.toReset = function () {

        $scope.hidden=false;
        $scope.mType='';
        clearAndReset();
        $scope.cp.mType='用例模板';
    }

    //新增、编辑用例后保存
    $scope.addTemplate=function(operator){

        clearAndReset();
        var formData=formSerialization('modelForm');//获取表格数据
        var modelId=angular.element('#modelId').text(); //获取模版的id
        formData['cmid']=modelId;

        if($scope.caseModel.length == 0 && (formData['selectModelType'] !='自定义用例')){
            $scope.msg = "无用例模板，请选择自定义用例！";
            //$scope.modelTips=true;
            setStyle('modelAlert','modelIcon',false);
            $timeout(function(){
                $('#modelTips').modal('hide');
            },2000)
            //angular.element('.alert').addClass('alert-danger');
            //angular.element('.icon').addClass('glyphicon-ban-circle');
            return;
        }

        if('新增' == operator){
            params=angular.extend(formData,{'opr':'caseadd','pid':projectId,'pmodel':modelName,'user':username});

            //新增时，需要判断当用例类型选择了模版类型时用户是否选择了模版
            if((formData['selectModelType'] =='用例模板') && modelId == ""){
                $scope.msg = "请选择模板！";
                setStyle('modelAlert','modelIcon',false)
                //angular.element('.alert').addClass('alert-danger');
                //angular.element('.icon').addClass('glyphicon-ban-circle');
                $timeout(function () {
                    $('#modelTips').modal('hide');
                }, 1000);
                return;
            }

        }else if('编辑' == operator){
            params=angular.extend(formData,{'opr':'caseupdate'},{'pid':projectId,'id':editorId,'pmodel':modelName,'user':username});
        }

        promise(params,url).then(function(result){

            if(result.flag){
                if(0 == result.data.status){
                    $scope.msg = "操作成功!";
                    setStyle('modelAlert','modelIcon',true)
                    $timeout(function(){
                        $('#modelTips').modal('hide');
                    },1000)
                    infoPart=result.data.data;
                    pageInfo=angular.fromJson(angular.toJson(infoPart));
                    total=result.data.total;
                    $scope.total=total;
                    paging(infoPart,8,$scope,total,idTemp,url,paramsPaging,pageInfo);
                }else{
                    $scope.msg = "操作失败！";
                    //$scope.modelTips=true;
                    setStyle('modelAlert','modelIcon',false)
                    //angular.element('.alert').addClass('alert-danger');
                    //angular.element('.icon').addClass('glyphicon-ban-circle');
                    $timeout(function () {
                        $('#modelTips').modal('hide');
                    }, 1000);
                }
            }else{
                alert(result.info);
            }
        }).then(function(res){

            clearAndReset();
            $scope.hidden=false;  //新增、编辑之后隐藏表格

        })
    }


    //批量删除,获取勾选的序号对应的id
    $scope.del=function(id){
        var doc=document.getElementById(id);
        var index=idTemp.indexOf(id)
        if(doc.checked==true && (index=-1 )){  //选中但没有找到
            idTemp.push(id);
        }else if(doc.checked==false && (index!=-1)){ //没有选择但找到，说明之前是选中的
            idTemp.splice(index,1);
        }
    }

    //开始删除
    $scope.delete=function(id){

        if(arguments.length == 1){   //单个删除
            params=angular.extend({'opr':'casedelete'},{'pid':projectId,'id':id,'pmodel':modelName});
        }else if(arguments.length ==0){  //批量删除
            params=angular.extend({'opr':'casedelete'},{'pid':projectId,'id':idTemp,'pmodel':modelName});
        }
        promise(params,url).then(function(result){

            if(result.flag){
                if(0 == result.data.status){
                    infoPart=result.data.data; //重新获取的数据
                    pageInfo=angular.fromJson(angular.toJson(infoPart));
                    total=result.data.total;
                    $scope.total=total;
                    idTemp=[];  //删除之后置为空
                    //刷新页面,重新判断勾选
                    $scope.isSelected = function(id) {
                        return idTemp.indexOf(id) != -1;
                    }
                    paging(infoPart,8,$scope,total,idTemp,url,paramsPaging,pageInfo);
                }else{
                    $scope.msg = "删除失败！";
                    //$scope.modelTips=true;
                    setStyle('modelAlert','modelIcon',false);
                    //angular.element('.alert').addClass('alert-danger');
                    //angular.element('.icon').addClass('glyphicon-ban-circle');
                    $timeout(function () {
                        $('#modelTips').modal('hide');
                    }, 1000);
                }

            }else{
                alert(result.info);
            }
        })
    }

    //根据模版名称模糊查询
    $scope.focus=function(text){
        params=angular.extend({'opr':'casequery_by_name'},{'pid':projectId,'name':text,'pmodel':modelName,'page':0});
        console.log(text)
        promise(params,url).then(function(result){

            if(result.flag){
                console.log(result)
                infoPart=result.data.data; //重新获取的数据
                pageInfo=angular.fromJson(angular.toJson(infoPart));
                total=result.data.total;
                $scope.total=total;
                idTemp=[];  //删除之后置为空
                //刷新页面,重新判断勾选
                $scope.isSelected = function(id) {
                    return idTemp.indexOf(id) != -1;
                }
                paging(infoPart,8,$scope,total,idTemp,url,params,pageInfo);
            }else{
                alert(result.info);
            }
        })
    }

    //编辑
    $scope.editor=function(id){

        clearAndReset();
        $scope.operation='编辑';
        $scope.toEdit=true; //编辑时不显示用例类型
        $scope.hidden=true;
        editorId=id;
        //先回显用例信息
        params=angular.extend({'opr':'casequery_by_id'},{'id':id});

        promise(params,url).then(function(result){
            $scope.bar=true;

            $scope.module=result.data.data
            $scope.rk=result.data.data.rank;
            $scope.met=result.data.data.method;
            $scope.enc=result.data.data.encrypt;
            $scope.tim=result.data.data.timing;
            $scope.module.check=angular.toJson($scope.module.check);
            $scope.module.data=angular.toJson($scope.module.data)
        })
    };


    //选中的要显示的表头
    $scope.updateSelection=function($event,id){

        var doc=document.getElementById(id);
        var index=$scope.dataFilter.indexOf(id)
        var name = $event.target.name;

        //console.log(pageInfo);
        $scope.trs=['用例名称','用例级别','请求数据','检查点','用例详情','定时任务','主机IP','请求URL','请求方法','请求类型'];
        var tempInfo=angular.fromJson(angular.toJson(pageInfo));//实现数组的深拷贝,slice/concat方法不能实现深拷贝
        //console.log(tempInfo);
        $scope.showInfo=tempInfo;

        if(doc.checked==true && (index!=-1 )){  //第一次被选中

            $scope.dataFilter.splice(index,1);
            $scope.tbodyFilter.splice(index,1);

        }else if(doc.checked==false && (index ==-1)){ //没有选择但找到，说明之前是选中的，删除
            $scope.dataFilter.push(id);
            $scope.tbodyFilter.push(name)

        }
        //console.log('dataFilter:'+$scope.dataFilter);
        //console.log('tbodyFilter:'+$scope.tbodyFilter);
    };


    $scope.change = function(cType) {
        console.log(cType)
        if('自定义用例' == cType){
            $scope.bar=true;
        }else{
            $scope.bar=false;
        }
    }

    //单个执行
    $scope.execute=function(id){
        $scope.singleComplete=false;
        params=angular.extend({'opr':'execute'},{'pid':projectId,'user':username,'id':id});

        var singleArr=[];

        promise(params,url_2).then(function(result){

            if(result.flag){
                try{
                    var respond=result.data;
                    if(1 == result.data.status){
                        alert('用例执行失败');
                        return;
                    }else if(0 == result.data.status){
                        $scope.singleInfo="用例执行成功，邮件发送成功";
                    }else if(2 == result.data.status){
                        $scope.singleInfo="用例执行成功，邮件发送失败";
                    }
                    singleArr[0]=respond.data;
                    $scope.singleResult=singleArr;
                    $scope.singleComplete=true;
                }catch(e){
                    angular.element('.modal-backdrop').remove();//移除模态框遮罩层
                    alert("后台数据可能出错，请查看相关日志")
                }

            }else{
                alert(result.info);
            }
        })

    }


    //批量执行
    $scope.executeBatch=function($event){

        if($scope.total == 0){
            $event.preventDefault();
            $event.stopPropagation();
            return;
        }

        params=angular.extend({'opr':'executeall'},{'pid':projectId,'user':username,'model':modelName});
        $scope.batchComplete=false;
        var successArr=[];
        var failArr=[];

        promise(params,url_2).then(function(result){

            if(result.flag){
                try{
                    var respond=result.data.data;

                    if(1 == result.data.status){
                        alert('用例执行失败')
                        return;
                    }else if(0 == result.data.status){
                        $scope.batchResult="用例执行成功，邮件发送成功";
                    }else if(2 == result.data.status){
                        $scope.batchResult='用例执行成功，邮件发送失败';
                    }
                    successArr=respond.success_list;
                    $scope.success_list=successArr;
                    failArr=respond.fail_list;
                    $scope.fail_list=failArr;
                    $scope.success_num=respond.success_num;
                    $scope.fail_num=respond.fail_num;
                    $scope.batchComplete=true;
                }catch(e){
                    angular.element('.modal-backdrop').remove();//移除模态框遮罩层
                    alert("后台数据可能出错，请查看相关日志")
                }

            }else{
                alert(result.info);
            }
        });
    }

    //查询执行记录
    $scope.record=function(id){

        params=angular.extend({'opr':'caseresult'},{'id':id})
        $scope.historyComplete=false;

        promise(params,url_2).then(function(result){

            if(result.flag){
                try{
                    $scope.singleHistory=result.data.data;
                    $scope.historyComplete=true;
                }catch(e){
                    angular.element('.modal-backdrop').remove();//移除模态框遮罩层
                    alert("后台数据可能出错，请查看相关日志")
                }
            }else{
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