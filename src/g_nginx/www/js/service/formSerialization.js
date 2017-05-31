/*
 * 表单序列化：
 *   参数：表单<form>的name属性值
 *   使用规则:1:form/input/textarea/select/checkbox/radio必须存在name属性
 *            2:checkbox的name属性名不同
 *   返回值:1、返回的表单数据是json格式
 *          2、键为input/textarea/select/checkbox/radio的name属性值
 */
angularApp.register.provider('formSerialization', function () {

    this.$get = function () {

        return function (formName) {
            var content = {} //表单数据容器
            var forms = document.forms[formName];  //根据表单名称获取表单
            var elements = forms.elements;         //获取表单内的所有元素
            for (var i = 0; i < elements.length; i++) {

                //获取input输入框中的数据
                if (elements[i].nodeName.toLowerCase() == "input") {
                    var type = elements[i].type;
                    var inputName;
                    switch (type) {
                        case 'text':
                            inputName = elements[i].name;
                            content[inputName] = elements[i].value
                            break;
                        case 'checkbox':
                            console.log(elements[i].checked);
                            if (elements[i].checked == true) {
                                inputName = elements[i].name;
                                content[inputName] = elements[i].nextSibling.nodeValue;
                            }
                            break;
                        case 'radio':
                            console.log(elements[i].checked);
                            if (elements[i].checked == true) {
                                inputName = elements[i].name;
                                content[inputName] = elements[i].nextSibling.nodeValue;
                            }
                            break;
                    }
                }
                //获取textarea中的数据
                if (elements[i].nodeName.toLowerCase() == "textarea") {
                    var inputName = elements[i].name;
                    var value = elements[i].value;
                    try {
                        value = eval('(' + value + ')');
                        if ((typeof value) == 'object') {
                            console.log(value)
                        } else {
                            value = eval('(' + value + ')');
                            console.log(value)
                        }
                        content[inputName] = value
                    } catch (e) {
                        content[inputName] = value;     //不是json就到异常中设置值
                    }
                }
                //获取下拉框中的数据
                if ((elements[i].nodeName.toLowerCase() == "select")) {
                    var inputName = elements[i].name;
                    var selected = elements[i].selectedIndex;//获取选中的下拉框索引，从0开始
                    //console.log(elements[i].options[selected].value)
                    var selectedValue = elements[i].options[selected].value.substring(7);
                    //var indexs=selectedValue
                    content[inputName] = selectedValue;
                }
            }
            return content;
        }
    }
})















