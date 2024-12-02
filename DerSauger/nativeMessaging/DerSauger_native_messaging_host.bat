@echo off
:: Copyright (c) 2013 The Chromium Authors. All rights reserved.
:: Use of this source code is governed by a BSD-style license that can be
:: found in the LICENSE file.

:: Path resolution example:
:: If this .bat is in: C:\MyApp\nativeMessaging\host\
:: Then:
:: %~dp0                                = C:\MyApp\nativeMessaging\host\
:: %~dp0..                             = C:\MyApp\nativeMessaging\
:: %~dp0..\python39_venv\Scripts       = C:\MyApp\python39_venv\Scripts\
:: %~dp0..\python39_venv\Scripts\python.exe = C:\MyApp\python39_venv\Scripts\python.exe

set PYTHON_PATH=%~dp0..\python39_venv\Scripts\python.exe
echo Resolved Python path: %PYTHON_PATH%

"%PYTHON_PATH%" "%~dp0/DerSauger_native_messaging_host" %*

:: for debugging
:: pause