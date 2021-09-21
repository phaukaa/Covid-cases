# Assingment 6 #
-----------------
## Requirements ##
To run the script ypu need to have these packages installed:
- Pandas
- Altair
- Flask
As well as Python 3.6 or higher.\
The packages can be installed using
```bash
pip3 install [package name]
```

#### web_visualization.py ####
This is the main script of the assignment.\
This script depends on data from the csv files in the covid_cases directory.\
When running the script using 
```bash
python3 web_visualization.py
```
the script creates graphs for all csv files in the covid_cases dir, both cumulative, reported cases and both combined, and shows these in a local running web server (on local host, most likely [127.0.0.0:5000](http://127.0.0.1:5000/)).\
The script also displays a nice menu where you can choose which county you want the stats for, and you can also set a start and end date for the graph to show stats.\
The default stats shown is the files in the covid_cases dir, from the first case (2020-02-21) to the day i downloaded the files (2020-11-09).