param(
    [string]$Script = "app.py"
)

# Run Streamlit using the same Python interpreter (avoids relying on a global `streamlit` exe)
$scriptPath = Join-Path $PSScriptRoot $Script
python -m streamlit run $scriptPath
