# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe
import glob
import os
import zlib
import shutil
import sys

shutil.rmtree("build", ignore_errors=True)
shutil.rmtree("dist", ignore_errors=True)
sys.argv.append("py2exe")

MANIFEST_TEMPLATE = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="x86"
    name="%(prog)s"
    type="win32"
  />
  <description>%(prog)s</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel
            level="asInvoker"
            uiAccess="false">
        </requestedExecutionLevel>
      </requestedPrivileges>
    </security>
  </trustInfo>
  <dependency>
    <dependentAssembly>
      <assemblyIdentity
            type="win32"
            name="Microsoft.VC90.CRT"
            version="9.0.21022.8"
            processorArchitecture="x86"
            publicKeyToken="1fc8b3b9a1e18e3b">
      </assemblyIdentity>
    </dependentAssembly>
  </dependency>
  <dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
  </dependency>
</assembly>
"""

class Target(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)

data_files = []

includes = ['MySQLdb']

excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter']

packages = ["sqlalchemy.databases"]

dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll',
                'tk84.dll',
                'MSVCP90.dll', 'mswsock.dll', 'powrprof.dll', 'cppuhelper3MSC.dll',
                'sal3.dll', 'cppu3.dll', 'stlport_vc7145.dll']
icon_resources = []
bitmap_resources = []
other_resources = []
other_resources = [(24, 1, MANIFEST_TEMPLATE % dict(prog="MyAppName"))]
py26MSdll = glob.glob(r"C:\Users\LUCAZ\Desktop\DLL\*.*")
data_files += [("", py26MSdll),]

GUI2Exe_Target_1 = Target(
    script = "cazzaniga.py",
    icon_resources = icon_resources,
    bitmap_resources = bitmap_resources,
    other_resources = other_resources,
    dest_base = "Fatturazione Autoservizi",
    version = "1.0",
    name = "Fatturazione Autoservizi"
    )

setup(
    data_files = data_files,
    options = {"py2exe": {"compressed": 2,
                          "optimize": 2,
                          "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          "dll_excludes": dll_excludes,
                          "bundle_files": 2,
                          "dist_dir": "dist",
                          "xref": False,
                          "skip_archive": False,
                          "ascii": False,
                          "custom_boot_script": '',
                         }
              },
    zipfile = "lib\library.zip",
    console = [],
    windows = [GUI2Exe_Target_1]
    )
