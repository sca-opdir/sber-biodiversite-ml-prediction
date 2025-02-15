---
layout: page
title: Présentation du projet
permalink: /presentation/
---

Prédiction de la qualité biologique des pâturages par machine learning : les différentes étapes 

### Préparation des données

1. Géodonnées
Les données initiales contenant les résultats de contrôles étaient fournies sous la forme de fichier .gdb. Dans les premières étapes il s'est agi de :
- identifier les polygones correspondant aux pâturages et, lors de superposition, ne garder que la donnée la plus récente (certaines surfaces ont pu être évaluées plusieurs années, parfois avec des résultats contradictoires)
- découper les polygones en pixel en utilisant la même grille que les données environnementales ou satellites

2. Variables environnementales
Le jeu de données SWECO 2025 fournit des fichiers raster pour chacune des variables environnementales ; en plus des fichier originaux (utilisés pour mon étude), il y a également des fichiers statistiques. Plus de XX variables sont disponibles (XXX voir la liste complète XXX). De façon quelque peu arbitraire, j'ai retenu les 21 variables suivantes qui me paraissaient les plus possiblement influantes sur la qualité biologique de surfaces herbagères : XXXXXXXX.
Les fichiers téléchargés de XX ont été traités de la façon suivante :
- superposition des pixels fichiers .tif avec les pixels des pâturages pour la création de fichiers tif ne contenant que les pixels se superposant avec les pâturages
- assemblage des fichiers .tif des différentes variables environnementales en un seul fichier tif

3. Données satellites
N'étant pas familière avec les données sentinel-2, l'acquisition et la préparation de ces données représentent une tâche ardue. Après quelques tentatives avec sentinelhub et envisagé XXX CUBE FORCE, je me suis finalement appuyée sur les données sentinel-2 fournies par XXX.
Malheureusement, elles contiennent moins de données (seulement 4 bandes), mais cette source présente l'avantage que ...
Depuis la page XX, j'ai identifié toutes les journées qui contenaient des données pour le vallée entre le XX et le XX. Puis, j'ai calculé la couverture nuageuse et finalement gardé les données du jour où celle-ci était la plus faible.

Après avoir préparé les pixels des polygones avec les données de contrôle et les pixels des variables environnementales (resp. satellites), les deux sources de données ont été combinées en un fichier GDB où l'étiquette du pixel, ainsi que ses valeurs de variables environnementales ou satellites sont stockées dans la table attributaire. 

4. Données à prédire
Les polygones des surfaces de pâturage présentes dans les géodonnées cantonales ont été extraites sous forme de .gdb et préparées comme les données avec résultats de contrôle, à la différence évidente que celles-là n'étaient pas étiquetées.

## Limites

- les données des variables environnementales SWECO25 ne sont pas toujours très récentes (ex. xXX)


