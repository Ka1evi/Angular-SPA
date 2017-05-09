/**
 * Created by root on 2017/4/12.
 */

angularApp.register.controller('slidebarCtrl', ['$state','$stateParams', '$scope','projectInfo','promise','$q',function($state,$stateParams, $scope,projectInfo,promise,$q) {

    var projectId,   //当前项目的id
        modules,     //模块名
        allProject, //所有项目,数组形式，里面是json
 		username,//用户名
 		params, //请求参数
		url,    //请求url
		path;   //对应模块的路径
	var	nameArr=[];//要删除的模块名称，是数组
	var addressTemp=[];//存储邮箱地址的容器
    var username=projectInfo.getUserName();
    allProject=projectInfo.getAllProject();
    if(username!=null){
    	$scope.currentUser=username;
    }
    
    $scope.$on("$stateChangeSuccess",function(){
    	
    	//var fromPage=projectInfo.getFromPage();
    	//if( null != fromPage && 'project'==fromPage){ //当来的页面是project.html
    		console.log(projectInfo)
    		var currentName=projectInfo.getProjectName();
	        var modelId=projectInfo.getModelId();
	        modules=projectInfo.getModels();
	       
	        if(currentName !=null){
	            $scope.vm={
	                projectName:currentName
	            }
	        }
	        if(modelId != null){
	        	projectId=modelId;
	        }
	        if(modules != null){
	        	$scope.modules= modules;
	        }
    	//}
    });
    
   
   
    //新增项目
    
    $scope.addProject=function(){
    	
    	var projectName=angular.element('#inputProjectName').val();
    	var projectDesc=angular.element('#inputProjectInfo').val();
    	params=angular.extend({"opr" : "proadd"},{'user':username,'name':projectName,'desc':projectDesc});
    	path=env[env['get']]['project']; 
		url =path['project'];
    	
    	promise(params,url).then(function(result){
        	
        	if(result.flag){
        		if(0 == result.data.status){
        			allProject=result.data.data;//更新所有项目
        			projectInfo.setAllProject(allProject);
        		}else{
        			alert('新增项目失败');
        		}
        	}else{
        		alert(result.info);
        	}
        	angular.element('#addProjectLabel').find('input').val('');
        });
    }
    
    //新增模块
    
    $scope.addModule=function(){
    	
    	var moduleName=angular.element('#inputModelName').val();
    	
    	params=angular.extend({"opr" : "addmodel"},{'id':projectId,'addmodel':moduleName});
    	path=env[env['get']]['model']; 
		url =path['model'];
    	//url='http://127.0.0.1:5002/cgi-bin/model.do';
    	
    	promise(params,url).then(function(result){
        	
        	if(result.flag){
        		if(0 == result.data.status){
        			$scope.modules=result.data.model;
        			projectInfo.setModules($scope.modules); //更新项目中的模块
        		}else{
        			alert('新增模块失败');
        		}
        	}else{
        		alert(result.info);
        	}
        	angular.element('#addModelLabel').find('input').val('');
        });
    }
    
    
    $scope.toProject=function(){
    	console.log($scope.modules)
    	$state.go('slidebar.project',{'detailData':allProject});
    }

    //查看当前项目的结果信息
    $scope.toCurrentResult=function(){
        params=angular.extend({'opr':'proquery'},{'id':projectId});
        path=env[env['get']]['project']; //获取选择项目的路径
        url =path['project'];

        promise(params,url).then(function(result){
            if(result.flag){
                var projectDetail=result.data;
                console.log(projectDetail);
                $state.go('slidebar.currentProject',{'projectDetail':projectDetail})
            }else{
                alert(result.info);
            }
        })
    }

    $scope.toCase=function(){
    	//var modelName=angular.element('#case').text(); //获取项目下模块名称
    	var modelName='用例模版';
    	params=angular.extend({"opr" : "cmquery"},{'page':0,'pid':projectId});
    	path=env[env['get']]['case_model']; 
		url =path['case_model'];
    	//url='http://127.0.0.1:5002/cgi-bin/case_model.do';
    	
    	promise(params,url).then(function(result){
        	
        	if(result.flag){
        		console.log(result.data)
        		var data=result.data;
        		$state.go('slidebar.useCase',{'detailCase':data,'modelName':modelName,'pid':projectId});
        	}else{
        		alert(result.info);
        	}
        })
    }
     
    /**
     * 跳转相应模块
     *  参数：1、id:模块id
     *       2、name:模块名称
     */
    $scope.toModules=function(name){
    	
    	params=angular.extend({"opr" : "casequery"},{'pmodel':name,'pid':projectId,'page':0});
    	path=env[env['get']]['model']; 
		url =path['case'];
    	//url='http://127.0.0.1:5002/cgi-bin/case.do';
    	
    	
    	promise(params,url).then(function(result){
        	
        	if(result.flag){
        		console.log(result)
        		var data=result.data;
        		$state.go('slidebar.model',{'detailCase':data,'modelName':name,'pid':projectId});
        	}else{
        		alert(result.info);
        	}
        })
    	
    	
    }
    
    //删除模块
    
    $scope.delModule=function(name){
    	nameArr=[];
    	nameArr.push(name);
    }
    //确认删除模块
    $scope.ensure=function(){
    	params=angular.extend({"opr":'deletemodel'},{'id':projectId,'deletemodel':nameArr[0]});
    	path=env[env['get']]['model']; 
		url =path['model'];
    	//url='http://127.0.0.1:5002/cgi-bin/model.do';
    	
    	promise(params,url).then(function(result){
        	
        	if(result.flag){
        		if(0 == result.data.status){
        			$scope.modules=result.data.model;
        			projectInfo.setModules(result.data.model);
        		}else{
        			alert("删除失败");
        		}
        	}else{
        		alert(result.info);
        	}
        })
    }
    
    
    //定时任务
    $scope.timing=function(){
    	var times=angular.element("#time").val();
    	params=angular.extend({"opr":'setting'},{'timing':times});
    	path=env[env['get']]['setting']; 
		url =path['setting'];
    	//url="http://127.0.0.1:5002/cgi-bin/setting.do";
    	
    	promise(params,url).then(function(result){
        	if(result.flag){
        		if(0 == result.data.status){
        			alert("设置成功");
        		}else{
        			alert("设置失败");
        		}
        	}else{
        		alert(result.info);
        	}
        })
    }
    
    //设置发邮件时先查找所有的用户邮箱
    $scope.findFriend=function(){
    	params={'opr':'user_email'};
    	path=env[env['get']]['setting']; 
		url =path['setting'];
    	//url="http://127.0.0.1:5002/cgi-bin/setting.do";
    	
    	promise(params,url).then(function(result){
        	if(result.flag){
        		$scope.friendInfo=result.data.data;
        	}else{
        		alert(result.info);
        	}
        })
    }

    //勾选要发送的邮箱
    $scope.chooseEmail=function(name,address){
    	
    	var doc=document.getElementById(name);
    	var index=addressTemp.indexOf(address)
    	if(doc.checked==true && (index=-1 )){  //选中但没有找到,加入
    		addressTemp.push(address);
    	}else if(doc.checked==false && (index!=-1)){ //没有选择但找到，说明之前是选中的，删除
    		addressTemp.splice(index,1);
    	}
    	console.log(addressTemp)
    }
    
    //勾选邮箱完成
    $scope.sendEmail=function(){
    	params=angular.extend({'opr':'to_email_address'},{'user':username,'to_email':addressTemp});
    	path=env[env['get']]['setting']; 
		url =path['setting'];
    	//url="http://127.0.0.1:5002/cgi-bin/setting.do";

        //没有勾选直接返回
        if(addressTemp.length == 0) {
        	return;
        }
        
    	promise(params,url).then(function(result){
        	
        	if(result.flag){
        		if(0 == result.data.status){
        			alert("设置要发送邮件人员成功")
        		}else{
        			alert("设置要发送邮件人员失败");
        		}
        	}else{
        		alert(result.info);
        	}
        }).then(function(){
        	addressTemp=[];
        })
    }
    
    
    //exit
    $scope.exit = function () {
        $state.go('login');
        angular.element('.modal-backdrop').remove();//移除模态框遮罩层
    }
    
    
    
     //format time
    $('#time').timeDropper({format: "HH:mm", mousewheel: true, autoswitch: true});

    //settings bg
    $.backstretch("img/bg-white.jpg", {transitionDuration: 200});
    
    
    
}]);