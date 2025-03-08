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

#### Résultats de la prédiction sur les données sans label

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


## Analyses complémentaires

Afin de consolider les résultats obtenus avec ce jeu de données environnementales, j'ai conduit des analyses similaires en adoptant d'autres approches méthodologiques
* mêmes jeux de données mais en enlevant certaines variables environnementales prédictives (pour tester si la variable avec le plus d'importance pouvait "fausser" les résultats),
* mêmes jeux de données mais une approche non neuronale, i.e. régression logistique ([notebook](https://www.kaggle.com/code/mzufferey/sber-data-logreg-p-turage)) ; les résultats montrant une certaine instabilité (absence de convergence), probablement due à la forte corrélation entre certains prédicteurs, j'ai répété l'analyse en enlevant les prédicteurs les plus fortement corrélés ([notebook](https://www.kaggle.com/code/mzufferey/sber-data-logreg-p-turage-lessvariables)),
* remplacer les données de contrôles au format "polygones" par les données brutes type "relevés" ([notebook](https://www.kaggle.com/code/mzufferey/sber-nn-relev-s-p-t)),
* remplacer les variables environnementales par des données sentinel-2 ([notebook](https://www.kaggle.com/code/mzufferey/ffn-sber-paturagev4-sentinel).

 La concordance entre les résultats a été évaluée et s'est révélée plutôt faible ([notebook](https://www.kaggle.com/code/mzufferey/cmp-p-turages-output)). 




<div align="center">
  <img src="{{site.baseurl}}/images/logreg_results.png" alt="Résultats de la régression logistique avec un jeu restreint de prédicteurs" width="600"/>
</div>


Variables favorisant PâtPlus (pâturage élevé) :

edaph_eiv_h (+3.61) : Fertilité élevée → pâturage plus important.
edaph_modiffus_p (+8.08) : Phosphore du sol favorisant le pâturage.
topo_alti3d_slope_median (+1.29) : Zones en pente plus pâturées.
Variables favorisant PâtMoins (moins pâturé) :

rs_sdc_2021_evi_mean (-185.45) : Indice de végétation élevé → Moins pâturé.
rs_sdc_2017_ndvi_mean (-3.91) : Végétation dense → Moins pâturé.
edaph_eiv_f (-3.23) : Sols humides → Moins pâturé.

PâtPlus (classe positive, y=1) ou PâtMoins (y=0).

Intercept (const)	90.08	Grande constante indiquant que la base du modèle favorise fortement PâtPlus.
rs_sdc_2017_ndvi_mean	-3.91	Plus la végétation est dense en 2017 (NDVI élevé), plus c’est PâtMoins. Un NDVI élevé indique peu de stress végétal, ce qui peut suggérer une absence de pâturage intense.
edaph_eiv_h	+3.61	Favorise PâtPlus. Une fertilité élevée des sols peut attirer plus de pâturage.
topo_alti3d_aspect_median	-0.87	Influence négative sur PâtPlus, les orientations spécifiques du terrain peuvent limiter le pâturage (exemple : versants moins accessibles).
edaph_eiv_f	-3.23	Plus le sol est humide (eiv_f élevé), moins la zone est pâturée (PâtMoins). Un sol trop humide peut être peu favorable au pâturage.
rs_sdc_2021_evi_mean	-185.45	Très fort impact négatif : une augmentation de l'indice de végétation en 2021 (EVI) réduit fortement la probabilité d’être PâtPlus. Un EVI élevé peut signaler une végétation dense et peu pâturée.
topo_alti3d_slope_median	+1.29	Plus la pente est forte, plus la zone est pâturée (PâtPlus). Contre-intuitif, mais pourrait s’expliquer par des espèces spécifiques adaptées aux zones en pente.
edaph_modiffus_n	+0.17	Pas significatif (p=0.742), donc aucune interprétation fiable.
edaph_modiffus_p	+8.08	Très forte influence positive sur PâtPlus. La richesse en phosphore favorise probablement la croissance d’herbes appétentes pour les herbivores.
