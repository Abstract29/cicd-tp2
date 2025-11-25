"""
Comparateur visuel d'images pour les tests
Utilise Pillow pour la comparaison pixel par pixel et génère un diff visuel
"""

from PIL import Image, ImageDraw, ImageChops
from pathlib import Path
import numpy as np
from typing import Tuple, Optional


class VisualComparator:
    """Compare deux images et génère un rapport de différences"""

    def __init__(self, tolerance: float = 0.1):
        """
        Args:
            tolerance: Pourcentage de différence acceptable (0.0 à 1.0)
        """
        self.tolerance = tolerance

    def compare_images(
            self,
            baseline_path: str,
            current_path: str,
            diff_output: Optional[str] = None
    ) -> Tuple[bool, float, str]:
        """
        Compare deux images

        Args:
            baseline_path: Chemin de l'image de référence
            current_path: Chemin de l'image courante
            diff_output: Chemin pour sauvegarder l'image de différence

        Returns:
            Tuple (is_match, difference_percentage, message)
        """
        baseline = Image.open(baseline_path)
        current = Image.open(current_path)

        # Vérifier que les images ont la même taille
        if baseline.size != current.size:
            return False, 100.0, f"Tailles différentes: {baseline.size} vs {current.size}"

        # Calculer la différence
        diff = ImageChops.difference(baseline, current)

        # Convertir en array numpy pour calcul
        diff_array = np.array(diff)

        # Calculer le pourcentage de différence
        if diff_array.size == 0:
            return True, 0.0, "Images identiques"

        # Moyenne des différences (0-255 par canal)
        mean_diff = np.mean(diff_array) / 255.0
        max_diff = np.max(diff_array) / 255.0

        # Pourcentage de pixels différents
        threshold = 10  # Seuil de différence par pixel
        diff_mask = np.any(diff_array > threshold, axis=-1) if len(diff_array.shape) == 3 else diff_array > threshold
        pixels_diff = np.sum(diff_mask)
        total_pixels = diff_mask.size
        percentage_diff = (pixels_diff / total_pixels) * 100

        # Générer l'image de différence si demandé
        if diff_output:
            self._generate_diff_image(baseline, current, diff, diff_output)

        # Déterminer si c'est un match
        is_match = percentage_diff <= (self.tolerance * 100)

        message = f"Différence: {percentage_diff:.2f}% des pixels (moyenne: {mean_diff * 100:.2f}%, max: {max_diff * 100:.2f}%)"

        return is_match, percentage_diff, message

    def _generate_diff_image(self, baseline: Image, current: Image, diff: Image, output_path: str):
        """Génère une image composite montrant baseline, current et diff"""
        width, height = baseline.size

        # Créer une image 3x plus large
        composite = Image.new('RGB', (width * 3, height), color='white')

        # Coller les images
        composite.paste(baseline.convert('RGB'), (0, 0))
        composite.paste(current.convert('RGB'), (width, 0))

        # Amplifier la différence pour la rendre visible
        diff_enhanced = diff.point(lambda x: x * 10)
        composite.paste(diff_enhanced.convert('RGB'), (width * 2, 0))

        # Ajouter des labels
        draw = ImageDraw.Draw(composite)

        # Sauvegarder
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        composite.save(output_path)

    def create_baseline(self, screenshot_path: str, baseline_path: str):
        """Copie un screenshot comme nouvelle baseline"""
        img = Image.open(screenshot_path)
        Path(baseline_path).parent.mkdir(parents=True, exist_ok=True)
        img.save(baseline_path)
        print(f"✅ Baseline créée: {baseline_path}")


def main():
    """Démonstration"""
    comparator = VisualComparator(tolerance=0.05)

    # Exemple d'utilisation
    print("Comparateur visuel initialisé avec tolérance de 5%")


if __name__ == '__main__':
    main()