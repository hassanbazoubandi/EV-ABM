# ADOPTION OF ELECTRIC VEHICLES – AN AGENT-BASED MODEL APPROACH
### Author
Project implemented by Bartłomiej Chwiłkowski (github: chwilko)
### License 
[MIT license](LICENSE)
## Table of content
- [ADOPTION OF ELECTRIC VEHICLES – AN AGENT-BASED MODEL APPROACH](#adoption-of-electric-vehicles--an-agent-based-model-approach)
    - [Author](#author)
    - [License](#license)
  - [Table of content](#table-of-content)
- [Repository contents](#repository-contents)
  - [model](#model)
    - [package structure tree](#package-structure-tree)
    - [Classes](#classes)
      - [Society](#society)
      - [Cars](#cars)
      - [City](#city)
      - [Corporations](#corporations)
      - [Customer](#customer)
      - [Government](#government)
      - [Prices](#prices)
      - [Time](#time)
    - [utils](#utils)
      - [common params](#common-params)
      - [get trajectoiries](#get-trajectoiries)
      - [make plot](#make-plot)
    - [Other files](#other-files)
      - [data](#data)
      - [initial\_params](#initial_params)
  - [analyze](#analyze)
  - [data](#data-1)
  - [otomoto-crawler](#otomoto-crawler)
  - [pictures](#pictures)
  - [tests](#tests)
  - [Makefile](#makefile)
    - [info](#info)
    - [generate figs](#generate-figs)
    - [linters](#linters)
    - [Run example trajectories](#run-example-trajectories)
    - [Scrap data form *otomoto.pl*](#scrap-data-form-otomotopl)


```
## Model summary
Agent-based model simulating electric vehicle adoption for the Polish city of Wroclaw. The purpose of the study is to check how different government strategies influence the adoption of electric vehicles. In the model, environment interacts with government and car producers. Customers buy new car following the decision tree.

## Desctiption
The project is an impolementation of the model described in the master's thesis (At Wroclaw University of Science and Technology for Applied Mathematics). The thesis itself will be made available most likely when the polytechnic's right to first publication expires (6 months after submission).

# How to run model
First create virtual environment using venv:

python3.11 -m venv abm
source abm/bin/activate
python3 -m pip install -r requirements.txt
```
or using poetry (version 1.2.1)
```
poetry env use python3.11
poetry shell
poetry install
```
Next run
```
python3 -m model
```
Congrats, you just generated a sample plot. To generate the remaining plots perform:
```
bash generate_figs.sh
```
or open one of the ".ipynb" files from [analyze/results/](analyze/results/main_results_by_gov.ipynb).

# Repository contents
## model
### package structure tree
```
model
├── __init__.py
├── __main__.py
├── Cars.py
├── City.py
├── common.py
├── constants.py
├── Corporations.py
├── Customer.py
├── data.json
├── Government.py
├── initial_params.json
├── Prices.py
├── Society.py
├── Time.py
└── utils
    ├── __init__.py
    ├── common_params.py
    ├── get_trajectories.py
    └── make_plot.py
````
### Classes
The model is implemented according to the OOP paradigm.

#### Society
Society is the main class. It is responsible for communicating with the other classes and iterating the algorithm.
Class SocietyConstantsEnergyPrices is used by default. There are is SocietyVariableEnergyPrices too.
Both of them inherit for Society.

#### Cars
Cars, as a customer field, are responsible for type (BEV, PHEV, CV), age and cost per km.
Any car type has own class witch inherit for class Car (like abstract class).

#### City
The city creates the environment of the model.
City is responsible for set initial public chargers, add new, remove old and count all nearby to checked Customer.

#### Corporations
Corporation represent type of one model agent. 
Corporations are responsible for auto prices and their changes.

#### Customer
Customer represent type of one model agent. 
Customers are agents whose status will be counted and analyzed.
Any Customer instance has indyvidual set of fields.
- procfile -- mean annual mileage
- home -- place in City
- car -- see class Car

The customer is also responsible for the mechanism for buying a car, and for choosing between two types.

#### Government
Government represent type of one model agent. 
Government are responsible for introduce seted government strategy.
Actually are implemented:
- GovernmentBuildChargingStation
- GovernmentProvidesSubsidies
- GovernmentMixedStrategy
- GovernmentNoSubsidies
- GovernmentCloseChargingStation
  
Any of them inherit for class AbstractGovernment (like abstract class).
To check other strategies it is advisable to create a corresponding class inheriting from AbstractGovernment.

#### Prices
Price is responsible for fuel and energy prices. 
In the default society "SocietyConstantsEnergyPrices" (see Society) is used class ConstatntPrice and are constants prices.
Howeover model is ready for implement function wich estimate future prices (class Prices).
Both of them (ConstatntPrice, Prices) inherit for class Price.

#### Time
Time is responsible for converting time from model time to real time.
This is especially true for variable fuel and energy prices

### utils
In this folder are useful parts of the package not directly responsible for model implementations.

#### common params
File common_params.py include json `common_params` with initial parameters used in thesis. 

#### get trajectoiries
The get_trajectories.py file contains functions that allow multi-threaded generation of multiple model trajectories. Both for a fixed set of parameters and for a single parameter in different versions.

#### make plot
File make_plot.py get output with get_trajectories.py functions and create plots with matplotlib.

### Other files
#### data
Not model parameters, but fixed values for customer profiles, and car parameters.
#### initial_params
Initial distributions of profiles and car types.


## analyze
The folder contains both data analysis and simulation files of various model trajectories. 

## data
In this folder I keep all collected data used to estimate model parameters. See corresponding [README](data/README.md)

## otomoto-crawler
Crowler used to download car data from [_otomoto.pl_](https://www.otomoto.pl/).
Crowler is borrowed with small changes. See corresponding [README](otomoto-crawler/README.md)
If you want run crawler follow the instructions below:

First create virtual environment using venv:

```
python3.11 -m venv abm
source abm/bin/activate
python3 -m pip install -r requirements.txt
```
or using poetry (version 1.2.1)
```
poetry env use python3.11
poetry shell
poetry install
```

Next run scrapping using *main*
```
make scrap_om
```
or directly:
```
python3 -m otomoto-crawler
```

## pictures
Folder for pictures generated by model. See section "How to run model"


## tests
Folder with tests. Tests use the **pytest** library.
To run tests:
```
pytest
```

## Makefile
Makefile this is the control panel with endpoints:
### info
```
make
```

### generate figs
Generation of graphs for trajectory and model with different parameters.
See "How to run model".
```
make generate_figs
```

### linters
```
make lint
```

### Run example trajectories
```
make run
```

### Scrap data form *otomoto.pl*
See subsection "otomoto-crawler"
```
make scrap_om
```
