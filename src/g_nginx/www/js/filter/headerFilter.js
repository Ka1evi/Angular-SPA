/*
 * 用于过滤表头
 */


angularApp.register.filter("headerFilter", function() {
	return function(input, arr) {
		
		//console.log(input);
		//console.log(arr)
		angular.forEach(arr, function(av, ak) {
			var index = input.indexOf(av);
			if(index != -1) {
				input.splice(index, 1);
			}
		})
		console.log(input);
		return input
	}
})