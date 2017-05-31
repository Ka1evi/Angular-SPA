/*!
 * IE10 viewport hack for Surface/desktop Windows 8 bug
 * Copyright 2014-2015 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 */

// See the Getting Started docs for more information:
// http://getbootstrap.com/getting-started/#support-ie10-width

(function () {
  'use strict';

  if (navigator.userAgent.match(/IEMobile\/10\.0/)) {
    var msViewportStyle = document.createElement('style')
    msViewportStyle.appendChild(
      document.createTextNode(
        '@-ms-viewport{width:auto!important}'
      )
    )
    document.querySelector('head').appendChild(msViewportStyle)
  }

})();


/**
 * 切换提示样式
 * id_alert:弹框文字的id
 * id_icon:图标的id
 * id_model:模态框id
 * flag:成功失败标志
 * scope:作用域
 * msg:提示信息
 *
 */
function setStyle(id_alert,id_icon,id_model,flag,scope,msg) {
    if(flag){
    	scope.msg =msg;
        document.getElementById(id_alert).className = "alert alert-success col-sm-8 icon-space fade in";
        document.getElementById(id_icon).className = "icon glyphicon glyphicon-ok-circle";
        setTimeout(function(){
            $(id_model).modal('hide');
        },1500);
    }else{
    	scope.msg =msg;
        document.getElementById(id_alert).className = "alert alert-danger col-sm-8 icon-space fade in";
        document.getElementById(id_icon).className = "icon glyphicon glyphicon-ban-circle";
        setTimeout(function(){
            $(id_model).modal('hide');
        },1500);
    }
}