from pathlib import Path
import sys

import dotenv


def test_streamlit_page_loads_with_mvp_as_script_directory(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(dotenv, "load_dotenv", lambda *_args, **_kwargs: None)

    from streamlit.testing.v1 import AppTest

    repository_root = Path(__file__).resolve().parents[1]
    mvp_directory = repository_root / "mvp"
    monkeypatch.setattr(sys, "path", [str(mvp_directory)] + [
        path for path in sys.path if path != str(repository_root)
    ])
    app_path = mvp_directory / "app.py"
    app = AppTest.from_file(str(app_path)).run()

    assert not app.exception
    assert any(selectbox.label == "Screening mode" for selectbox in app.radio)
    assert any(
        notice.value
        == "Demonstration with public synthetic data only. Not for clinical or enrolment decisions."
        for notice in app.info
    )
