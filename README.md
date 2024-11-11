# Apprentissage par Renforcement Q-Learning pour la Prédiction du Prix d'Ethereum

Ce projet applique un algorithme d'apprentissage par renforcement Q-learning pour effectuer des transactions sur Ethereum en se basant sur les données historiques de prix et des indicateurs techniques. Grâce à l'algorithme Q-learning, l'agent apprend à prendre des actions optimales (acheter, vendre, conserver) en fonction des indicateurs calculés.

## Aperçu du Projet

### Fonctionnalités

- **Indicateurs Techniques** : Calculés dans le script `crypto_indicators.py` à l'aide de la bibliothèque `ta`. Les indicateurs utilisés sont :
  - MACD (Convergence-Divergence des Moyennes Mobiles)
  - RSI (Indice de Force Relative)
  - ADX (Indice Directionnel Moyen)
  - Bandes de Bollinger
  - Momentum
- **Source de Données** : Les données historiques d'Ethereum sont stockées dans une base de données MongoDB, configurée dans `config.py`.
- **Environnement de Trading** : `trading_env.py` définit un environnement Gym personnalisé pour entraîner l'agent à trader l’Ethereum en fonction des indicateurs.
- **Agent Q-Learning** : Implémenté dans `q_learning_agent.py`, l'agent apprend des stratégies de trading optimales en utilisant Q-learning.

## Installation et Configuration

### Prérequis

Le projet nécessite les bibliothèques suivantes :

- `pandas`
- `numpy`
- `matplotlib`
- `plotly`
- `gym`
- `pymongo`
- `ta` (pour le calcul des indicateurs techniques)

Installez les dépendances avec :

```bash
pip install pandas numpy matplotlib plotly gym pymongo ta
```

### Configuration de MongoDB

1. Assurez-vous que MongoDB fonctionne avec les données historiques d'Ethereum, formatées avec des champs comme `open`, `high`, `low`, et `close`.
2. Configurez les paramètres de connexion dans `config.py` :
   - `DATABASE_NAME`
   - `COLLECTION_NAME`

### Structure des Fichiers

- **`main.py`** : Lance la boucle d'entraînement et initialise l'environnement et l'agent.
- **`trading_env.py`** : Définit l'environnement de trading basé sur la bibliothèque Gym.
- **`q_learning_agent.py`** : Implémente l'algorithme Q-learning pour la prise de décision dans les actions de trading.
- **`crypto_indicators.py`** : Calcule les indicateurs techniques et les stocke dans un DataFrame.
- **`plot_trades.py`** (à ajouter éventuellement) : Pour visualiser les trades après l'entraînement.
- **`config.py`** : Stocke les informations de connexion à MongoDB.

## Utilisation

### Étape 1 : Calcul des Indicateurs et Chargement des Données

Dans `crypto_indicators.py`, la classe `CryptoTechnicalIndicators` récupère les données historiques depuis MongoDB, calcule les indicateurs techniques et prépare le DataFrame pour l'entraînement.

### Étape 2 : Entraîner l'Agent Q-Learning

Exécutez `main.py` pour démarrer l'entraînement de l'agent sur les données historiques.

```bash
python main.py
```

Dans `main.py` :

- La classe `TradingEnv` est instanciée avec le DataFrame des indicateurs techniques.
- L’agent Q-learning s'entraîne sur plusieurs épisodes, chaque épisode représentant une période de données historiques.
- Les journaux d'entraînement sont sauvegardés dans `trades.pkl`.

### Étape 3 : Visualisation des Résultats

Après l'entraînement, vous pouvez tracer les actions de trading (achat, vente, conservation) sur un graphique pour visualiser la performance de l'agent. Utilisez `plot_trades.py` ou un script similaire avec `plotly` ou `matplotlib` pour générer des graphiques interactifs.

### Exemples de Commandes

Pour voir et analyser les décisions de trading :

1. Chargez `trades.pkl` dans un script de traçage.
2. Utilisez `plotly` ou `matplotlib` pour superposer les actions d'achat/vente sur les données de prix.

## Explication du Code

- **Environnement de Trading** (`trading_env.py`) : Environnement personnalisé qui définit les récompenses, les actions et l'espace d'états en fonction des indicateurs techniques.
- **Agent Q-Learning** (`q_learning_agent.py`) : Implémente l'algorithme Q-learning avec équilibre exploration/exploitation.
- **Calcul des Indicateurs** (`crypto_indicators.py`) : Utilise la bibliothèque `ta` pour calculer les indicateurs et organiser les données pour l'agent.
- **Configuration** (`config.py`) : Configuration centrale pour MongoDB.

## Améliorations Futures

Suggestions d'améliorations :

- **Ajouter des Indicateurs** : Expérimenter avec davantage d'indicateurs techniques.
- **Ajuster les Paramètres** : Ajuster les paramètres de Q-learning pour améliorer la performance.
- **Approfondir avec DQN ou PPO** : Explorer des méthodes d'apprentissage par renforcement avancées pour des résultats potentiellement meilleurs.
