#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
from semantics import semantics_index
from semantics import semantics_show
from catchwords import catchwords_index
from catchwords import catchwords_show
from pca import pca_index
from pca import pca_show

import os
home=''
os.environ["SCRIPT_NAME"] = home
os.environ["REAL_SCRIPT_NAME"] = home

urls = (
    "/", "semantics_index",
    "/semantics", "semantics_index",
    "/semantics/show", "semantics_show",
    "/catchwords", "catchwords_index",
    "/catchwords/show", "catchwords_show",
    "/pca", "pca_index",
    "/pca/show", "pca_show",
    )
app = web.application(urls, globals())

if __name__ == "__main__":
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()
