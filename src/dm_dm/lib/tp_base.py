#!/usr/bin/env python
# coding=utf-8

# @file    vpn_base.py
# @brief   基础文件
# @author  zhanglong
# @date    2016-08-23
# @version 1.0

import login, upload, project, case_model, case, result, setting, model,tp_out,tp_read

tp_index_dict = {
    "login.do": login.Clogin(),
    "upload.do": upload.Cupload(),
    "project.do": project.Cproject(),
    "case_model.do": case_model.Ccase_model(),
    "case.do": case.Ccase(),
    "out.do": tp_out.Cout(),
    "read.do": tp_read.Cread(),
    "result.do": result.Cresult(),
    "setting.do": setting.Csetting(),
    "model.do": model.Cmodel()
}

tp_file_upload_list = ["upload.do"]
