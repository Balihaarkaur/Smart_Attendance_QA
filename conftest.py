import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--run-selenium",
        action="store_true",
        default=False,
        help="Run Selenium/UI tests"
    )

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "selenium: mark test as selenium/ui test"
    )

def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-selenium"):
        return

    skip_selenium = pytest.mark.skip(
        reason="Selenium tests skipped by default (use --run-selenium)"
    )

    for item in items:
        if "selenium" in item.keywords:
            item.add_marker(skip_selenium)
