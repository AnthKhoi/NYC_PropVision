@echo off
chcp 65001 > nul
echo ========================================================
echo   KHOI DONG NYC REAL ESTATE ANALYTICS & AI DASHBOARD
echo ========================================================
echo.

if not exist nyc_rf_model.pkl (
    echo Dang huan luyen mo hinh AI...
    python train_model.py
)

echo Dang mo giao dien Streamlit Dashboard...
if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" -m streamlit run app.py
) else (
    streamlit run app.py || python -m streamlit run app.py
)

pause
