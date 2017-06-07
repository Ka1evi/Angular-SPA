/**
 * 提供关闭上传和导出文件的服务
 */
angularApp.register.provider("download", function() {

	this.$get = function($timeout,promise) {


		/**
		 * scope:对应的作用域
		 * type:1为用例，0为模版
		 * down_address:导出地址
		 * idTemp:选择的导出的用例、模版id
		 * alertId:模态框样式id
		 * iconId:图标id
		 * tipId:提示信息模态框id
		 */
		return function(scope,method,type,down_address,idTemp,down_url,alertId,iconId,tipId){
			//关闭上传
		    scope.closeUp = function () {
		        var others = document.getElementById('count');
		        var canvas = document.querySelector('canvas');
		        var context = canvas.getContext('2d');
		        others.innerText = 0;
		        context.clearRect(0, 0, 500, 20);
		    }

		    //导出到文件
		    scope.download = function () {

		        if (0 == idTemp.length) {

		        	angular.element(tipId).modal('show');
		        	setStyle(alertId,iconId,tipId,false,scope,"请选择需要导出的用例/模版");
		            return;
		        }

		        params = angular.extend({'opr': method}, {'typ': type, 'address': down_address, 'id': idTemp});

		        promise(params, down_url).then(function (result) {

		            if (result.flag) {
		                var downloadFile = result.data;
		                if (0 == downloadFile.status) {
		                    var file_address = downloadFile.address + downloadFile.filename;
		                    var downLink=angular.element('#isDownload').get(0);
		                    downLink.href=file_address;
		                    downLink.click();
		                }else{
		                	angular.element(tipId).modal('show');
				        	setStyle(alertId,iconId,tipId,false,scope,"文件导出失败");
		                }

		            } else {
		                alert(result.info);
		            }
		        })
		    }
		}
	}
});


