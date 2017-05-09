/**
 * 对每次获取项目下的模块数据的$http请求的封装
 */

angularApp.register.provider("promise",function(){
	
	/*
	 * method:方法名
	 * params:请求参数
	 * content:返回的数据
	 * 
	 */
	
	this.$get=function($http,$q){
		var content;  //获取的数据 
		var flag=false;   //是否响应成功
		return function(params,url){
			
			var deferred = $q.defer();  
			$http({
				url:url,
	            dataType: 'json',
	            headers: {
	                        'Content-Type': 'application/x-www-form-urlencoded'
	                        },
	            method:'post',
				data:params
				
			}).then(function(respond){
				flag=true;
				console.log(params)
				content=angular.extend(respond,{'flag':flag})
				deferred.resolve(content);  
			}).catch(function(e){
				
				content={'info':e,'flag':flag};
				deferred.resolve(content);  
			})
			return deferred.promise;
		}
	}
	
})




