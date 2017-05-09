/*
 * 创建一个服务用于存放用户选择的项目名和项目id,用户名,项目模块
 */

angularApp.register.service("projectInfo",function(){
    this.user={};  //用户名
    this.project={};//项目名称
    this.model={};  //选择的项目id
    this.modules={};//项目下的模块;
    this.allProject={};//当前用户下的所有项目
    this.fromPage=null;//设置来的页面
    
    this.setProjectName=function(name){
        this.project.name=name
    }
    this.getProjectName=function(){
        return this.project.name
    }
    
    this.setModelId=function(modelName){
    	this.model=modelName;
    }
    this.getModelId=function(){
    	return this.model
    }
    
    this.setUserName=function(name){
    	this.user.name=name;
    }
    
    this.getUserName=function(){
    	return this.user.name;
    }
    
    this.setModules=function(modules){
    	this.modules=modules;
    }
    
    this.getModels=function(){
    	return this.modules;
    }
    
    this.setAllProject=function(allProject){
    	this.allProject=allProject;
    }
    
    this.getAllProject=function(){
    	return this.allProject;
    }
    
    this.setFromPage=function(name){
        this.fromPage=name;
    }
    this.getFromPage=function(){
        return this.fromPage;
    }
    
})