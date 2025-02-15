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

<div align="center">
  <br>
  <img src="/images/preparation_data_controles.png" alt="données pour l'entrainement" width="200"/>
  <br>  
  <p align="center">
    <i>Exemples des données de contrôle à disposition</i>
  </p>
</div>

2. Variables environnementales
   
La qualité biologique des pâturages étant déterminée lors des contrôles en grande partie par leur composition botanique, les recherches en modélisation des communautés de plantes constituent une source d'inspiration évidente. C'est ainsi les travaux de Brun et al. ([2024](https://doi.org/10.1038/s41467-024-48559-9)) qui m'ont aiguillée sur le jeu de données SWECO25. Ce dernier fournit des cartes environnementales (>5'000 couches raster), à une résolution de 25m couvrant l'ensemble de la Suisse pour plus d'une trentaine de variables réparties dans 10 catégories (<a href="sweco25_details">voir la liste complète</a>). De façon quelque peu arbitraire, j'ai retenu les 21 variables qui me paraissaient les plus possiblement influantes sur la qualité biologique de surfaces herbagères.

<div align="center">
  <br>
  <img src="/images/preparation_data_sweco25.png" alt="données SWECO25" width="200"/>
  <br>  
  <p align="center">
    <i>Construction du jeu de données SWECO25 ([source](https://www.bafu.admin.ch/dam/bafu/fr/dokumente/biodiversitaet/praesentation/referat-antoine-guisan-bafu-tagung-30-11-23.pdf.download.pdf/Les%20mod%C3%A8les%20de%20distribution%20d%27esp%C3%A8ces%20pour%20prioriser%20l%27infrastructure%20%C3%A9cologique.pdf))</i>
  </p>
</div>

Ces données sont librement téléchargeables depuis [Zenodo](https://zenodo.org/communities/sweco25/records). Je les ai ensuite traités de la façon suivante :
- superposition des pixels fichiers .tif avec les pixels des pâturages pour la création de fichiers tif ne contenant que les pixels se superposant avec les pâturages
- assemblage des fichiers .tif des différentes variables environnementales en un seul fichier tif

3. Données satellites

N'étant pas familière avec les données sentinel-2, l'acquisition et la préparation de ces données représentent une tâche ardue. Après avoir effectué quelques laborieuses tentatives avec [sentinelhub](https://sentinelhub-py.readthedocs.io/en/latest/index.html) et envisagé de recourir à [FORCE](https://force-eo.readthedocs.io/en/latest/), je me suis finalement appuyée sur le jeu de données [swissEO S2-SR](https://www.swisstopo.admin.ch/fr/imagesatellite-swisseo-s2-sr) récemment mis en place par swisstopo qui recèle des "données optiques par satellite (Sentinel-2) utilisées pour montrer les réflectances de la surface terrestre (surface reflectance - SR) pour les quatre canaux Rouge, Vert, Bleu et proche Infrarouge avec une résolution spatiale de 10 mètres" - sur recommandation de Dr. Dominique Weber (WSL), auteur notamment des [Grassland-use intensity maps for Switzerland](https://www.envidat.ch/#/metadata/grassland-use-intensity-maps-for-switzerland) (selon lui, cela aurait été un travail conséquent et aurait demandé un ordinateur d'une certaine puissance de partir des données brutes de sentinel-2, notamment pour les aligner sur une grille de la Suisse).

Ce jeu de données contient un nombre limité de bandes, mais présente l'avantage de pré-taiter les données sentinel-2, et notamment d'assembler les différentes "tiles" qui couvrent la Suisse. En fonction de l'orbite du satellite, le territoire valaisan n'est pas toujours couvert. J'ai visuellement identifié dans la [liste des couches disponibles](https://data.geo.admin.ch/browser/index.html#/collections/ch.swisstopo.swisseo_s2-sr_v100?.language=en) celles contenant le Valais entre mai et août, période que j'estimais la plus propice pour évaluer la végétation. Au final, j'ai téléchargé les donneés pour 10 jours (format .tif), échelonnés entre le 28 mai et le 21 août 2024. Après avoir isolé les pixels qui se superposaient avec les polygones des pâturages, j'ai calculé la couverture nuageuse moyenne et retenu le jour où celle-ci était la plus faible (06.08).

4. Assemblage des données de contrôle et environnementales (resp. satellites)
   
Après avoir préparé les pixels des polygones avec les données de contrôle et les pixels des variables environnementales (resp. satellites), les deux sources de données ont été combinées en un fichier GDB où l'étiquette du pixel, ainsi que ses valeurs de variables environnementales (resp. satellites) sont stockées dans la table attributaire. 

5. Données à prédire

Le but du modèle est de pouvoir prédire la qualité de pâturages n'ayant jamais été évalués sur le terrain. J'ai donc extrait des géodonnées cantonales tous les polygones des surfaces déclarées en pâturage en 2024 et soustrait de ces surfaces les zones déjà évaluées utilisées pour la construction du modèle. Puis, ces données ont été stockées dans un fichier .gdb et préparées comme les données de contrôle, à la différence évidente que celles-là n'étaient pas étiquetées.

## Limites

- les données des variables environnementales SWECO25 ne sont pas toujours très récentes (par exemple, pour gci, ndvi et ndwi, les données remontent à 2017)

## Références

Brun, P., Karger, D.N., Zurell, D. et al. Multispecies deep learning using citizen science data produces more informative plant community models. [Nat Commun 15, 4421 (2024)](https://doi.org/10.1038/s41467-024-48559-9). 

Guisan A. Les modèles de distribution d'espèces pour prioriser l'infrastructure écologique. Présentation dans le cadre de la BAFU Tagung | Journée de l’OFEV ([2023](https://www.bafu.admin.ch/dam/bafu/fr/dokumente/biodiversitaet/praesentation/referat-antoine-guisan-bafu-tagung-30-11-23.pdf.download.pdf/Les%20mod%C3%A8les%20de%20distribution%20d%27esp%C3%A8ces%20pour%20prioriser%20l%27infrastructure%20%C3%A9cologique.pdf)).


