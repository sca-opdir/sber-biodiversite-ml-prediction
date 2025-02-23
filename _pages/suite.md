---
layout: page
permalink: /suite/
title: Suite
---

#### Pistes de recherches futures

Pour étoffer ce projet, les différentes pistes de recherche ci-dessous sont envisageables :

* d'un point de vue méthodologique
    * combiner les variables environnementales et les données spatiales
    * utiliser les données spatiales dans toutes leurs dimensions à l'aide d'un CNN
    * formuler la problématique d'identification des surfaces avec qualité biologique comme un problème de segmentation à résoudre avec un CNN
    * mettre à profit la dimension temporelle
    * essayer d'autres méthodes non neuronales

* d'un point de vue des données
    * répéter les analyses pour d'autres surfaces de promotion de la biodiversité (prairies notamment)
    * évaluer les avantages/désavantages à conduire les analyses pour tous les types de SPB de façon conjointe

* obtenir la probabilité de présence des espèces végétales indicatrices avec florID


De manière plus générale, des méthodes de machine learning pourraient être utilisées pour les contrôles suivants

* plausibilité des déclarations de codes de culture : *crop mapping*


* présence d'arbres sur les parcelles déclarant des 921-925 : *tree detection*

https://github.com/shmh40/detectreeRGB cited by https://acocac.github.io/environmental-ai-book/forest/modelling/forest-modelling-treecrown_detectree.html with tutorials


* https://github.com/microsoft/torchgeo, https://torchgeo.readthedocs.io/en/stable/tutorials/pretrained_weights.html
* 
      * https://deepforest.readthedocs.io/en/v1.5.0/user_guide/11_training.html
https://github.com/weecology/DeepForest_demos/blob/master/street_tree/StreetTrees.ipynb
https://acocac.github.io/environmental-ai-book/forest/modelling/forest-modelling-treecrown_detectree.html

  https://patball1.github.io/detectree2/tutorial_multi.html  
https://patball1.github.io/detectree2/tutorial.html
https://github.com/martibosch/detectree : data from from the SWISSIMAGE WMS !

https://github.com/martibosch/swiss-urban-trees/blob/main/notebooks/train-crown.ipynb :
As noted in the user guide, the prebuilt model is trained on 400x400 images at a 10 cm resolution https://deepforest.readthedocs.io/en/v1.4.1/user_guide/10_better.html#check-patch-size

https://github.com/martibosch/swisslandstats-geopy

#### Littérature d'intérêt pour poursuivre la réflexion :

* Weber, D., Schwieder, M., Ritter, L., Koch, T., Psomas, A., Huber, N., Ginzler, C., Boch, S.. ([2024](https://doi.org/10.1002/rse2.372)). Grassland-use intensity maps for Switzerland based on satellite time series: Challenges and opportunities for ecological applications. Remote Sensing in Ecology and Conservation, Volume 10, Issue 3, 312-327.
* Dollinger, J., Brun, P., Sainte Fare Garnot, V., and Wegner, J. D.. ([2024](https://doi.org/10.5194/isprs-annals-X-2-2024-41-2024)). Sat-SINR: High-Resolution Species Distribution Models Through Satellite Imagery. ISPRS Ann. Photogramm. Remote Sens. Spatial Inf. Sci., X-2-2024, 41–48.
