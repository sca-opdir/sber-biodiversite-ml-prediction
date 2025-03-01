---
layout: page
permalink: /apprentissage/
title: Apprentissage
---

## Exploration des données

Avant de plonger dans la mise en place des modèles neuronaux, il me semblait utile de visualiser les données à disposition pour mieux comprendre leur structure et leur distribution. Quelques analyses préliminaires ont donc été effectuées dans ce [notebook](https://www.kaggle.com/code/mzufferey/sber-explore-p-turage-data). 

Par exemple, ci-dessous les résultats obtenus par analyse en composantes principales : 

<div align="center">
  <img src="{{site.baseurl}}/images/acp_predicteurs.png" alt="ACP sur les variables environnementales et poids des prédicteurs" width="600"/>
</div>


## Prédiction de la qualité (Plus/Moins) à partir des variables environnementales

Les analyses décrites dans cette section ont été conduites depuis ce [notebook](https://www.kaggle.com/code/mzufferey/sber-data-vm-p-turage-corrv4).

#### Le modèle neuronal

J'ai utilisé le module `torch` pour construire un simple modèle neuronal à propagation avant. Les entrées du modèle sont les 21 variables environnementales. La couche de sortie, de taille 2, donne un score (logit) pour chacune des classes (PâtPlus/PâtMoins). La fonction softmax est ensuite utilisée pour convertir les scores bruts en probabilités, qui s'additionnent à 1 pour chaque échantillon. Le label prédit retenu est logiquement celui dans la valeur est supérieure à 0.5.

Plusieurs valeurs ont été testées comme taille de la couche intermédiaire (32, 64, 128). Etant donné que certaines des variables prédictives étaient corrélées (**voir la matrice de corrélations** matrice_corrélations_prédicteurs.png), j'ai également inclus du dropout dans le modèle étant donné que cette méthode "contributes a regularization effect which helps neural networks (NNs) explore functions of lower-order interactions \[...\] by reducing the effective learning rate of higher-order interactions" (Lengerich et al. [2022](https://proceedings.mlr.press/v151/lengerich22a/lengerich22a.pdf)). 

En outre, il y avait un certain déséquilibre dans les données étiquetées (23136 PâtMoins, 83736 PâtPlus). J'ai traité ce problème en utilisant une fonction de perte pondérée.


```python
class DropoutFeedForwardNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, dropout_rate=0.5):
        super(DropoutFeedForwardNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(p=dropout_rate)  # Utilisation du taux passé en argument
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.fc2(out)
        return out
```

#### Résultats de l'apprentissage

Je renvoie au [notebook](https://www.kaggle.com/code/mzufferey/sber-data-vm-p-turage-corrv4) pour les résultats détaillés. En bref, de façon attendue, augmenter la taille de la couche cachée améliore les résultats.

<div align="center">
  <img src="{{site.baseurl}}/images/train_val_auc_16-128.png" alt="Résultats couche cachée de 16 à 128 unités" width="600"/>
</div>

Les résultats obtenus, trop "parfaits" (ci-dessous : les courbes d'apprentissage pour une couche cachée de 128 neurones) pointent vers un problème dans les données ou dans l'implémentation de l'apprentissage. 

<div align="center">
  <img src="{{site.baseurl}}/images/all_curves_h128.png" alt="Courbes d'apprentissage pour la couche cachée de 128 unités" width="600"/>
</div>

Pour vérifier s'il y avait un problème dans le modèle, j'ai répété l'analyse en "randomizant" les labels des données d'entrainement. Comme attendu (espéré) dans ce cas-là, l'apprentissage peine à converger et la prédiction revient à un assignement aléatoire. Ceci semble indiquer quand le processus d'apprentissage est correctement implémenté.

<div align="center">
  <img src="{{site.baseurl}}/images/Training Curves_random.png" alt="Courbes d'apprentissage pour les données 'randomizée'" width="600"/>
</div>

J'ai ensuite vérifié les données, notamment s'il n'y avait pas de contamination (présence d'échantillons identiques dans les jeux de données d'entrainement et de test). J'ai également vérifié qu'il n'y avait aucun chevauchement de longitude/latitude entre les différents jeux de données. Finalement, j'ai également reproduit les analyses en sous-échantillonnant la catégorie surreprésentée afin d'évaluer si le déséquilibre de classes pouvait biaiser le résultat. Ces vérifications n'ont pas révélé d'anomalies et <span style="color: red;">des vérifications sont encore actuellement en cours pour éclaircir ce point et mieux comprendre les résultats obtenus</span>.

### Résultat sur le set de données labellisées

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



<!-- [x/dt2pred.shape[0] for x in dt2pred['predicted_label'].value_counts()]
[0.7801568048377456, 0.21984319516225434] -->

En regardant la <a href="{{site.baseurl}}/images/all_curves_h128.png">distribution des variables environnementales</a>, on remarque que les pixels pour lesquelles la prédiction a été erronnée montrent un décalage des courbes pour les variables relatives au sol (edaph_eiv_r, edaph_eiv_n) et topographique (alti3d_aspect_median, alti3d_hillshade_median, alti3d_dem_median) qui pourrait peut-être expliquer en partie les difficultés de prédiction.

#### Résultats de la prédiction sur les données sans label

<!-- [x/dt_scaled.shape[0] for x in dt_scaled['label'].value_counts()]
[0.7835167302941837, 0.2164832697058163] -->

| predicted label  |   |
| --- | ---: |
| **PâtPlus** | 44380 |
| **PâtMoins** | 12506 |



#### Evaluation de la prédiction

Des analyses similaires ont été effectuées en utilisant directement les données de relevés ([notebook](https://www.kaggle.com/code/mzufferey/sber-nn-relev-s-p-t)) ainsi qu'en utilisant un modèle non neuronal (régression logistique, [notebook](https://www.kaggle.com/code/mzufferey/sber-data-logreg-p-turage)). La concordance entre les résultats a été évaluée et s'est révélée plutôt faible ([notebook](https://www.kaggle.com/code/mzufferey/cmp-p-turages-output)). 


## Prédiction de la qualité (Plus/Moins) à partir des données satellites


Les analyses décrites dans cette section ont été conduites depuis ce [notebook](https://www.kaggle.com/code/mzufferey/ffn-sber-paturagev4-sentinel).


#### Le modèle neuronal


#### Résultats de l'apprentissage

#### Résultats de la prédiction


#### Evaluation de la prédiction


#### References

* Lengerich B.,  Xing E. P. and Caruana R. Dropout as a Regularizer of Interaction Effect ([2022](https://proceedings.mlr.press/v151/lengerich22a/lengerich22a.pdf)). Proceedings of the 25th International Conference on Artificial Intelligence and Statistics (AISTATS), Valencia, Spain. PMLR: Volume 151.

