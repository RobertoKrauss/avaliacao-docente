# Encerra processos travados e inicia o app Streamlit

taskkill /IM streamlit.exe /F 2>$null
taskkill /IM python.exe /F 2>$null

cd C:\Users\rober\Documents\09_Projeto_acompanhamento
$env:PYTHONPATH="C:\Users\rober\Documents\09_Projeto_acompanhamento"
streamlit run app/main.py
