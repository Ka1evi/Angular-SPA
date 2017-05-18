/**
 * Created by root on 2017/4/12.
 */
'use strict';

/*
 * 配置项目路由，同时异步加载所需的js文件
 */

angularApp.config(['$stateProvider','$urlRouterProvider','$locationProvider',function ($stateProvider, $urlRouterProvider,$locationProvider) {
    $stateProvider
        .state('login',{
            url:'/login',
            templateUrl: 'templates/login.html',
            resolve: {
                load: angularApp.asyncjs(['js/controller/loginCtrl.js','js/jquery/jquery.backstretch.js','js/service/projectInfo.js','js/service/promise.js','js/directive/validate.js'])
            }
        })
        .state('slidebar',{
            url:'/slidebar',
            templateUrl: 'templates/slidebar.html',
            resolve: {
                load: angularApp.asyncjs(['js/controller/slidebarCtrl.js', 'js/util/timedropper.min.js', 'js/jquery/jquery.backstretch.js', 'js/service/projectInfo.js','js/service/promise.js'])
            },
            params:{detailData:null,username:null}
        })

        .state('slidebar.project',{
            url:'/project',
            templateUrl: 'templates/project.html',
            resolve: {
                load: angularApp.asyncjs(['js/controller/projectCtrl.js','js/service/projectInfo.js','js/service/promise.js'])
            },
            params:{detailData:null}
        })

        .state('slidebar.currentProject',{
            url:'/currentProject',
            templateUrl: 'templates/currentProject.html',
            resolve: {
                load: angularApp.asyncjs(['js/controller/currentProjectCtrl.js','js/service/projectInfo.js','js/service/promise.js'])
            },
            params:{projectDetail:null}
        })

        .state('slidebar.useCase',{
            url:'/useCase',
            templateUrl: 'templates/useCase.html',
            resolve: {
                load: angularApp.asyncjs(['js/controller/useCaseCtrl.js','js/service/projectInfo.js','js/service/promise.js','js/service/paging.js','js/service/formSerialization.js','js/service/upload.js'])
            },
            params:{detailCase:null,modelName:null,pid:null}
        })

        .state('slidebar.model',{
            url:'/model',
            templateUrl: 'templates/model.html',
            resolve: {
                load: angularApp.asyncjs(['js/controller/modelCtrl.js','js/service/projectInfo.js','js/service/promise.js','js/service/paging.js','js/service/formSerialization.js','js/directive/isJson.js','js/filter/headerFilter.js','js/filter/tableDataFilter.js'])
            },
            params:{detailCase:null,modelName:null,pid:null,caseInfo:null}
        })

    $locationProvider.hashPrefix('');
    $urlRouterProvider.otherwise('login');
}])


