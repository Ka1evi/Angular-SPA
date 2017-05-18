/**
 * 定义一个服务用于文件上传
 *  注意: 1、一次最多上传5个文件
 *        2、文件大小不能超过100M
 * 
 */

angularApp.register.provider("upload", function() {

	this.$get = function($http,paging) {
		
		/**
		 * url:文件上传的地址
		 * formData:上传所需的参数
		 * scope：对应的作用域
		 * idTemp:被选中的数据
		 * paramsPaging:查询数据所需的参数
		 * url_paging:分页的url
		 */
		
		return function(url,formData,scope,idTemp,paramsPaging,url_paging) {
			
			var dropArea = document.getElementById('dropArea');
			var count = document.getElementById('count');
			var result = document.getElementById('result');
			var canvas = document.querySelector('canvas');
			var context = canvas.getContext('2d');
			
			var list = [];  //文件容器
			var totalSize = 0; //文件总大小
			var totalProgress = 0; //进度条
			var dataList={}; //返回的数据
			var contentError="";//上传的文件内容格式错误
			var typeError="";//上传文件的类型错误
			var files_num=0;//当次拖拽的文件总数
			var num=0 ;//已经上传和正在上传的文件数

			//监听文件上传事件
			function initHandlers() {
				
				dropArea.addEventListener('dragenter', handleEnter, false);
				dropArea.addEventListener('drop', handleDrop, false);
				dropArea.addEventListener('dragover', handleDragOver, false);
			}

			//绘制进度条
			
			function drawProgress(progress) {

				//清空进度信息
				context.clearRect(0, 0, canvas.width, canvas.height);

				context.beginPath();
				context.strokeStyle = '#5cb85c';
				context.fillStyle = '#5cb85c';
				context.fillRect(0, 0, progress * 500, 20);
				context.closePath();

				context.font = '16px Verdana';
				context.fillStyle = '#000';
				context.fillText('上传进度: ' + Math.floor(progress * 100) + '%', 50, 15);

			}
			
			//文件拖到目标
			function handleEnter(event){
				
				event.preventDefault();
				event.stopPropagation();
			}

			//文件拖动事件
			function handleDragOver(event) {
				
				event.preventDefault();
				event.stopPropagation();

				dropArea.className = 'file-highlighted';
			}

			//文件拖动完成事件
			function handleDrop(event) {
				
				event.preventDefault();
				event.stopPropagation();

				processFiles(event.dataTransfer.files);
			}

			//获取文件的信息
			function processFiles(filelist) {
				if(!filelist || !filelist.length || list.length) return;
                
                //重置数据
                files_num=0;
				num=0 ;
				totalSize = 0;
				totalProgress = 0;
				contentError="";
				typeError="";
				//result.textContent = '';

				for(var i = 0; i < filelist.length && i < 5; i++) {
					list.push(filelist[i]);
					totalSize += filelist[i].size;
				}
				files_num=list.length;
				uploadNext();
			}
			

			//一个文件上传完成后更新进度条
			
			function handleComplete(size) {
				totalProgress += size;
				drawProgress(totalProgress / totalSize);
				uploadNext();
			}

			//文件开始上传
			function uploadFile(file, status) {
                
				
				formData.append('file', file);
				console.log(formData.get('file'))
				console.log(formData.get('typ'))
				$http({
					url:url,
		            headers: {
		                        'Content-Type': undefined
		                        },
		            method:'post',
					data:formData
					
				}).then(function(res){
					num++;
					console.log(num);
	                var respond=res.data;
	                formData.delete('file'); //上传后删除
	                console.log(formData.get('file'))
	                if(0 == respond.status){
	                	//handleComplete(file.size);
						if("success" == respond.msg){
							var results=respond.data;
							$scope.total=results.count;
			        		total=results.count;
			        		infoPart=results.list;
			        		paging(infoPart,8,scope,total,idTemp,url_paging,paramsPaging);
			        		
			        		if("fail" == results.msg){
			        			//alert("文件"+file.name+"上传失败");
			        			contentError = contentError+file.name +" ;"
			        			handleComplete(0);
			        			//return;
			        		}else{
			        			handleComplete(file.size);
			        		}
						}
	                }else{
	                	//alert(respond.msg)
	                	console.log(num);
	                	formData.delete('file'); //上传后删除
	                	typeError = typeError+file.name +" ;"
	                	handleComplete(0);
	                }
					
					
				}).catch(function(e){
					
					num++;
					console.log(num);
					formData.delete('file'); //上传后删除
					typeError = typeError+file.name +" ;"
					handleComplete(0);
				}).finally(function(){
					
					if(num == files_num){
						if("" != contentError && "" != typeError){
							alert("文件 "+contentError+"内容错误,"+typeError+"类型错误")
						}else if("" != contentError){
							alert("文件 "+contentError+"内容错误")
						}else if("" != typeError){
							alert("文件 "+typeError+"类型错误")
						}
					}
				})
				
			}

			function uploadNext() {
				if(list.length) {
					
					console.log(formData)
					count.textContent = list.length - 1;
					dropArea.className = 'file-drop-zone';

					var nextFile = list.shift();
					if(nextFile.size >= 104857600) { // 100M
						alert("文件超过了100M");
						handleComplete(nextFile.size);
					} else {
						uploadFile(nextFile, status);
					}
				} else {
					dropArea.className = 'file-drop-zone';
				}
			}
			initHandlers();
		}
	}
})