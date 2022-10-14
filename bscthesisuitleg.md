# bscthesis
Het doel van dit project is om te bepalen of het fiber bundle model (FBM) geschikt is om de detachment van een suction cup array te beschrijven. Zeekat is een module die
data uit een rheometer kan verwerken en analyseren. Ook bevat de module functies om de data te fitten aan het FBM. 

Module zeekat
zeekat bevat functies die de data knipt, de stress en strain bepaalt en een fit uitvoert met het FBM. Let op:
-zk.calcstress() heeft als argument 'features'. Dit is 110 voor p2.5, 80 voor p3 en 42 voor p4. 
- zk.schaar() heeft twee threshold arguments (threshold1 &threshold2). De defaults werken voor alle representatieve curves behalve P4 van retraction speeds, daar moet threshold2 worden verhoogd.
- zk.weibfit() heeft 'ouput'als arg, hier moet je aangeven of je een array wilt met de weibull pars (output='pars') of het dataframe (output='df')

Er is een apart script voor iedere feature density, zowel voor alle FN experimenten als ook de retraction speed (RS) experimenten. M.b.v. dict comprehension worden curves selectief geplot. Je kunt deze de normaalkrachten of retraction speeds zoals deze in de filename staan invullen om bepaalde curves te plotten.

Voor P2.5 zijn er in de categorie FN 2 mapjes met representatieve curves, deze verschillen alleen in de curve van 0.7N. Het mapje met de naam P2.5B heeft daar een curve die meer representatief is voor de hele loop maar minder goed fit dan de curve die in P2.5 staat. 
