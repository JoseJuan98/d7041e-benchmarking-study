# Applied AI Benchmarking Study

This comprehensive benchmarking study involves systematically evaluating the performance of multiple machine learning models across a variety of datasets. 
The goal is to compare the effectiveness of different models and preprocessing techniques in a consistent and reproducible manner.

## Setup

For the setup of the project follow the instructions in the [SETUP.md](docs/SETUP.md) file.

## Project Structure

```bash
│
├── artifacts                 # folders excluded from the repo, what you store here it won't be store in the repo
│     ├── data
│     └── models
│
├── src                      # source code folder for common code and for CRISP-DM steps
│     ├── common
│     ├── data_understanding
│     ├── data_preparation
│     ├── ...               
│     └── modelling
│
├── dev-requirements.txt     # testing dependencies
├── environment.yaml         # conda formatted dependencies, used by 'make init' to create the virtualenv
├── README.md                
└── requirements.txt         # core dependencies of the library in pip format
```
