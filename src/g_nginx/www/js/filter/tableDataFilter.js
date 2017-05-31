/*
 * 用于过滤表格数据
 * 
 */

angularApp.register.filter("tableDataFilter", function () {
    return function (input, arr) {

        //console.log(input);
        //console.log(arr)

        var filterArr = []; //过滤后的数组
        var tempArr = {}; //临时存放满足过滤条件的数组元素

        angular.forEach(input, function (v, k) {

            angular.forEach(arr, function (av, ak) {
                //console.log(v);
                delete v[av];
            })

            filterArr[filterArr.length] = v
        })
        //console.log(filterArr);
        return filterArr;
    }
})