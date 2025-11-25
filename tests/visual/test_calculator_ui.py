"""
Tests visuels de l'interface calculatrice avec Selenium
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pathlib import Path
import time
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from ai_tools.visual_comparator import VisualComparator


@pytest.fixture
def driver():
    """Fixture pour le driver Selenium"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def comparator():
    """Fixture pour le comparateur visuel"""
    return VisualComparator(tolerance=0.02)  # 2% de tolérance


class TestCalculatorVisual:
    """Tests visuels de la calculatrice"""

    def test_initial_state(self, driver, comparator):
        """Test de l'état initial de la calculatrice"""
        # Charger la page
        html_path = Path(__file__).parent.parent.parent / 'src' / 'calculator_ui.html'
        driver.get(f'file://{html_path.absolute()}')

        # Attendre que la page soit chargée
        time.sleep(1)

        # Prendre un screenshot
        screenshots_dir = Path(__file__).parent.parent.parent / 'screenshots'
        current_path = screenshots_dir / 'current' / 'initial_state.png'
        baseline_path = screenshots_dir / 'baseline' / 'initial_state.png'
        diff_path = screenshots_dir / 'diff' / 'initial_state_diff.png'

        current_path.parent.mkdir(parents=True, exist_ok=True)
        driver.save_screenshot(str(current_path))

        # Si baseline n'existe pas, la créer
        if not baseline_path.exists():
            comparator.create_baseline(str(current_path), str(baseline_path))
            pytest.skip("Baseline créée, relancer les tests")

        # Comparer avec la baseline
        is_match, diff_percentage, message = comparator.compare_images(
            str(baseline_path),
            str(current_path),
            str(diff_path)
        )

        assert is_match, f"Différence visuelle détectée: {message}"

    def test_after_calculation(self, driver, comparator):
        """Test après une opération de calcul"""
        html_path = Path(__file__).parent.parent.parent / 'src' / 'calculator_ui.html'
        driver.get(f'file://{html_path.absolute()}')
        time.sleep(1)

        # Effectuer un calcul: 5 + 3 =
        driver.find_element(By.XPATH, "//button[text()='5']").click()
        time.sleep(0.2)
        driver.find_element(By.XPATH, "//button[text()='+']").click()
        time.sleep(0.2)
        driver.find_element(By.XPATH, "//button[text()='3']").click()
        time.sleep(0.2)
        driver.find_element(By.XPATH, "//button[text()='=']").click()
        time.sleep(0.5)

        # Screenshot
        screenshots_dir = Path(__file__).parent.parent.parent / 'screenshots'
        current_path = screenshots_dir / 'current' / 'after_calculation.png'
        baseline_path = screenshots_dir / 'baseline' / 'after_calculation.png'
        diff_path = screenshots_dir / 'diff' / 'after_calculation_diff.png'

        driver.save_screenshot(str(current_path))

        if not baseline_path.exists():
            comparator.create_baseline(str(current_path), str(baseline_path))
            pytest.skip("Baseline créée, relancer les tests")

        is_match, diff_percentage, message = comparator.compare_images(
            str(baseline_path),
            str(current_path),
            str(diff_path)
        )

        assert is_match, f"Différence visuelle après calcul: {message}"

    def test_display_content(self, driver):
        """Test du contenu affiché (test fonctionnel en bonus)"""
        html_path = Path(__file__).parent.parent.parent / 'src' / 'calculator_ui.html'
        driver.get(f'file://{html_path.absolute()}')
        time.sleep(1)

        # Vérifier l'affichage initial
        display = driver.find_element(By.ID, 'display')
        assert display.text == '0', "Affichage initial incorrect"

        # Test de calcul
        driver.find_element(By.XPATH, "//button[text()='7']").click()
        time.sleep(0.2)
        assert display.text == '7'

        driver.find_element(By.XPATH, "//button[text()='8']").click()
        time.sleep(0.2)
        assert display.text == '78'