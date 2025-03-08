---
layout: page
title: Résultats
permalink: /results/
---

## Résultat sur le set de données labellisées

**Taux de prédiction (%)**

| true_label | PâtMoins | PâtPlus |
| --- | ---: | ---: |
| **predicted_label PâtMoins** | 99.69 | 0.31 |
| **predicted_label PâtPlus** | 0.05 | 99.95 |

**Nombre de prédictions (comptage)**

| true_label  | PâtMoins | PâtPlus |
| --- | ---: | ---: |
| **predicted_label PâtMoins** | 23094 | 72 |
| **predicted_label PâtPlus** | 42 | 83664 |

En analysant la carte des erreurs de prédictions

<div align="center">
  <img src="{{site.baseurl}}/images/erreurs_PlusFalse.png" alt="Pixels classifiés 'Plus' de façon erronnée" width="600"/>
</div>


<div align="center">
  <img src="{{site.baseurl}}/images/erreurs_MoinsFalse.png" alt="Pixels classifiés 'Moins' de façon erronnée" width="600"/>
</div>

<!-- [x/dt2pred.shape[0] for x in dt2pred['predicted_label'].value_counts()]
[0.7801568048377456, 0.21984319516225434] -->

Par ailleurs, en regardant la <a href="{{site.baseurl}}/images/train2pred_correct-false_dist.png">distribution des variables environnementales</a>, on remarque que les pixels pour lesquelles la prédiction a été erronnée montrent un décalage des courbes pour les variables relatives au sol (edaph_eiv_r, edaph_eiv_n) et topographique (alti3d_aspect_median, alti3d_hillshade_median, alti3d_dem_median) qui pourrait peut-être expliquer en partie les difficultés de prédiction pour ces pixels-là.

## Résultats de la prédiction sur les données sans label

Le modèle entrainé a ensuite été utilisé pour de l'inférence sur les pixels des polygones de pâturages jamais évalués sur le terrain.

<!-- [x/dt_scaled.shape[0] for x in dt_scaled['label'].value_counts()]
[0.7835167302941837, 0.2164832697058163] -->

| predicted label  |   |
| --- | ---: |
| **PâtPlus** | 44380 |
| **PâtMoins** | 12506 |

En regardant les cartes obtenues, nous pouvons voir certains résultats 'logiques', par exemple le comblement de zones 'Plus' (resp. 'Moins') par des pixels prédits 'Plus' (resp. 'Moins'). 

<div align="center">
  <img src="{{site.baseurl}}/images/nevereval_logic.png" alt="Résultats des prédictions 'attendus'" width="600"/>
</div>

Mais il faut toutefois reconnaitre que certains résultats sont plus difficiles à interpréter, par exemple lorsqu'un pixel est prédit 'Plus' (resp. 'Moins') dans une zone de pixels 'Moins' (resp. 'Plus').

<div align="center">
  <img src="{{site.baseurl}}/images/nevereval_weird.png" alt="Résultats des prédictions plus difficiles à interpréter" width="600"/>
</div>

Il est prévu de confronter la carte des prédictions avec les résultats des contrôles terrain de cette année.


## Importance des variables sur les poids du modèle

Afin de tenter d'interpréter le modèle obtenu, j'ai regardé l'importance des variables prédictives en récupérant les poids de la première couche du modèle.


<div align="center">
  <img src="{{site.baseurl}}/images/importance_poids_modele.pn" alt="Poids des variables dans la première couche" width="600"/>
</div>



## Analyses complémentaires

Afin de consolider les résultats obtenus avec ce jeu de données environnementales, j'ai conduit des analyses similaires en adoptant d'autres approches méthodologiques
* étant donné qu'une des variables dominait fortement dans les poids de la première couche, mêmes jeux de données mais en enlevant certaines variables environnementales prédictives (pour tester si la variable avec le plus d'importance pouvait "fausser" les résultats),
* mêmes jeux de données mais une approche non neuronale, i.e. régression logistique ([notebook](https://www.kaggle.com/code/mzufferey/sber-data-logreg-p-turage)) ; les résultats montrant une certaine instabilité (absence de convergence), probablement due à la forte corrélation entre certains prédicteurs, j'ai répété l'analyse en enlevant les prédicteurs les plus fortement corrélés ([notebook](https://www.kaggle.com/code/mzufferey/sber-data-logreg-p-turage-lessvariables)),
* remplacer les données de contrôles au format "polygones" par les données brutes type "relevés" ([notebook](https://www.kaggle.com/code/mzufferey/sber-nn-relev-s-p-t)),
* remplacer les variables environnementales par des données sentinel-2 ([notebook](https://www.kaggle.com/code/mzufferey/ffn-sber-paturagev4-sentinel).

 La concordance entre les résultats a été évaluée et s'est révélée plutôt faible ([notebook](https://www.kaggle.com/code/mzufferey/cmp-p-turages-output)). 


<div align="center">
  <img src="{{site.baseurl}}/images/sentinel_apprentissage.png" alt="Résultats de la régression logistique avec un jeu restreint de prédicteurs" width="600"/>
</div>




<div align="center">
  <img src="{{site.baseurl}}/images/logreg_results.png" alt="Résultats de la régression logistique avec un jeu restreint de prédicteurs" width="600"/>
</div>

*Interprétation des résultats de la régression logistique*
- L'intercept élevé montre que la base du modèle favorise la catégorisation PâtPlus, ce qui n'est pas surprenant étant donné le déséquilibre des classes (à noter que le *class imbalance* a été pris en compte pour la construction du modèle).
- La probabilité d'être PâtPlus augmente lorsque les valeurs de pente (topo_alti3d_slope_median), humus (edaph_eiv_h) et surtout phosphore (edaph_modiffus_p) augmente. De façon intéressante, une méta-analyse a mis en évidence le lien entre disponibilité en phosphore du sol et diversité végétale ([Chen et al. 2022](https://doi.org/10.1038/s41559-022-01794-z)).
- L'absence de qualité biologique est favorisée par une végétation dense (indices de végétation élevés ; toutefois leur interprétation n'est pas si [directe](https://docs.up42.com/help/spectral-indexes)) et une forte humidité du sol (edaph_eiv_f).
- Ces résultats sont en partie en tout cas cohérents avec les observations de terrain.


