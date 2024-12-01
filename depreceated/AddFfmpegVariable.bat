:: setx PATH %PATH%;%~dp0python-3.9.0-embed-amd64


for /f "usebackq tokens=2,*" %%A in (`reg query HKCU\Environment /v PATH`) do set my_user_path=%%B

setx PATH "%~dp0ffmpeg\bin;%my_user_path%"

timeout 1

