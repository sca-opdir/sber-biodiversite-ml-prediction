---
layout: page
title: Le jeu de données SWECO25
permalink: /sweco25_details/
---

### Contenu

Développé dans le cadre du projet [ValPar.CH](https://valpar.ch/index_fr.php), ce jeu de données rassemble un grand nombre de variables (celles retenues pour mon analyse sont indiquées en vert) réparties dans 10 catégories. 

1. Géologie (“geol”) : "geotechnic" dataset ;  subsoil of Switzerland ; 30 classes

2. Topographie (“topo”) : "alti3d" dataset ; topography of Switzerland ; 4 variables (<span style="color:darkgreen;">elevation</span> = digital elevation model, <span style="color:darkgreen;">aspect</span> = slope orientation, <span style="color:darkgreen;">hillshade</span>, and <span style="color:darkgreen;">slope</span> = steepness)

3. Climat (“bioclim”)  : "chclim25" dataset ; past, current, and future climate of Switzerland ; individual precipitation and temperature over 1981-2017 period ; 30-y average climate normal (1981-2010) layers for 28 climate parameters (<span style="color:darkgreen;">tave</span> = temperature, <span style="color:darkgreen;">prec</span> = precipitation, <span style="color:darkgreen;">etp</span> = evapotranspiration, <span style="color:darkgreen;">gdd0</span> = growing days > 0) 

4. Hydrologie (“hydro”)  : 1) "gwn07 " dataset (distance to the hydrological network) ; 2)"morph" (ecomorphology of the Swiss rivers and streams), and "swisstopo" (steepness of the watercourses ) datasets. 

5. Sol (“edaph”) : 1) "eiv" dataset (local soil properties and climate conditions, 8 variables : <span style="color:darkgreen;">soil pH</span>, <span style="color:darkgreen;">nutrients</span>, <span style="color:darkgreen;">moisture</span>, moisture variability, aeration, <span style="color:darkgreen;">humus</span>, climate continentality, and <span style="color:darkgreen;">light</span>) ; 2) "modiffus" dataset (<span style="color:darkgreen;">nitrogen (n)</span> and <span style="color:darkgreen;">phosphorus (p)</span> loads)

6. Utilisation et exploitation du sol (“lulc”) : 1) "geostat25" dataset (land use and cover, 65 classes at 3 time periods) ; 2) "wslhabmap"	 (natural habitats, 41 categories (32 classes = second level and 9 groups= first level of the TypoCH classification)) 

7. Population (densité) (“pop”) : "statpop" dataset, population density for 2010-2020

8. Transports (“trans”) : 1) "tlm3d" = distance to the road network ; 2) "sonbase" dataset describes the exposure to noise levels

9. vegetation (“vege”) : 1) "copernicus" dataset (dominant leaf : 2 categories coniferous and deciduous) ; 2) "<span style="color:darkgreen;">nfi</span>" (height of the vegetation canopy, maximum, minimum, and median values) 

10. Télédetection (“rs”) : "sdc" dataset (vegetation indices : (<span style="color:darkgreen;">evi</span> (2021) = enhanced vegetation index ; <span style="color:darkgreen;">gci</span> (2021) = green chlorophyll index ; <span style="color:darkgreen;">lai</span> (2021) = leaf area index ; <span style="color:darkgreen;">ndvi</span> (2017) = normalized difference vegetation index ; <span style="color:darkgreen;">ndwi</span> (2017) = normalized difference water index) at yearly time step for 1996-2021 period, when available.


### Aperçu de la préparation de ces données

<div align="center">
  <br>
  <img src="/images/details_data_sweco25.png" alt="données SWECO25" width="200"/>
  <br>  
  <p align="center">
    <i>Construction du jeu de données SWECO25 ([source](https://doi.org/10.1038/s41597-023-02899-1))</i>
  </p>
</div>

