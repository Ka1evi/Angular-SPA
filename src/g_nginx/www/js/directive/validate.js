/*
 * 校验信息的唯一性
 */

angularApp.register.directive("validate", function ($http, $q) {

    return {
        restrict: 'A',
        require: 'ngModel',
        link: function (scope, element, attr, ctrl) {

            ctrl.$asyncValidators.unique = function (modelValue, viewValue) {
                var value = modelValue || viewValue;
                var defer = $q.defer();
                var path = env[env['get']]['login']; //获取登录模块的路径
                var url = path['login'];
                var method = attr.method; //获取后台校验方法的名称

                $http.get(url + '?opr=' + method + '&name=' + value).then(function (res) {
                    if (1 == res.data.status) {
                        defer.reject();
                    } else {
                        defer.resolve();
                    }
                })

                return defer.promise;
            }
        }
    }

});