---
layout: page
title: Présentation du projet
permalink: /presentation/
---

Prédiction de la qualité biologique des pâturages par machine learning : les différentes étapes 

### Préparation des données

1. Géodonnées
   
Les données initiales contenant les résultats de contrôles terrain des surfaces de promotion de la biodiversité étaient fournies sous la forme de fichier .gdb. Dans les premières étapes il s'est agi de :

- identifier les polygones correspondant aux pâturages et, lors de superposition, ne garder que la donnée la plus récente (certaines surfaces ont pu être évaluées plusieurs années, parfois avec des résultats contradictoires)
- labelliser les données "Plus" (avec qualité, au moins 6 espèces indicatrices) / "Moins" (sans qualité)
- découper les polygones en pixel en utilisant la même grille que les données environnementales ou satellites

  preparation_data_controles.png

2. Variables environnementales
   
La qualité biologique des pâturages étant déterminée lors des contrôles en grande partie par leur composition botanique, les recherches en modélisation des communautés de plantes constituent une source d'inspiration évidente. C'est ainsi les travaux de Brun et al. ([2024](https://doi.org/10.1038/s41467-024-48559-9)) qui m'ont aiguillée sur le jeu de données SWECO25. Ce dernier fournit des cartes environnementales (>5'000 couches raster), à une résolution de 25m couvrant l'ensemble de la Suisse pour 10 catégories de variables ; en plus des fichier originaux (utilisés pour mon étude), il y a également des fichiers statistiques. Plus de XX variables sont disponibles (XXX voir la liste complète XXX). De façon quelque peu arbitraire, j'ai retenu les 21 variables suivantes qui me paraissaient les plus possiblement influantes sur la qualité biologique de surfaces herbagères : XXXXXXXX.

preparation_data_sweco25.png

Les fichiers téléchargés de XX ont été traités de la façon suivante :
- superposition des pixels fichiers .tif avec les pixels des pâturages pour la création de fichiers tif ne contenant que les pixels se superposant avec les pâturages
- assemblage des fichiers .tif des différentes variables environnementales en un seul fichier tif

3. Données satellites

N'étant pas familière avec les données sentinel-2, l'acquisition et la préparation de ces données représentent une tâche ardue. Après quelques tentatives avec sentinelhub et envisagé XXX CUBE FORCE, je me suis finalement appuyée sur les données sentinel-2 fournies par XXX.
Malheureusement, elles contiennent moins de données (seulement 4 bandes), mais cette source présente l'avantage que ...
Depuis la page XX, j'ai identifié toutes les journées qui contenaient des données pour le vallée entre le XX et le XX. Puis, j'ai calculé la couverture nuageuse et finalement gardé les données du jour où celle-ci était la plus faible.

Après avoir préparé les pixels des polygones avec les données de contrôle et les pixels des variables environnementales (resp. satellites), les deux sources de données ont été combinées en un fichier GDB où l'étiquette du pixel, ainsi que ses valeurs de variables environnementales ou satellites sont stockées dans la table attributaire. 

4. Données à prédire

Le but du modèle est de pouvoir prédire la qualité de pâturages n'ayant jamais été évalués sur le terrain. J'ai donc extrait des géodonnées cantonales les polygones des surfaces de pâturage et soustrait les surfaces déjà évaluées. Puis, ces données ont été stockées dans un fichier .gdb et préparées comme les données avec résultats, à la différence évidente que celles-là n'étaient pas étiquetées.

## Limites

- les données des variables environnementales SWECO25 ne sont pas toujours très récentes (ex. xXX)

## Références

Brun, P., Karger, D.N., Zurell, D. et al. Multispecies deep learning using citizen science data produces more informative plant community models. [Nat Commun 15, 4421 (2024)](https://doi.org/10.1038/s41467-024-48559-9). 

Guisan A. Les modèles de distribution d'espèces pour prioriser l'infrastructure écologique. Présentation dans le cadre de la BAFU Tagung | Journée de l’OFEV ([2023](https://www.bafu.admin.ch/dam/bafu/fr/dokumente/biodiversitaet/praesentation/referat-antoine-guisan-bafu-tagung-30-11-23.pdf.download.pdf/Les%20mod%C3%A8les%20de%20distribution%20d%27esp%C3%A8ces%20pour%20prioriser%20l%27infrastructure%20%C3%A9cologique.pdf)).


