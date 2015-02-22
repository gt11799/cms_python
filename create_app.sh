#!/bin/bash

mkdir $1

touch $1/__init__.py

touch $1/views.py && echo "#coding:utf-8" > $1/views.py

touch $1/urls.py  && echo "#coding:utf-8" > $1/urls.py && echo "from views import *" >> $1/urls.py

touch $1/models.py && echo "#coding:utf-8" > $1/models.py
