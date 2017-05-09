/*
 * 实现分页
 */

angularApp.register.provider("paging", function() {

	this.$get = function($http) {

		return function(info, contains, scope, total, idTemp, url, params,pageInfo) {
			    /**
			     * 
			     * info:当页数据
			     * contains:每页显示的数据量，默认8条
			     * scope：对应的作用域
			     * total:数据总数
			     * idTemp:被选中的数据
			     * url:查询数据的url
			     * params:查询数据所需的参数
			     * pageInfo:保存当页数据
			     */
			    $scope=scope;
			    $scope.pageSize = contains;   //每页显示5条
				$scope.pages = Math.ceil(total / contains); //分页数
				$scope.newPages = $scope.pages > 5 ? 5 : $scope.pages;    //确定页码,只显示5个页码
				$scope.pageList = [];
				$scope.selPage = 1;
				$scope.num=0;
				//获取表格数据
				$scope.setData = function(current) {
					params = angular.extend(params, {'page': current})
					$http({
						url: url,
						dataType: 'json',
						headers: {
							'Content-Type': 'application/x-www-form-urlencoded'
						},
						method: 'post',
						data: params
		
					}).then(function(respond) {
						$scope.showInfo = respond.data.data;
						pageInfo=angular.fromJson(angular.toJson(respond.data.data))
						$scope.isSelected = function(id) {
							return idTemp.indexOf(id) != -1;
						}
		
					}).catch(function(e) {
						alert(e.toString())
					})
					
				}
				$scope.showInfo = info;
				
				//pageInfo=info;
				
				//初始化页码
				for(var i = 0; i < $scope.newPages; i++) {
					$scope.pageList.push(i + 1);
				}
				//获取当前选中页索引
				$scope.selectPage = function(page) {
					
					//不能小于1大于最大
					if(page < 1 || page > $scope.pages) return;
					
					//确定序号起始
					$scope.num=(page-1)*contains
					
					//页码容器，最多显示分页数5
					var newpageList = []; 
					if($scope.pages <= 5){     //页码数小于5
						for(var i=0;i<$scope.pages;i++){
							newpageList.push(i + 1);
						}
						$scope.pageList = newpageList;
					}else if(page >2 && page<($scope.pages-2) ) {
						//因为只显示5个页数，大于2页开始分页转换
						for(var i = (page - 3); i < ((page + 2) > $scope.pages ? $scope.pages : (page + 2)); i++) {
							newpageList.push(i + 1);
						}
						$scope.pageList = newpageList;
					}else if(page >= ($scope.pages-2)){  //页码大于等于总数-2
						for(var i = ($scope.pages - 4); i <= $scope.pages; i++) {
							newpageList.push(i);
						}
						$scope.pageList = newpageList;
					}else if(page <=2 ){   //选择首页
						for(var i = 0; i < $scope.newPages; i++) {
							newpageList.push(i + 1);
						}
						$scope.pageList = newpageList;
					}
					$scope.selPage = page;                 //选择的页码
					$scope.setData(page);                  //获取数据
					$scope.isActivePage(page);           //激活样式
				};
				//设置当前选中页样式
				$scope.isActivePage = function(page) {
					return $scope.selPage == page;
				};
				//首页
				$scope.first=function(){
					$scope.selectPage(1);
				};
				//上一页
				$scope.pre = function() {
					$scope.selectPage($scope.selPage - 1);
				}
				//下一页
				$scope.next = function() {
					$scope.selectPage($scope.selPage + 1);
				};
				//尾页
				$scope.last=function(){
					$scope.selectPage($scope.pages);
				}
		}
	}
})