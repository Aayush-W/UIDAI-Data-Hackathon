@echo off
rem Helper to run Streamlit using the same Python interpreter (avoids PATH issues)
if "%1"=="" (
  python -m streamlit run "%~dp0app.py"
) else (
  python -m streamlit run "%~dp0%1"
)
