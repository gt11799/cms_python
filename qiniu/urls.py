from views import *

urls = [
    (r"/qiniu/test_upload/?", TestUploadHandler),
    (r"/qiniu/upload/?", UploadHandler),
    (r"/qiniu/delete/?", DeleteHandler),
    (r"/qiniu/goods_image_upload/?", GoodsImageUpload),
    (r"/qiniu/test_saveas/?", TestsaveasHandler),
    (r"/qiniu/gen_upload_token/?",GenUploadToken),
    (r"/qiniu/upload_client_image_info/?",uploadClientImageInfoHandler),
]
