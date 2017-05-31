/*
 * 创建一个服务用于存放用户选择的项目名和项目id,用户名,项目模块
 */

angularApp.register.service("projectInfo", function () {
    var user = {};  //用户名
    var project = {};//项目名称
    var model = {};  //选择的项目id
    var modules = {};//项目下的模块;
    var allProject = {};//当前用户下的所有项目
    var fromPage = null;//设置来的页面

    this.setProjectName = function (name) {
        project.name = name
    }
    this.getProjectName = function () {
        return project.name
    }

    this.setModelId = function (id) {
        model = id;
    }
    this.getModelId = function () {
        return model
    }

    this.setUserName = function (name) {
        user.name = name;
    }

    this.getUserName = function () {
        return user.name;
    }

    this.setModules = function (allModule) {
        modules = allModule;
    }

    this.getModels = function () {
        return modules;
    }

    this.setAllProject = function (projects) {
        allProject = projects;
    }

    this.getAllProject = function () {
        return allProject;
    }

    this.setFromPage = function (page) {
        fromPage = page;
    }
    this.getFromPage = function () {
        return fromPage;
    }

})