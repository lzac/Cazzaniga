# -*- coding: utf-8 -*-

# Moduli di libreria
# Moduli python
import tempfile
import string
import os, sys
import datetime
import tempfile
# Moduli sql alchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy import MetaData
from sqlalchemy import exc
# Moduli wxpython
import wx
import wx.lib.agw.aui as aui
import wx.lib.mixins.listctrl  as  listmix
import wx.xrc as xrc
import xml.etree.ElementTree
import xml.etree.cElementTree as ET
from xml.dom.minidom import Document
import mod_lib as lib #@UnusedImport
import myxrc