/**
 * Created by root on 2017/3/17.
 */
'use strict';

var angularApp = angular.module('start',['ngRoute', 'ui.router' ,'ngAnimate', 'chart.js']);

/**
 * 异步加载ui-router-config.js中resolve属性配置的js
 */
angularApp.config(function($controllerProvider, $compileProvider, $filterProvider, $provide) {
    angularApp.register = {      //由于script.js是异步加载的，在加载js时angular的controller还没有实例化，所以需要给controller赋值
        controller: $controllerProvider.register,
        directive: $compileProvider.directive,
        filter: $filterProvider.register,
        factory: $provide.factory,
        service: $provide.service,
        provider:$provide.provider,
    };
    angularApp.asyncjs = function (js) {
        return ["$q", "$route", "$rootScope", function ($q, $route, $rootScope) {
            var deferred = $q.defer();
            $script(js, function () {
                $rootScope.$apply(function () {
                    deferred.resolve();
                });
            });
            return deferred.promise;
        }];
    }
});

