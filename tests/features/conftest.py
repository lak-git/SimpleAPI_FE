import pytest
from driver import get_driver


@pytest.fixture(scope="function")
def driver():
    """
    Create and yield a webdriver instance. Always quit at teardown.
    """
    drv = get_driver(headless=True)  # set True for CI/headless runs
    yield drv
    try:
        drv.quit()
    except Exception:
        pass