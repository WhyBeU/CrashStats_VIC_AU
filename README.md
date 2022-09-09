# CrashStats_VIC_AU 

Investigation of the crash statistics dataset of the Victorian government (Australia)
[Dataset publicly available](https://discover.data.vic.gov.au/dataset/crash-stats-data-extract)
 ---

## Requirement installation - 

Use [pipenv](https://pipenv-fork.readthedocs.io/en/latest/basics.html) or pip to install the dependencies for the code:

`>> pipenv install`

`>> pip install requirement.txt`

Download the crash statistics dataset of the Victorian government and extract the csv files in the data folder

## Structure -

```
project
│   README.md
│
└───code
│   │   injury_statistics.py        [calculation and plotting of the injury-related statistics]
│   │   location_statistics.py      [calculation and plotting of the injury-related location map of Victoria]
|   |   matplotlibestyle.py         [matplotlib parameters settings]
│   
└───data
│   │   <add datasets here>   
│ 
└───figures
    │   <plots and graphs are saved here>

```
