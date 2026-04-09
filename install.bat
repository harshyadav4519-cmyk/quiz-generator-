@echo off
echo Installing dependencies...

python -m pip install --upgrade pip

pip install flask
pip install flask-cors
pip install groq

echo.
echo Installation complete!
pause