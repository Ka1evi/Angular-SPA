#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, make_response, redirect
import json, time, os, sys
from tp_base import tp_index_dict
from tp_base import tp_file_upload_list
from tp_global import *
from tp_mongodb import *
from tp_read import Cread
from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
app = Flask(__name__)
app.debug = True


@app.route("/cgi-bin/<fun>", methods=['GET', 'POST', 'OPTIONS'])
def index_func(fun):
    if fun in tp_index_dict:
        c = tp_index_dict[fun]
        req_dict = {}
        isupload = False
        if request.method == "GET":
            if fun in tp_file_upload_list:
                return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
          <p><input type=file name=file>
             <input type=submit value=Upload>
        </form>
'''
            else:
                req_dict["input"] = request.args
        elif request.method == "POST":

            if fun in tp_file_upload_list:
                req_dict["input"] = {"opr": "upload"}

                isupload = True

            else:
                try:
                    req_dict["input"] = json.loads(request.get_data())
                except:
                    return g_err["refused"]
        else:
            return g_err["refused"]
        ip = request.headers.get('X-Real-IP')

        if ip is None or ip == "":
            ip = "127.0.0.1"
        ssid = request.cookies.get('ssid')
        if ssid is None:
            ssid = ''
        req_dict["tp_self"] = {}
        req_dict["tp_self"]["ip"] = ip
        req_dict["tp_self"]["ssid"] = ssid
        req_dict["tp_self"]["m"] = request.method
        req_dict["tp_self"]["fun"] = fun
        c.myinit()
        c.setenv(req_dict)
        try:
            c.onInit()
        except:
            c.mydel()
            raise
        out = c.output()

        # file upload
        if isupload:
            try:
                ret_dict = json.loads(out)
            except:
                c.mydel()
                return g_err["refused"]
            if int(ret_dict["status"]) != 0:
                c.mydel()
                return g_err["refused"]
            file = request.files['file']
            pid=request.form.get("pid",'')
            typ = request.form.get("typ", '')
            pmodel = request.form.get("pmodel", '')
            user = request.form.get("user", '')
            filename = file.filename
            a, b = os.path.splitext(filename)
            if '.' in filename and filename.rsplit('.', 1)[1] in ret_dict["allow"]:
                f = "%.20f" % time.time()
                f += "%s" % b
                file.save(ret_dict["path"] + f)
                data=Cread().caread(pid,typ,f,pmodel,user)
                out = {"status": 0, "msg": "success", "data": data}
            else:
                out = {"status": 1, "msg": "文件类型错误，只支持yaml,xls,xlsx格式"}
            c.mydel()
            out = json.dumps(out)
            # return json.dumps(out, ensure_ascii=False)

        if c.redirect_url is not None:
            c.mydel()
            return redirect(c.redirect_url)
        resp = make_response(out)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        resp.headers['Access-Control-Allow-Headers'] = allow_headers
        # resp.headers['Content-type'] = 'application/json'

        if c.out_ssid is not None:
            resp.set_cookie('ssid', value=c.out_ssid)
        c.mydel()
        return resp
    else:
        return g_err["refused"]

if __name__ == '__main__':
    # app.run()
    http_server = WSGIServer(('127.0.0.1', 5002), app)
    http_server.serve_forever()