# Sucker analysis

This project studies the adhesion of arrays of millimeter-sized suction cups made from polydimethylsiloxane. Repository contains both data obtained in this project and code used to analyse said data.

## Table Of Contents

- [Introduction](#Introduction)
- [Fabrication](#Fabrication)
- [Measurements](#Measurements)
- [About the data](#about)
     - [Content CSV files](#dat) 
     - [Experiments](#exp)
          - [Preload series](#preload)
          - [Retraction speed series](#retraction)
          - [Array size series](#array)
          - [Thin backing layer](#backing)
          - [Cut backing layer](#cut)
- [Zeekat library](#Zeekat)
- [Scripts for analysis](#scripts)
     - [Fitting and plots](#fitting)
     - [Detachment quantum distribution](#detachment)



## <a name="Introduction"></a> Introduction

Patterned surfaces are known to show superior adhesive properties compared to continuos surfaces. [1] Animals such as geckos use patterned surfaces to climb. Many aritficial bio-inspired patterned adhesive surfaces have been made. We make and study arrays of millimeter-sized suction cups, inspired by the surfaces found on cephalopods for applications in soft robotics. This research was carried out at the Laboratory of Physical Chemistry & Soft Matter at Wageningen University & Research and funded by 4TU.Federation through the program 'Soft Robotics' with Grant No. 4TU-UIT-335. This repository contains all data that was collected in this project as well as the code used to analyse it. This document contains detailed information about how the data was acquired.


## <a name="Fabrication"></a> Fabrication
We use a double-negative mold to make the samples. A positive mold is made by 3D-printing (1). We cast this mold with Dragon Skin &trade; (2) to obtain a soft, negative mold. This mold is coated with fluor polymers to allow for the release of the sample from the mold later (3). We then pour Ecoflex &trade; in the mold after which we degas the liquid Ecoflex &trade; for 15 minutes to ensure no bubbles are present in our sample(4). We cure the Ecoflex &trade; at room temperature for 24 hours before peeling it from the mold to obtain our final sample (5). This sample was connected to a glass microscope slide by plasma bonding. 

<img src="https://user-images.githubusercontent.com/115638429/211778798-6e8c12da-0609-40a9-8d09-609569a7ac57.png" width=50% height=50%>


The figure below shows the geometry of the suction cups.

<img src="https://user-images.githubusercontent.com/115638429/211783580-20ed9f20-d98c-4cd4-afcd-09e351d37080.png" width=20% height=20%>


## <a name="Measurements"></a> Measurements

All measurements were performed using an Anton Paar MCR-501 rheometer. A glass plate accessory (P-PTD120/GL) was used as a countersurface to the suction cups. Samples were glued to a custom-made 3D-printed probe. A sample was placed on the countersurface with the cups facing down after which glue was placed on the sample (1). The probe was lowered so it is only in contact with the glue, after which the glue is cured by UV-light (2). This procedure aims to align the sample perfectly with the glass countersurface and is visualized below. 

![confinement](https://user-images.githubusercontent.com/115638429/211790352-ae902d75-9e3a-4d72-8a2c-8e93ca8150d9.png)

One measurement cycle consists of four distinct phases, visualized below. The first phase is the approach (1 & 2) where the probe approaches the countersurface until a certain force is detected. The force by which we indent the sample to the countersurface is called the preload. The next phase is the relaxation phase, where the probe does not move for 20 seconds (3). AFter the relaxation, retraction starts. The probe pulls the sample away from the countersurface at a certain speed that we call the retraction speed (4 & 5). After the sample has detached completely from the countersurface, a short transition phase happens where the retraction ends and approach is initiated. Generally, we repeat this cycle multiple times for each experiment. For information about the preload, retraction speed and number of cycles that correspond to each dataset, see [About the data](#about). 

![Expopzet](https://user-images.githubusercontent.com/115638429/211790927-e9ab5a05-e07a-4d3e-a7f4-dcec078bb192.png)

It is important to note that each phase has its own CSV file in the raw data, indicated by the interval in the file name. The first interval corresponds to the indentation phase, the second interval to the relaxation phase, the third interval to the retraction phase and the fourht interval to the transition phase. In a folder with interval ranging from 1 to 40, ten complete cycles of measurement have been performed.


## <a name="about"></a> About the data

### <a name="dat"></a> Content CSV files

The CSV files contain four columns. The first column, 'Point No.', simply gives an index to each data point. The column 'Normal Force [N]' gives the force measured by the rheometer in Newton. The adhesive force that resists the retraction is negative. The column 'Gap [mm]' gives the distance between the probe and the countersurface. Note that this distance also includes the sample itself and the distance should therefore be normalized. The fourth column 'Time [s]' gives the time in seconds. 

The filenames contain information about the metadata. For example:
Eco_P3_FN1.0_v_onespeed_Interval_7.csv
'Eco' indicates that the sample was made from Ecoflex &trade;. 'P3' indicates that the sample had a periodicity of 3 mm, which means that there was 3 mm between neighbouring suction cups on the array and this is a unit of feature density. Three periodicities were used: 2.5 mm, 3 mm and 4 mm. 'FN1.0' indicates that the preload was 1.0 N in this experiment. 

### <a name="exp"></a> Experiments


#### <a name="preload"></a> Preload series

This data was obtained to study the influence of the preload on detachment behaviour in our system. Three samples were used, each with a different feature density. Note that the three samples did not have the same number of cups. The P2.5 sample had 110 cups, the P3 sample had 80 cups and the P4 sample had 42 cups. The backing layer was approximately 4 mm thick for all samples and the retraction speed was 500 µm/s for all measurements. The preload was varied and the preload in Newton is indicated in each filename by the 'FNx' part.


#### <a name="retro"></a> Retraction speed series

This data was obtained to study the influence of the retraction speed on detachment behaviour in our system and some interesting phenomena can be seen in this data. The same three samples were used that were also used in the preload series experiment. The preload was 4 N for all measurements and the retraction speed was varied. The retraction speed is indicated by the 'retrSpdx' part in the filename. 

#### <a name="array"></a> Array size series

This data was obtained to study the influence of the number of cups in an array on the detachment behaviour. A P3 sample with 80 cups was taken and measurements were made after which two rows of cups (one row in each dimension of the lattice) were cut off from the sample. This was repeated until only 3 cups remained. The retraction speed was 500 µm/s for all measurements. The preload per cup was kept the same for all measurements and was 0.05 N per cup (so 4 N for 80 cups). The number of cups for each measurement is indicated in the filename by the 'cupp_x' part. 

#### <a name="backing"></a> Thin backing layer

This data was obtained to study the influence of the thickness of the backing layer on the detachment behaviour in our system. A P2.5 sample was made with 121 cups and a bakcing layer of 0.31 mm thick. Measurements were performed with four different preloads, indicated by the 'FNx' part of the filename. The preloads were chosen so the preload per cup was equal to the preload per cup in the preload series experiment to allow for comparison between the samples studied in that experiment and the sample studied in this experiment. 

#### <a name="cut"></a> Cut backing layer

This data was obtained to study the role of elastic interactions in the backing layer on detachment behaviour in our system. The backing layer is the layer of Ecoflex &trade; to which the individual cups are attached and which connects all features. A P4 sample with a backing layer of 1.10 mm thick was measured with a preload of 6 N and a retraction speed of 500 µm/s. The backing layer was then cut in both dimensions of the lattice and the measurements were repeated. The orange lines in the figure below show schematically where the backing layer was cut.

<img src="https://user-images.githubusercontent.com/115638429/212077430-061dffea-21f6-4733-820d-d20c82c02ee9.png" width=40% height=40%>

This experiment was also carried out for a P2.5 sample with a backing layer of 2.59 mm thick. In this experiment, we also obtained data after cutting the backing layer in only one dimension of the lattice. In the filenames, 'uncut' indicates data for the intact backing layer, 'pcut' indicates data for a backing layer that is cut in one direction and 'cut' indicates data obtained for a sample where the backing layer was cut in two dimensions. 

## <a name="zeekat"></a> Zeekat library

The zeekat library is a collection of functions used for the analysis of the data in this repository. 


