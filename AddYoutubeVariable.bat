
for /f "usebackq tokens=2,*" %%A in (`reg query HKCU\Environment /v PATH`) do set my_user_path=%%B

setx PATH "%~dp0youtube-dl;%my_user_path%"

timeout 5