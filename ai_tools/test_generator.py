"""
Générateur automatique de tests à partir de spécifications Gherkin (Cucumber)
Simule l'utilisation d'un LLM pour transformer le langage naturel structuré en code de test Pytest.
"""

import re
import os
import sys
from typing import List, Dict, Optional, Tuple
from pathlib import Path
# import math # Non nécessaire ici

# --- Configuration des chemins ---
# Le générateur lit maintenant le fichier Gherkin standard
SPECS_FILE_PATH = "specs/calculator_cucumber.feature"
OUTPUT_DIR = Path("tests/generated")
OUTPUT_FILE_PATH = OUTPUT_DIR / "test_calculator_generated.py"

# Le template de base pour le fichier de tests Pytest
TEST_FILE_TEMPLATE = """
import pytest
import sys
import os 
from pathlib import Path

# CORRECTION IMPORTATION: Ajoute la racine du projet (CWD) au chemin d'importation pour Pytest.
sys.path.append(os.path.join(os.getcwd(), "src"))

# Importez la classe AdvancedCalculator depuis le module calculator.py
from calculator import AdvancedCalculator 

@pytest.fixture
def calculator():
    return AdvancedCalculator()

# --- TESTS GÉNÉRÉS AUTOMATIQUEMENT À PARTIR DE SPECS/CALCULATOR_CUCUMBER.FEATURE ---

class TestCalculatorGenerated:
{generated_tests}
"""

