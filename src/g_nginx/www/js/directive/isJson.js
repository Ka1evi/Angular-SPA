/*
 * 校验请求数据为json格式
 */

angularApp.register.directive("isJson", function () {
    return {
        require: 'ngModel',
        link: function ($scope, $element, $attr, ctrl) {

            ctrl.$parsers.unshift(function (obj) {
                try {
                    obj = eval('(' + obj + ')');
                    console.log(obj)
                    var flag = $.isPlainObject(obj);
                    if (flag) {
                        ctrl.$setValidity('isJson', true);
                        return obj;
                    } else {
                        ctrl.$setValidity('isJson', false);
                    }
                } catch (e) {
                    ctrl.$setValidity('isJson', false);
                    return;
                }
            })
        }
    }
})
