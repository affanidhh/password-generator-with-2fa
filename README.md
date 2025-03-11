# Générateur de Mot de Passe avec 2FA

Cette application de génération de mot de passe utilise Python et Tkinter pour fournir une interface graphique conviviale. Elle permet de générer des mots de passe sécurisés et inclut une fonctionnalité de double authentification (2FA) utilisant `pyotp` et `qrcode`.

## Fonctionnalités

- Génération de mots de passe aléatoires avec options de configuration
- Évaluation de la robustesse du mot de passe
- Sauvegarde des mots de passe générés avec chiffrement
- Exportation et importation des mots de passe en formats CSV et JSON
- Double authentification (2FA) avec codes TOTP et QR code

## Prérequis

- Python 3.x
- Bibliothèques Python : `pyotp`, `qrcode[pil]`, `pillow`, `tkinter`, `cryptography`

## Installation

Installez les bibliothèques requises :

```sh
pip install pyotp qrcode[pil] pillow cryptography
```

## Utilisation

1. Exécutez le script `password_generator_with_2fa.py` :

```sh
python password_generator_with_2fa.py
```

2. Configurez les options de génération de mot de passe dans l'interface graphique.
3. Cliquez sur "Générer" pour créer un nouveau mot de passe.
4. Sauvegardez le mot de passe si nécessaire.
5. Configurez la double authentification (2FA) en scannant le QR code avec votre application d'authentification et vérifiez le code.
6. Exportez ou importez les mots de passe en utilisant les boutons correspondants.

## Contribuer

Les contributions sont les bienvenues ! Veuillez soumettre des pull requests pour toute amélioration ou correction de bugs.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
