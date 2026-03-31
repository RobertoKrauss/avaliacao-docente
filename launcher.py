"""
Launcher para o executável Windows.
- Cria/garante o banco e o schema.
- Inicia o Streamlit apontando para app/main.py.
- Registra log em launcher.log (na mesma pasta do executável).
"""
import os
import sys
import traceback
from pathlib import Path

from app.db.seed import bootstrap_database
import streamlit.web.cli as stcli


def log(msg: str) -> None:
    log_dir = Path(sys.executable).resolve().parent  # sempre na pasta do executável/dist
    log_file = log_dir / "launcher.log"
    with log_file.open("a", encoding="utf-8") as f:
        f.write(msg + "\n")


def main():
    base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    os.chdir(base_dir)
    # evitar conflito de porta/dev-mode ao empacotar
    os.environ["STREAMLIT_GLOBAL_DEVELOPMENTMODE"] = "false"
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    os.environ["STREAMLIT_BROWSER_GATHERUSAGESTATS"] = "false"
    os.environ["STREAMLIT_BROWSER_SERVER_ADDRESS"] = "localhost"
    log("---- iniciar launcher ----")
    try:
        bootstrap_database()
        log("Banco e schema prontos.")
        target = base_dir / "app" / "main.py"
        if not target.exists():
            raise FileNotFoundError(f"main.py não encontrado em {target}")
        # escreve config local para evitar conflito com config global do usuário
        config_dir = base_dir / ".streamlit"
        config_dir.mkdir(exist_ok=True)
        config_file = config_dir / "config.toml"
        config_file.write_text(
            "[server]\nheadless = true\nport = 8501\nenableCORS = false\nenableXsrfProtection = false\n"
            "[browser]\ngatherUsageStats = false\n"
            "[global]\ndevelopmentMode = false\n",
            encoding="utf-8",
        )
        os.environ["STREAMLIT_CONFIG_FILE"] = str(config_file)
        sys.argv = ["streamlit", "run", str(target)]
        log("Chamando streamlit...")
        sys.exit(stcli.main())
    except SystemExit as e:
        log(f"SystemExit: {e}")
        raise
    except Exception as e:
        tb = traceback.format_exc()
        log(f"Erro: {e}\n{tb}")
        raise


if __name__ == "__main__":
    main()
