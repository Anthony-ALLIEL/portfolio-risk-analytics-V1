# Portfolio Risk Analytics (Version 1.0)

## Introduction : À quoi sert ce projet ?
Ce projet est un **moteur d'analyse quantitative et de gestion des risques (Risk Management)**. Il permet à un gérant de portefeuille ou à un analyste d'auditer instantanément la santé financière d'un portefeuille d'actifs.

Concrètement, le programme permet de :

* Mesurer la rentabilité et le risque (volatilité, perte maximale) du portefeuille.
* Comparer ses performances face à un indice de référence (Benchmark).
* Simuler l'impact de crises historiques majeures (Stress Testing).
* Analyser la vitesse à laquelle le portefeuille peut être revendu sur les marchés sans perturber les cours (Profil de liquidité).

---

## Pourquoi ce projet ?
Ce programme a été développé comme **projet final dans le cadre de la prestigieuse formation CS50** (Introduction to Computer Science de l'Université Harvard).

L'objectif technique principal était de s'imposer une contrainte forte : **s'entraîner au Python natif**. Le calcul d'indicateurs financiers complexes s'effectue ici sans utiliser de bibliothèques lourdes d'analyse de données comme *Pandas* ou *NumPy*. Tout le pipeline (ingestion, alignement des dates, calculs matriciels, statistiques) est codé à la main à l'aide des structures de données fondamentales de Python (listes, dictionnaires, tuples), démontrant une maîtrise approfondie de l'algorithmique et de la gestion de la mémoire.

---

## Prérequis
Le projet ayant été conçu pour être le plus léger et autonome possible, les prérequis sont minimaux :

* **Langage :** Python 3.10 ou version supérieure.
* **Outils :** Un terminal et l'outil `Git` installés (pour le clonage).
* **Librairies externes :** Aucune bibliothèque de calcul n'est requise. Le programme utilise exclusivement les modules natifs de Python (`math`, `csv`, `os`, `sys`).

---

## Explication module par module
L'architecture du projet est découpée de manière modulaire. Chaque script a un rôle unique et précis :

### `main.py` (L'Orchestrateur)
C'est le cœur du programme. Il accueille l'utilisateur, charge les fichiers de données brutes, et coordonne l'exécution en appelant successivement les 7 modules de calcul (A à G). Il centralise ensuite les résultats pour afficher un rapport d'audit propre et structuré dans la console.

### `performances.py` [MODULE A]
Il calcule les rendements quotidiens du portefeuille sur les derniers jours en faisant la somme pondérée des rendements de chaque actif. Il calcule également l'Alpha, qui est la surperformance directe du portefeuille par rapport au Benchmark (`SPY`).

### `risque_absolu.py` [MODULE B]

Ce module quantifie le risque propre du portefeuille. Il calcule la **volatilité journalière** (écart-type des rendements) et l'annualise sur une base de 252 jours de cotation. Il calcule aussi la **VaR Historique (Value at Risk) à 95%**, qui détermine la perte maximale statistique du portefeuille sur un horizon de 24 heures.

### `risque_relatif.py` [MODULE C]

Il évalue le comportement du portefeuille face au marché. Il calcule la **Tracking Error** (le risque de déviation par rapport à l'indice) et le **Beta ($\beta$)**, qui mesure la sensibilité du portefeuille : un Beta de 1.1 signifie que si le marché monte de 10%, le portefeuille a tendance à monter de 11%.

### `ratios.py` [MODULE D]

Ce module calcule les indicateurs d'efficience de la gestion :

* Le **Ratio de Sharpe** : la rentabilité obtenue par unité de risque global pris.
* Le **Ratio d'Information** : la capacité du gérant à générer de la surperformance par rapport au risque de déviation qu'il a accepté de prendre.

### `expositions.py` [MODULE E]

Il réalise une cartographie du portefeuille. Il agrège les lignes pour calculer le poids global en pourcentage du capital investi par **secteur économique** (Technologie, Finance, Santé...) et par **zone géographique** (Pays), permettant de détecter immédiatement un risque de surconcentration.

### `contributions.py` [MODULE F]

Ce module utilise la formule mathématique d'Euler pour décomposer la volatilité globale. Il attribue à chaque actif sa **contribution réelle au risque total**, en prenant en compte les corrélations. Il permet de mettre en lumière les actifs de couverture (qui réduisent le risque global du portefeuille).

### `stress_liquidite.py` [MODULE G]

Ce module gère deux aspects critiques :

1. **Stress Testing** : Il propage l'impact de krachs historiques majeurs (Bulle Internet 2000, Subprimes 2008, COVID-19 2020) sur le portefeuille via son Beta.
2. **Liquidité** : Il calcule le pourcentage du portefeuille réversible en cash à 1 jour, 2 jours et 1 semaine, sous la contrainte réglementaire de ne jamais vendre plus de 10% du volume quotidien moyen (`adv`) de chaque action.

---

## Comment exécuter le programme
Pour lancer l'analyse sur votre machine, suivez ces trois étapes simples :

1. **Cloner le projet** depuis GitHub sur votre ordinateur :
```bash
git clone https://github.com/VotrePseudo/portfolio-risk-analytics.git

2. **Naviguer dans le dossier** du projet :
```bash
cd portfolio-risk-analytics

3. **Placer vos fichiers** `portfolio.csv` et `prices.csv` dans ce dossier, puis **lancer le programme principal** :
```bash
python main.py

Le script va s'exécuter et afficher instantanément l'analyse complète directement dans votre console.
