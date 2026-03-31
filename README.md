# Sistema de Controle de Avaliação de Desempenho Docente — v1

Stack: **Python + SQLite + Streamlit**  
Pasta de trabalho: `C:\Users\rober\Documents\09_Projeto_acompanhamento`

## Estrutura
- `app/db/` — schema, seed e repositórios (anos, atividades, evidências, regras, alertas, checkins, sugestões, configs).
- `app/services/` — cálculo de pontuação, risco, alertas, pipelines.
- `app/ui/` — páginas Streamlit: dashboard, evidências, regras, alertas, check-ins, relatório, ChatGPT (MVP) + tema e componentes.
- `app/main.py` — entrypoint Streamlit.
- `tests/test_calculo.py` — testes básicos do motor de pontuação.
- `sample_data.py` — insere dados de exemplo.

## Setup rápido
```powershell
cd C:\Users\rober\Documents\09_Projeto_acompanhamento
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m app.db.seed   # cria/atualiza banco e regras padrão
```

## Executar a aplicação
```powershell
streamlit run app/main.py
```
Sidebar de navegação:
Dashboard | Evidências | Regras | Alertas | Check-ins | Relatório | ChatGPT (MVP)

## Dados de exemplo (opcional)
```powershell
python sample_data.py
```
Cria algumas atividades por fator, uma evidência e uma regra personalizada para testar dashboard, alertas e relatório.

## Exportações
- Relatório anual: prévia Markdown e download `.md` / `.csv` em **Relatório**.
- PDF simples não incluído (mantido no escopo mínimo).

## ChatGPT (MVP)
- Consultivo apenas; exige consentimento explícito para usar perfil de escrita.
- Sugestões são salvas em `sugestoes_chatgpt` e nunca alteram dados automaticamente.

## Testes
```powershell
python -m unittest tests/test_calculo.py
```

## Empacotamento Windows (PyInstaller)
1) Ative o ambiente e instale dependências:
```powershell
cd C:\Users\rober\Documents\09_Projeto_acompanhamento
.\.venv\Scripts\activate
pip install -r requirements.txt pyinstaller
```
2) Comando exato usado:
```powershell
pyinstaller ^
  --onefile ^
  --name AvaliacaoDocente ^
  --add-data "app\\db\\schema.sql;app/db" ^
  --add-data "app\\db\\database.sqlite;app/db" ^
  --add-data "app\\ui\\theme.py;app/ui" ^
  launcher.py
```
3) Artefatos ficam em `dist\AvaliacaoDocente.exe`.
4) Arquivo auxiliar `run.bat` (gerado) pode ser usado para iniciar.

Executar o .exe
```powershell
cd C:\Users\rober\Documents\09_Projeto_acompanhamento\dist
.\AvaliacaoDocente.exe
```
O navegador abrirá em http://localhost:8501 (ou copie a URL exibida no console).
- Logs do launcher ficam em `dist\launcher.log` (útil para depuração).

## Script run.bat
```
@echo off
set BASE=%~dp0
cd /d %BASE%
if exist AvaliacaoDocente.exe (
  AvaliacaoDocente.exe
) else (
  echo Executavel não encontrado. Gere primeiro com PyInstaller.
)
```

## Escopo e limites
- Sem login/multiusuário, SIAVI, OCR, integrações automáticas.
- Pontuação não é alterada por IA; alertas e sugestões são apenas apoio.

## Próximos passos possíveis
- PDF do relatório (quando o fluxo estiver estável).
- Melhorias de UX em formulários de atividade/evidência.
