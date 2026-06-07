import time
from importlib import reload

import pytest
from playwright.sync_api import sync_playwright

# step 1: Choose Browser / Supported Browser
Supported_Browsers = ["Firefox", "Chrome", "Webkit", "Safari"]

# Step 2: Define The Browser
Browser_Name = "firefox"

# STep 3: URL
URL = " https://automation.ebrahimhossain.com.bd/hovers.html"
Headless = False
# Step 4: Setup + Teardown

@pytest.fixture(scope="class")
def setup(request):
    print(f"Starting {Browser_Name} browser .....")

    # Step 5: Start Playwright
    playwright = sync_playwright().start()

    # step 6: Browser Launch
    if Browser_Name == "chromium":
        browser = playwright.chromium.launch(headless=Headless)
    elif Browser_Name == "firefox":
        browser = playwright.firefox.launch(headless=Headless)
    elif Browser_Name == "webkit":
        browser = playwright.webkit.launch(headless=Headless)
    else:
        raise ValueError(f"Browser_Name {Browser_Name} not supported")

    # Step 7: Create Browser Context
    context = browser.new_context()

    # Step 8: Create a New Page
    page = context.new_page()

    # Viewport Set
    page.set_viewport_size({"width": 1920, "height": 1080})

    # Step 9: Open the URL
    page.goto(URL)

    request.cls.page = page

    # YIELD = test run here
    yield

    # Teardown
    context.close()
    browser.close()
    playwright.stop()


@pytest.mark.usefixtures("setup")
class TestNestedMenu:
    def test_nested_menu_hover(self):

        first_layer = self.page.get_by_test_id("tree-menu-root")
        first_layer.hover()
        self.page.wait_for_timeout(2000)

        second_layer = self.page.get_by_test_id("tree-l2-electronics")
        second_layer.hover()
        self.page.wait_for_timeout(2000)

        third_layer = self.page.get_by_test_id("tree-l3-audio")
        third_layer.hover()
        self.page.wait_for_timeout(2000)
