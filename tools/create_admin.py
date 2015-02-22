import os
import sys

path =  os.path.dirname(__file__)
sys.path.append(os.path.join(path,".."))

from utility.utils import getMongoDBConn
from login.models import genCompanyAcount

username = "pluray"
password = "admin"
email = "haifang@pluray.com"
phone = "18603036769"
company_name = "youihui"
level = 2

genCompanyAcount(username,password,email,phone,company_name,level)