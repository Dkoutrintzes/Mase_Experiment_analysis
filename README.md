# Mase_Experiment_analysis

Most codes need an Expert folder with the results of the expert playthrough in order to plot those results in their graphs. The codes dont ask for that file manually.

---
-Distances create a boxplot with the distances of the participants in each block. 
-Scores create a boxplot with the scores of the participants in each block.
-Speeds create a boxplot with the avg speed of the participants in each block.
-Wins create a boxplot with the number of wins the participant had in each block.

All codes need the same input as referred to bellow.

When run it needs the input of the folder where the JSON files of the participants are. The title and the labels are changed manually inside the code.

```
python Distances.py <path to folder>
```

Scoreeval creates a boxplot using the json files from the familiarization games. Works as the above but needs the json files from the Familiarization games. 

---
Temperature creates a plot with the temperature scores and entropy. It has 2 inputs, first the folder with the json files of the participant or the expert and a numeric flag. 
The numeric flag has 3 options:
'1' if the json files are for the No_TL group
'2' if the json files are for the TL group
'3' if the json file is for the expert

The entropy is only plotted in the case of '3' where the expert is plotted. 

```
python temperature.py <path to folder> <1 or 2 or 3>
```
---

Heatmap.py creates the heatmaps for all participants. It does not have and input and it searches for folders NO_TL_Final_results, TL_Final_results and Expert for the json files. It does not have any checks so if the files doesnt exist it may crash :)

Heatmap2.py it is a pile of codes that i dont have the smallest idea what is what in there :) 

---