class TestGenerator:
    """Génère des tests pytest à partir de spécifications Gherkin (Feature/Scenario)"""

    def __init__(self, specs_file: str):
        self.specs_file = Path(specs_file)
        # Utilise la nouvelle méthode de parsing Gherkin
        self.specs: List[Dict[str, str]] = self._parse_gherkin_scenarios()

    def _parse_gherkin_scenarios(self) -> List[Dict[str, str]]:
        """Parse le fichier Gherkin standard (Scenario, Given/When/Then multi-ligne)."""
        if not self.specs_file.exists():
            print(f"Erreur: Fichier de spécifications Gherkin introuvable à {self.specs_file}")
            return []

        with open(self.specs_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        scenarios = []
        current_scenario: Optional[Dict[str, str]] = None
        current_feature = "General"

        for line in lines:
            stripped_line = line.strip()

            if not stripped_line or stripped_line.startswith('#'):
                continue

            if stripped_line.startswith('Feature:'):
                 current_feature = stripped_line.replace('Feature:', '').strip()

            # Début d'un nouveau scénario
            if stripped_line.startswith('Scenario:'):
                if current_scenario:
                    scenarios.append(current_scenario)
                current_scenario = {
                    'title': stripped_line.replace('Scenario:', '').strip(),
                    'feature': current_feature, # Ajout de la feature pour le contexte
                    'Given': '',
                    'When': '',
                    'Then': ''
                }

            elif current_scenario:
                # Stockage des étapes
                if stripped_line.startswith('Given '):
                    current_scenario['Given'] = stripped_line.replace('Given', '', 1).strip()
                elif stripped_line.startswith('When '):
                    current_scenario['When'] = stripped_line.replace('When', '', 1).strip()
                elif stripped_line.startswith('Then '):
                    current_scenario['Then'] = stripped_line.replace('Then', '', 1).strip()

        # Ajouter le dernier scénario
        if current_scenario:
            scenarios.append(current_scenario)

        return scenarios

    # Renommage pour alignement avec la structure de l'ancien générateur (mais non utilisée)
    def _parse_specifications(self) -> List[Dict[str, str]]:
        """Méthode conservée pour la compatibilité, mais redirige vers le parsing Gherkin."""
        # Dans ce cas, nous allons retourner la liste de scénarios comme une liste de dictionnaires.
        # Nous n'avons plus de 'sections' comme clés de haut niveau dans ce format.
        return self._parse_gherkin_scenarios()

    def _generate_test_name(self, scenario_title: str) -> str:
        """Génère un nom de test Pytest valide à partir du titre du scénario."""
        # Convertit le titre en snake_case
        name = scenario_title.lower()
        name = re.sub(r'[^a-z0-9]+', '_', name)
        return f"test_{name.strip('_')}"

    def _generate_test_body(self, scenario: Dict[str, str]) -> str:
        """Génère le corps du test en fonction du scénario"""

        given = scenario.get('Given', '')
        when = scenario.get('When', '')
        then = scenario.get('Then', '')

        # Génération du code
        code, docstring = self._map_scenario_to_code(scenario)

        return f'''{docstring}
        # L'instance 'calculator' est fournie par le fixture pytest
{code}'''

    def _map_scenario_to_code(self, scenario: Dict[str, str]) -> Tuple[str, str]:
        """
        Mappe un scénario Gherkin vers du code Python concret.
        La logique est adaptée pour utiliser les valeurs extraites.
        Retourne: (test_body_code, docstring)
        """
        when = scenario['When']
        then = scenario['Then']

        # Création d'une docstring structurée
        docstring = f"        \"\"\"Scenario: {scenario['title']}\n        Given {scenario['Given']}\n        When {when}\n        Then {then}\"\"\""

        # --- Extraction des Valeurs et Mappage d'Appel de Méthode ---

        # Extraction des arguments numériques dans la clause 'When'
        add_match = re.search(r"j'additionne (\-?\d+\.?\d*) et (\-?\d+\.?\d*)", when, re.IGNORECASE)
        sub_match = re.search(r"je soustrais (\-?\d+\.?\d*) de (\-?\d+\.?\d*)", when, re.IGNORECASE)
        mult_match = re.search(r"je multiplie (\-?\d+\.?\d*) par (\-?\d+\.?\d*)", when, re.IGNORECASE)
        div_match = re.search(r"je divise (\-?\d+\.?\d*) par (\-?\d+\.?\d*)", when, re.IGNORECASE)
        pow_match = re.search(r"je calcule la puissance de (\-?\d+\.?\d*) avec l'exposant (\-?\d+\.?\d*)", when, re.IGNORECASE)
        mod_match = re.search(r"je calcule le modulo de (\-?\d+\.?\d*) par (\-?\d+\.?\d*)", when, re.IGNORECASE)

        fact_match = re.search(r"je calcule la factorielle de (\-?\d+)", when, re.IGNORECASE)
        prime_match = re.search(r"je vérifie si (\-?\d+) est premier", when, re.IGNORECASE)

        # Extraction du résultat attendu
        expected_match = re.search(r"doit être (.*)|reste doit être (.*)|levée", then, re.IGNORECASE)
        expected_val_full = ""
        if expected_match:
             # Capture le contenu après 'doit être' ou 'reste doit être'
            expected_val_full = expected_match.group(1) or expected_match.group(2) if expected_match.group(1) or expected_match.group(2) else ""
            if "levée" in then.lower():
                 expected_val_full = "exception" # Marqueur pour le cas d'exception

        method_call = None

        if add_match:
            a, b = float(add_match.group(1)), float(add_match.group(2))
            method_call = f"calculator.add({a}, {b})"
        elif sub_match:
            # Soustraction : soustrais B de A -> A - B. Le deuxième groupe est A.
            a, b = float(sub_match.group(2)), float(sub_match.group(1))
            method_call = f"calculator.subtract({a}, {b})"
        elif mult_match:
            a, b = float(mult_match.group(1)), float(mult_match.group(2))
            method_call = f"calculator.multiply({a}, {b})"
        elif div_match:
            a, b = float(div_match.group(1)), float(div_match.group(2))
            method_call = f"calculator.divide({a}, {b})"
        elif pow_match:
            a, b = float(pow_match.group(1)), float(pow_match.group(2))
            method_call = f"calculator.power({a}, {b})"
        elif mod_match:
            a, b = float(mod_match.group(1)), float(mod_match.group(2))
            method_call = f"calculator.modulus({a}, {b})"
        elif fact_match:
            n = int(fact_match.group(1))
            method_call = f"calculator.factorial({n})"
        elif prime_match:
            n = int(prime_match.group(1))
            method_call = f"calculator.is_prime({n})"

        # --- Construction du Corps du Test ---

        code_lines = []

        # Cas 1: Exception attendue
        if "exception" in then.lower():

            match_error = re.search(r'exception \"(.*?)\"', then, re.IGNORECASE)
            exception_type = match_error.group(1) if match_error else 'Exception'

            # Mappage des messages d'erreur
            expected_msg = ""
            if 'divise' in when and '0' in when:
                 expected_msg = "Cannot divide by zero"
            elif 'modulo' in when and '0' in when:
                 expected_msg = "Cannot perform modulus with zero divisor"
            elif 'factorielle' in when and '-' in when:
                 expected_msg = "Factorial is not defined for negative numbers"

            code_lines.append(f"        with pytest.raises({exception_type}) as excinfo:")
            code_lines.append(f"            {method_call}")
            code_lines.append(f"        assert str(excinfo.value) == \"{expected_msg}\"")

        # Cas 2: Assertion de valeur (normale)
        elif method_call:

            code_lines.append(f"        result = {method_call}")

            if "approximativement" in then.lower():
                # Extraction de la valeur numérique de la chaîne 'approximativement X'
                number_match = re.search(r'[\d\.\-]+', expected_val_full)
                if number_match:
                    expected_num = float(number_match.group(0))
                    code_lines.append(f"        assert result == pytest.approx({expected_num})")
                else:
                    code_lines.append(f"        # ERREUR: Impossible de lire la valeur approximative de : {expected_val_full}")
                    code_lines.append("        assert False")

            elif expected_val_full in ["True", "False"]:
                # Assertion pour les booléens
                code_lines.append(f"        assert result is {expected_val_full == 'True'}")
            else:
                # Assertion pour les entiers ou décimaux directs
                try:
                    # Traiter comme un flottant si un point est présent
                    if '.' in expected_val_full:
                        expected_num = float(expected_val_full)
                        code_lines.append(f"        assert result == pytest.approx({expected_num})")
                    else:
                        expected_num = int(expected_val_full)
                        code_lines.append(f"        assert result == {expected_num}")
                except ValueError:
                    # Cas où la valeur n'est ni un nombre ni un booléen connu
                    code_lines.append(f"        # ERREUR: Valeur attendue non reconnue : {expected_val_full}")
                    code_lines.append("        assert False")

        else:
             # Scénario non mappé
            code_lines.append("        # TODO: Le scénario n'a pas pu être mappé à une fonction (manque de données)")
            code_lines.append("        pass")

        return "\n".join(code_lines), docstring


    def generate_tests(self, output_file: str):
        """Génère le fichier de tests complet"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        generated_tests = []

        # Génération des tests
        for scenario in self.specs:
            test_name = self._generate_test_name(scenario['title'])
            test_body_code, docstring = self._map_scenario_to_code(scenario)

            test_function = [
                f"\n    def {test_name}(self, calculator):",
                docstring,
                test_body_code
            ]
            generated_tests.append("\n".join(test_function))

        # Assemblage du fichier final
        final_content = TEST_FILE_TEMPLATE.format(generated_tests='\n'.join(generated_tests))

        # Écriture du fichier
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_content)

        print(f"✅ Tests générés avec succès: {output_path}")
        print(f"📊 Nombre total de tests générés: {len(self.specs)}")

        # Ajout du rappel pour l'environnement
        if not Path("tests", "__init__.py").exists():
            print("\n⚠️ ATTENTION: Pour que Pytest puisse trouver le module 'calculator' (où se trouve AdvancedCalculator), vous devez créer le fichier vide 'tests/__init__.py'.")

def main():
    """Point d'entrée principal"""
    # Utilise le nouveau fichier Gherkin standard
    generator = TestGenerator(SPECS_FILE_PATH)
    generator.generate_tests(str(OUTPUT_FILE_PATH))


if __name__ == '__main__':
    main()