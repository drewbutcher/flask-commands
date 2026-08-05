import os
import subprocess

from click.testing import CliRunner

from flask_commands.commands.new import new
from flask_commands.utils.venv import venv_executable


def _assert_app_factory_renders_starter_template(project_path):
    python_path = venv_executable(str(project_path / "venv"), "python")
    environment = os.environ.copy()
    environment.update(
        {
            "APP_NAME": "test application",
            "SQLALCHEMY_DEVELOPMENT_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_PRODUCTION_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    result = subprocess.run(
        [
            python_path,
            "-c",
            (
                "from flask import render_template\n"
                "from app import create_app\n"
                "\n"
                'for config_name in ("development", "production"):\n'
                "    app = create_app(config_name)\n"
                '    with app.test_request_context("/"):\n'
                '        rendered = render_template("mains/index.html")\n'
                '        assert "<title>Hello World | Test Application</title>" in rendered\n'
                '        assert "<div>Hello World</div>" in rendered\n'
                '        assert "tailwind.min.css?v=" in rendered\n'
            )
        ],
        cwd=project_path,
        env=environment,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr

def _assert_user_model_crud_helpers(project_path):
    python_path = venv_executable(str(project_path / "venv"), "python")
    environment = os.environ.copy()
    environment.update(
        {
            "APP_NAME": "test application",
            "SQLALCHEMY_DEVELOPMENT_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_PRODUCTION_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    result = subprocess.run(
        [
            python_path,
            "-c",
            (
                "from app import create_app, db\n"
                "from app.models import User\n"
                "\n"
                'app = create_app("development")\n'
                "with app.app_context():\n"
                "    db.create_all()\n"
                "\n"
                "    user = User.create({\n"
                '        "username": "original",\n'
                '        "password": "secret",\n'
                "    })\n"
                "    assert user.id is not None\n"
                '    assert user.username == "original"\n'
                '    assert user.verify_password("secret")\n'
                "\n"
                "    updated_user = user.update({\n"
                '        "username": "updated",\n'
                '        "password": "new secret",\n'
                "    })\n"
                "    assert updated_user is user\n"
                '    assert user.username == "updated"\n'
                '    assert user.verify_password("new secret")\n'
                "\n"
                "    try:\n"
                "        user.update({\n"
                '            "username": "should not change",\n'
                '            "zeta": "invalid",\n'
                '            "alpha": "invalid",\n'
                "        })\n"
                "    except AttributeError as exception:\n"
                "        assert str(exception) == (\n"
                '            "Unknown User attribute(s): alpha, zeta"\n'
                "        )\n"
                "    else:\n"
                '        raise AssertionError("User.update() accepted invalid attributes")\n'
                '    assert user.username == "updated"\n'
                "\n"
                "    try:\n"
                "        User.create({\n"
                '            "username": "not-created",\n'
                '            "unknown": "invalid",\n'
                "        })\n"
                "    except AttributeError as exception:\n"
                "        assert str(exception) == (\n"
                '            "Unknown User attribute(s): unknown"\n'
                "        )\n"
                "    else:\n"
                '        raise AssertionError("User.create() accepted invalid attributes")\n'
                "    assert User.query.filter_by(\n"
                '        username="not-created"\n'
                "    ).first() is None\n"
                "\n"
                "    user_id = user.id\n"
                "    user.delete()\n"
                "    assert db.session.get(User, user_id) is None\n"
            ),
        ],
        cwd=project_path,
        env=environment,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr

def _assert_common_project_scaffold(project_path, project_name):
    # Core paths
    assert (project_path / "run.py").exists()
    assert (project_path / "run.sh").exists()
    assert (project_path / ".env").exists()
    assert (project_path / ".env.example").exists()
    assert (project_path / "requirements.txt").exists()
    assert (project_path / "venv" / "bin" / "python").exists()

    assert (project_path / "app" / "controllers" / "__init__.py").exists()
    assert (project_path / "app" / "controllers" / "main_controller.py").exists()
    assert (project_path / "app" / "routes" / "mains" / "__init__.py").exists()
    assert (project_path / "app" / "routes" / "mains" / "routes.py").exists()
    assert (project_path / "app" / "templates" / "base.html").exists()
    assert (project_path / "app" / "templates" / "mains" / "index.html").exists()

    expected_index_template = (
        '{% extends "base.html" %}\n'
        "\n"
        "{% block title %}Hello World | {{ super() }}{% endblock title %}\n"
        "\n"
        "{% block content %}\n"
        "    <div>Hello World</div>\n"
        "{%- endblock content %}\n"
    )

    assert (
        project_path
        / "app"
        / "templates"
        / "mains"
        / "index.html"
    ).read_text(encoding="utf-8") == expected_index_template

    assert (project_path / "app" / "static" / "src" / "input.css").exists()
    assert (project_path / "config" / "__init__.py").exists()
    assert (project_path / "config" / "base_config.py").exists()
    assert (project_path / "config" / "development_config.py").exists()
    assert (project_path / "config" / "production_config.py").exists()

    # Executable run.sh
    assert os.access(project_path / "run.sh", os.X_OK)

    # Exact content checks
    expected_main_controller = (
        "from flask import render_template\n"
        "\n"
        "class MainController:\n"
        "    def index(self) -> str:\n"
        "        return render_template('mains/index.html')\n"
    )
    assert (project_path / "app" / "controllers" / "main_controller.py").read_text(encoding="utf-8") == expected_main_controller

    expected_main_routes = (
        "from app.controllers import MainController\n"
        "from app.routes.mains import bp\n"
        "\n"
        "@bp.route('/', methods=['GET'])\n"
        "def index():\n"
        "    return MainController().index()\n"
    )
    assert (project_path / "app" / "routes" / "mains" / "routes.py").read_text(encoding="utf-8") == expected_main_routes

    run_sh = (project_path / "run.sh").read_text(encoding="utf-8")
    assert "project_path" not in run_sh
    assert f"cd {project_path}" in run_sh

def _requirements_packages(project_path):
    req = (project_path / "requirements.txt").read_text(encoding="utf-8").splitlines()
    return {line.split("==", 1)[0].strip().lower() for line in req if "==" in line}


def test_new_command_creates_project_with_db(tmp_path, monkeypatch):
    runner = CliRunner()
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(new, ["my_app"])

    assert result.exit_code == 0, result.output
    assert "cd my_app" in result.output
    assert "./run.sh" in result.output

    project_path = tmp_path / "my_app"
    _assert_common_project_scaffold(project_path, "my_app")

    expected_env = (
        "SECRET_KEY=PUT_SOMETHING_SECRET_HERE\n"
        "FLASK_APP=run.py\n"
        "FLASK_CONFIG=development\n"
        f"APP_NAME=my_app\n"
        f"SQLALCHEMY_DEVELOPMENT_DATABASE_URI=sqlite:///{project_path}/my_app_dev.db\n"
        f"SQLALCHEMY_PRODUCTION_DATABASE_URI=mysql+pymysql://username:password@localhost:3306/my_app_prod\n"
    )
    assert (project_path / ".env").read_text(encoding="utf-8") == expected_env

    assert (project_path / "app" / "models").is_dir()
    assert (project_path / "app" / "models" / "__init__.py").read_text(encoding="utf-8") == "from .user import User\n"

    user_model = (project_path / "app" / "models" / "user.py").read_text(encoding="utf-8")
    assert "class User(UserMixin, db.Model):" in user_model
    assert "__tablename__ = 'users'" in user_model
    assert "@login_manager.user_loader" in user_model

    app_init = (project_path / "app" / "__init__.py").read_text(encoding="utf-8")
    assert "from flask_login import LoginManager" in app_init
    assert "from flask_migrate import Migrate" in app_init
    assert "from flask_sqlalchemy import SQLAlchemy" in app_init
    assert "from app import models" in app_init

    pkgs = _requirements_packages(project_path)
    assert "flask" in pkgs
    assert "python-dotenv" in pkgs
    assert "flask-login" in pkgs
    assert "flask-migrate" in pkgs
    assert "flask-sqlalchemy" in pkgs

    # DB path created by flask db init
    assert (project_path / "migrations").exists()

    _assert_app_factory_renders_starter_template(project_path)
    _assert_user_model_crud_helpers(project_path)

def test_new_command_creates_project_without_db(tmp_path, monkeypatch):
    runner = CliRunner()
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(new, ["my_app", "--no-db"])

    assert result.exit_code == 0, result.output
#     assert "cd my_app" in result.output
    assert "./run.sh" in result.output

    project_path = tmp_path / "my_app"
    _assert_common_project_scaffold(project_path, "my_app")


    expected_env = (
        "SECRET_KEY=PUT_SOMETHING_SECRET_HERE\n"
        "FLASK_APP=run.py\n"
        "FLASK_CONFIG=development\n"
        f"APP_NAME=my_app\n"
    )
    assert (project_path / ".env").read_text(encoding="utf-8") == expected_env

    expected_env_example = (
        "SECRET_KEY=\n"
        "FLASK_APP=\n"
        "FLASK_CONFIG=\n"
        "APP_NAME=\n"
    )
    assert (project_path / ".env.example").read_text(encoding="utf-8") == expected_env_example

    assert not (project_path / "app" / "models").exists()
    assert not (project_path / "migrations").exists()

    app_init = (project_path / "app" / "__init__.py").read_text(encoding="utf-8")
    assert "from app import models" not in app_init

    # Desired no-db behavior assertions:
    assert "from flask_login import LoginManager" not in app_init
    assert "from flask_migrate import Migrate" not in app_init
    assert "from flask_sqlalchemy import SQLAlchemy" not in app_init

    pkgs = _requirements_packages(project_path)
    assert "flask" in pkgs
    assert "python-dotenv" in pkgs
    assert "flask-login" not in pkgs
    assert "flask-migrate" not in pkgs
    assert "flask-sqlalchemy" not in pkgs

    _assert_app_factory_renders_starter_template(project_path)

def test_new_command_fails_if_project_exists(tmp_path, monkeypatch):
    runner = CliRunner()
    monkeypatch.chdir(tmp_path)

    # Pre-create the project directory
    (tmp_path / "existing_project").mkdir()

    result = runner.invoke(new, ["existing_project"])

    assert result.exit_code == 0, result.output
    assert "already exists" in result.output

def test_new_command_cleans_up_on_exception(tmp_path, monkeypatch):
    runner = CliRunner()
    monkeypatch.chdir(tmp_path)

    def boom(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr("flask_commands.commands.new.create_venv", boom)

    result = runner.invoke(new, ["broken_project"])

    assert result.exit_code == 1
    assert not (tmp_path / "broken_project").exists()
    assert "Project Creation Failed" in result.output
    assert "boom" in result.output

def test_new_command_exception_before_project_directory_exists_does_not_cleanup(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    blocking_file = tmp_path / "taken"
    blocking_file.write_text("not a directory", encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(new, ["taken/my_app"])

    assert result.exit_code != 0
    assert "Project Creation Failed" in result.output
    assert "Not a directory" in result.output or "not a directory" in result.output

    assert blocking_file.exists()
    assert not (tmp_path / "taken" / "my_app").exists()

def test_docs_starting_a_project_create_project_with_flask_new(tmp_path, monkeypatch):
    runner = CliRunner()
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(new, ["myproject"])

    assert result.exit_code == 0, result.output
    project = tmp_path / "myproject"
    _assert_common_project_scaffold(project, "myproject")


def test_docs_starting_a_project_create_project_without_database(tmp_path, monkeypatch):
    runner = CliRunner()
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(new, ["myproject", "--no-db"])

    assert result.exit_code == 0, result.output
    project = tmp_path / "myproject"
    _assert_common_project_scaffold(project, "myproject")
    assert not (project / "app" / "models").exists()
    assert not (project / "migrations").exists()
