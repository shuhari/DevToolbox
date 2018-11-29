set QTDIR=D:\Lan\Qt\5.11.2\build\win64-msvc

cd src
pylupdate5 strings.py -ts translations/strings_zh.ts
%QTDIR%\bin\linguist .\translations\strings_zh.ts
cd ..
