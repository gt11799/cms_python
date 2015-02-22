#coding:utf-8

from utils import *

class JianBasicTemplateHandler(BasicTemplateHandler):

    def __init__(self, *request, **kwargs):

        super(BasicTemplateHandler,self).__init__(*request,**kwargs)
        self.clear_cookie("alert_body")

    def _post(self, **kws):
        try:
            Arguments = self.getArgument()
            assert isinstance(Arguments, dict) == True
            if self.EscapeSQL():
                for key, value in Arguments.items():
                    try:
                        value = MySQLdb.escape_string(value)
                        Arguments[key] = value
                    except:
                        pass
            Arguments.update(kws)
            try:
                self.DBAction(Arguments)
                if self.record_operate_log:
                    logStr = self.get_operate_log(Arguments)
                    logStr and DEBUGLOG.debug(logStr)

            except MyDefineError as e:
                self.write({"status": RET_DBERROR, "msg": str(e)})
                errorStr = traceback.format_exc()
                ERRORLOG.error(errorStr)
                self.set_cookie("alert_body",str(e),expires_days=10)
            except Exception as e:
                errorStr = traceback.format_exc()
                ERRORLOG.error(errorStr)
        except:
            errorStr = traceback.format_exc()
            ERRORLOG.error(errorStr)

        if self.__dict__.get('to_redirect',True):
            self.redirect(self.to_url)
        return   

class JianAsyncHandler(AsyncHandler):

    def __init__(self, *request, **kwargs):

        super(AsyncHandler,self).__init__(*request,**kwargs)
        self.clear_cookie("alert_body")

    @tornado.gen.coroutine
    def _post(self, **kws):
        try:
            self.set_cookie("alert_body","")
            Arguments = self.getArgument()
            assert isinstance(Arguments, dict) == True
            if self.EscapeSQL():
                for key, value in Arguments.items():
                    try:
                        value = MySQLdb.escape_string(value)
                        Arguments[key] = value
                    except:
                        pass
            Arguments.update(kws)
            try:
                yield self.DBAction(Arguments)
                if self.record_operate_log:
                    logStr = self.get_operate_log(Arguments)
                    logStr and DEBUGLOG.debug(logStr)

            except MyDefineError as e:
                self.write({"status": RET_DBERROR, "msg": str(e)})
                errorStr = traceback.format_exc()
                ERRORLOG.error(errorStr)
                self.set_cookie("alert_body",str(e),expires_days=10)
            except Exception as e:
                errorStr = traceback.format_exc()
                ERRORLOG.error(errorStr)
        except:
            errorStr = traceback.format_exc()
            ERRORLOG.error(errorStr)

        self.redirect(self.to_url)
        return 