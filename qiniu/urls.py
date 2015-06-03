from views import *

urls = [
    (r"/qiniu/upload/?", UploadHandler),
    (r"/qiniu/delete/?", DeleteHandler),
]
