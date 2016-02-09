# Steps for getting node-gyp working on Windows.

1. install Python2.7

    a. copy python.exe python2.7.exe

    b. copy pythonw.exe python2.7w.exe

1. add C:\Python27;C:\Python27\Scripts to PATH

1. environment variable PYTHON=C:\Python27\python.exe

1. either VS 2015 or VS Build Tools installed

1. environment variable GYP_MSVS_VERSION=2015

1. `npm config set python python2.7 --global`

1. `npm config set msvs_version 2015 --global`

NOTE: (some steps may be redundant?)

Useful walkthrough: http://www.serverpals.com/blog/building-using-node-gyp-with-visual-studio-express-2015-on-windows-10-pro-x64

## All Windows Versions

For 64-bit builds of node and native modules you will also need the Windows 7 64-bit SDK

You may need to run one of the following commands if your build complains about WindowsSDKDir not being set, and you are sure you have already installed the SDK:

```bash
call "C:\Program Files\Microsoft SDKs\Windows\v7.1\bin\Setenv.cmd" /Release /x86
call "C:\Program Files\Microsoft SDKs\Windows\v7.1\bin\Setenv.cmd" /Release /x64
```

might need build tools for BOTH windows 8.1 and windows 10 SDKs
