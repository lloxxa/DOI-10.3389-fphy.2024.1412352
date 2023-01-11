# Sucker analysis

This project studies the adhesion of arrays of millimeter-sized suction cups made from polydimethylsiloxane. Repository contains both data obtained in this project and code used to analyse said data.

## Table Of Contents

- [Introduction](#Introduction)
- [Fabrication](#Fabrication)
- [Measurements](#Measurements)
- [About the data](#About)
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

One measurement cycle consists of four distinct phases, visualized below. The first phase is the approach (1 & 2) where the probe approaches the countersurface until a certain force is detected. The force by which we indent the sample to the countersurface is called the preload. The next phase is the relaxation phase, where the probe does not move for 20 seconds (3). AFter the relaxation, retraction starts. The probe pulls the sample away from the countersurface at a certain speed that we call the retraction speed (4 & 5). After the sample has detached completely from the countersurface, a short transition phase happens where the retraction ends and approach is initiated. Generally, we repeat this cycle multiple times for each experiment. For information about the preload, retraction speed and number of cycles that correspond to each dataset, see About the data(#About). 

![Expopzet](https://user-images.githubusercontent.com/115638429/211790927-e9ab5a05-e07a-4d3e-a7f4-dcec078bb192.png)

It is important to note that each phase has its own CSV file in the raw data. 


