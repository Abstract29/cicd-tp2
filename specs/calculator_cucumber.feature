Feature: Advanced Calculator Operations
  In order to ensure complex arithmetic operations are reliable
  As a user of the AdvancedCalculator class
  I want all basic and advanced functions to behave correctly according to mathematical rules.

  Scenario: Addition de deux nombres positifs
    Given le calculateur est prêt
    When j'additionne 10 et 5
    Then le résultat doit être 15

  Scenario: Addition d'un nombre positif et un nombre négatif
    Given le calculateur est prêt
    When j'additionne 20 et -10
    Then le résultat doit être 10

  Scenario: Addition de deux nombres décimaux
    Given le calculateur est prêt
    When j'additionne 1.5 et 2.5
    Then le résultat doit être 4.0

  Scenario: Soustraction de deux nombres positifs
    Given le calculateur est prêt
    When je soustrais 10 de 30
    Then le résultat doit être 20

  Scenario: Soustraction avec un résultat négatif
    Given le calculateur est prêt
    When je soustrais 30 de 10
    Then le résultat doit être -20
    # Note: La soustraction est normalement 10 - 30 = -20. L'étape de soustraction doit être précisée dans l'étape "When" du step definition.

  Scenario: Multiplication de deux nombres positifs
    Given le calculateur est prêt
    When je multiplie 4 par 5
    Then le résultat doit être 20

  Scenario: Multiplication par zéro
    Given le calculateur est prêt
    When je multiplie 42 par 0
    Then le résultat doit être 0

  Scenario: Multiplication de deux nombres négatifs
    Given le calculateur est prêt
    When je multiplie -4 par -5
    Then le résultat doit être 20

  Scenario: Division réussie
    Given le calculateur est prêt
    When je divise 10 par 2
    Then le résultat doit être 5.0

  Scenario: Division par zéro lève une erreur
    Given le calculateur est prêt
    When je divise 10 par 0
    Then une exception "ValueError" doit être levée

  Scenario: Division décimale précise
    Given le calculateur est prêt
    When je divise 10 par 3
    Then le résultat doit être approximativement 3.3333333333333335

  Scenario: Calcul de puissance avec exposant positif
    Given le calculateur est prêt
    When je calcule la puissance de 2 avec l'exposant 3
    Then le résultat doit être 8

  Scenario: Calcul de puissance avec exposant négatif
    Given le calculateur est prêt
    When je calcule la puissance de 2 avec l'exposant -2
    Then le résultat doit être 0.25

  Scenario: Calcul de puissance avec exposant de zéro
    Given le calculateur est prêt
    When je calcule la puissance de 50 avec l'exposant 0
    Then le résultat doit être 1

  Scenario: Calcul du Modulo (reste)
    Given le calculateur est prêt
    When je calcule le modulo de 25 par 7
    Then le reste doit être 4

  Scenario: Modulo avec diviseur zéro lève une erreur
    Given le calculateur est prêt
    When je calcule le modulo de 10 par 0
    Then une exception "ValueError" doit être levée

  Scenario: Calcul de la factorielle d'un entier positif
    Given le calculateur est prêt
    When je calcule la factorielle de 5
    Then le résultat doit être 120

  Scenario: Calcul de la factorielle de zéro
    Given le calculateur est prêt
    When je calcule la factorielle de 0
    Then le résultat doit être 1

  Scenario: Factorielle d'un nombre négatif lève une erreur
    Given le calculateur est prêt
    When je calcule la factorielle de -5
    Then une exception "ValueError" doit être levée

  Scenario: Vérification d'un nombre premier
    Given le calculateur est prêt
    When je vérifie si 17 est premier
    Then le résultat doit être True

  Scenario: Vérification d'un nombre non premier
    Given le calculateur est prêt
    When je vérifie si 9 est premier
    Then le résultat doit être False

  Scenario: Vérification d'un nombre inférieur à 2
    Given le calculateur est prêt
    When je vérifie si 1 est premier
    Then le résultat doit être False