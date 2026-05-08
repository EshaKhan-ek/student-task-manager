import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

APP_URL = os.environ.get('APP_URL', 'http://web:5000')

@pytest.fixture(scope='module')
def driver():
    options = Options()
    options.add_argument('--headless')          # Run in headless mode (no GUI)
    options.add_argument('--no-sandbox')        # Required for Docker/CI environments
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited /dev/shm
    options.add_argument('--disable-gpu')       # Disable GPU acceleration
    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(10)
    yield drv
    drv.quit()

# ─────────────────────────────────────────────────────────────────────
# Test Case 1: Verify the application homepage loads successfully
# ─────────────────────────────────────────────────────────────────────
def test_homepage_loads(driver):
    """TC-01: Check that the homepage returns HTTP 200 and contains
    the expected page title 'Student Task Manager'."""
    driver.get(APP_URL)
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
    assert 'Student Task Manager' in driver.title, \
        f"Expected 'Student Task Manager' in title, got: {driver.title}"
    print('TC-01 PASSED: Homepage loaded successfully.')

# ─────────────────────────────────────────────────────────────────────
# Test Case 2: Add a new task and verify it appears in the task list
# ─────────────────────────────────────────────────────────────────────
def test_add_task(driver):
    """TC-02: Fill the task input form with 'Complete DevOps Assignment',
    submit it, and verify the new task appears in the task list on the page."""
    driver.get(APP_URL)
    wait = WebDriverWait(driver, 15)

    # Locate input field and submit button
    task_input = wait.until(EC.presence_of_element_located((By.NAME, 'task')))
    task_text = 'Complete DevOps Assignment'
    task_input.clear()
    task_input.send_keys(task_text)

    # Submit the form
    submit_btn = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    submit_btn.click()

    # Wait for page reload and verify the task appears
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'task-item')))
    page_body = driver.find_element(By.TAG_NAME, 'body').text
    assert task_text in page_body, \
        f"Expected '{task_text}' in page body after submission."
    print(f'TC-02 PASSED: Task "{task_text}" added and verified on page.')
