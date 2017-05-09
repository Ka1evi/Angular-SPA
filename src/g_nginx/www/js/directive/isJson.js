/*
 * 校验请求数据为json格式
 */


angularApp.register.directive("isJson", function() {
	return {
		require: 'ngModel',
		link: function($scope, $element, $attr, ctrl) {

			ctrl.$parsers.unshift(function(obj) {
				try{
					var input=parseInt(obj); //输入的是数值型的字符串
					console.log((typeof input))
					if(((typeof input) =='number') && !isNaN(input)){
						ctrl.$setValidity('isJson', false);
						return;
					}
					obj=eval('(' + obj + ')');
					
					if((typeof obj) == 'object'){
						ctrl.$setValidity('isJson', true);  //输入框的数据没有用引号引起来，即形如:{'name':'liSi', 'password':'321'}
						return obj;
					}
					obj=eval('(' + obj + ')');
					ctrl.$setValidity('isJson', true);
					return obj;
				}catch(e){
					ctrl.$setValidity('isJson', false);
					return;
				}
			})
		}
	}
})