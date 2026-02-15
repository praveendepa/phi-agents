import json
import os
import glob


def test_readme_exists_and_nonempty():
    path = os.path.join(os.path.dirname(__file__), os.pardir, "README.md")
    path = os.path.abspath(path)
    assert os.path.exists(path), f"README.md not found at {path}"
    assert os.path.getsize(path) > 0, "README.md is empty"


def test_config_json_valid():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    cfg = os.path.join(root, "config.json")
    assert os.path.exists(cfg), "config.json missing"
    with open(cfg, "r") as f:
        data = json.load(f)
    # Expect at least one of the known env blocks
    assert "local" in data or "cloud" in data, "config.json missing expected keys"


def test_functions_files_declare_factories():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "src/phi_agents/functions"))
    # Only check files that follow the agent factory naming pattern
    pyfiles = glob.glob(os.path.join(root, "*_agent.py"))
    assert pyfiles, "No agent factory files found in src/phi_agents/functions matching '*_agent.py'"
    # For each agent file, ensure it declares at least one 'def ' and references 'Agent(' to match repo pattern
    for p in pyfiles:
        with open(p, "r") as f:
            content = f.read()
        assert "def " in content, f"No function definitions found in {p}"
        assert "Agent(" in content or "Agent (" in content, f"No Agent(...) usage found in {p}"


def test_requirements_mentions_core_deps():
    req = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), "src/phi_agents/requirements.txt")
    assert os.path.exists(req), "requirements.txt not found"
    with open(req, "r") as f:
        txt = f.read().lower()
    assert "agno" in txt, "requirements.txt does not mention 'agno'"


def test_supervisor_agent_exists():
    """Test that the supervisor agent is created and properly configured."""
    supervisor_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "src/phi_agents/functions/supervisor_agent.py"))
    assert os.path.exists(supervisor_path), "supervisor_agent.py not found"
    
    with open(supervisor_path, "r") as f:
        content = f.read()
    assert "def supervisor_agent" in content, "supervisor_agent() function not found"
    assert "Agent(" in content, "Agent(...) not used in supervisor_agent.py"
    assert "Supervisor" in content, "Supervisor agent name not found"


def test_supervisor_documentation_exists():
    """Test that supervisor agent documentation is present."""
    doc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, ".github/agents/supervisor.agent.md"))
    assert os.path.exists(doc_path), "supervisor.agent.md documentation not found"
    
    with open(doc_path, "r") as f:
        content = f.read()
    assert "Supervisor Agent" in content, "Supervisor Agent title not found in documentation"
    assert "orchestrat" in content.lower(), "Documentation does not mention orchestration"

