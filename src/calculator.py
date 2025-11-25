import math


class AdvancedCalculator:
    """
    Calculatrice avancée implémentant les opérations de base, la puissance,
    le modulo, la factorielle, et la vérification de nombres premiers.
    """

    def add(self, a, b):
        """Additionne deux nombres."""
        return a + b

    def subtract(self, a, b):
        """Soustrait b de a."""
        return a - b

    def multiply(self, a, b):
        """Multiplie deux nombres."""
        return a * b

    def divide(self, a, b):
        """Divise a par b. Gère la division par zéro."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def power(self, base, exponent):
        """Calcule la puissance : base ** exponent."""
        return base ** exponent

    def modulus(self, a, b):
        """Calcule le reste de la division (modulo)."""
        if b == 0:
            raise ValueError("Cannot perform modulus with zero divisor")
        return a % b

    def factorial(self, n):
        """Calcule la factorielle d'un entier non négatif."""
        if not isinstance(n, int):
            raise TypeError("Factorial input must be an integer")
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")

        if n == 0:
            return 1
        return math.factorial(n)

    def is_prime(self, n):
        """Vérifie si un nombre est premier."""
        if not isinstance(n, int):
            raise TypeError("is_prime input must be an integer")

        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False

        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2

        return True