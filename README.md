# MIRA - Cirrus scheduler modelling - Jan 2024 period

Repository for data and configuration for modelling scheduling on 
[Cirrus](https://www.cirrus.ac.uk) CPU partition using [ElastiSim](https://elastisim.github.io/).

This repository contains data for the January 2024 modelling period. There is a 
[correpsonding repository for the September 2024 modelling period](https://github.com/EPCCed/mira-cirrus-elastisim-sep2024).

## Repository contents

- [algorithm/](algorithm/) - Subdirectory containing the simple, FIFO scheduling algorithm used by Elastisim simulations
- [analysis/](analysis/) - Scripts and analysed data from measured job load and simulations
- [cirrus-cpu-measured/](cirrus-cpu-measured/) - Measured job data from Cirrus
- cirrus-cpu-* - Various scheduler simulations (see below for details)
- [emissions/](emissions/) - Emissions modelling data and output 
- [utils/](utils/) - Utility scripts

### Simulation subdirectories

| Directory | Description |
|-----------|-------------|
| [cirrus-cpu-R/](cirrus-cpu-R/) | Cirrus jobs only, Cirrus jobs rigid |
| [cirrus-cpu-M/](cirrus-cpu-M/) | Cirrus jobs only, Cirrus jobs moldable |
| [cirrus-cpu-M_archer2-R-10pc/](cirrus-cpu-M_archer2-R-10pc/) | Cirrus jobs moldable. ARCHER2 mobile jobs: 10% of Cirrus resource use |
| [cirrus-cpu-M_archer2-R-20pc/](cirrus-cpu-M_archer2-R-10pc/) | Cirrus jobs moldable. ARCHER2 mobile jobs: 20% of Cirrus resource use |
| [cirrus-cpu-M_archer2-R-30pc/](cirrus-cpu-M_archer2-R-10pc/) | Cirrus jobs moldable. ARCHER2 mobile jobs: 30% of Cirrus resource use |
| [cirrus-cpu-M_archer2-R-40pc/](cirrus-cpu-M_archer2-R-10pc/) | Cirrus jobs moldable. ARCHER2 mobile jobs: 40% of Cirrus resource use |
| [cirrus-cpu-M_archer2-R-50pc/](cirrus-cpu-M_archer2-R-10pc/) | Cirrus jobs moldable. ARCHER2 mobile jobs: 50% of Cirrus resource use |
| [cirrus-cpu-M_archer2-R-60pc/](cirrus-cpu-M_archer2-R-10pc/) | Cirrus jobs moldable. ARCHER2 mobile jobs: 60% of Cirrus resource use |
| [cirrus-cpu-M_archer2-R-70pc/](cirrus-cpu-M_archer2-R-10pc/) | Cirrus jobs moldable. ARCHER2 mobile jobs: 70% of Cirrus resource use |
| [cirrus-cpu-M_archer2-R-80pc/](cirrus-cpu-M_archer2-R-10pc/) | Cirrus jobs moldable. ARCHER2 mobile jobs: 80% of Cirrus resource use |
| [cirrus-cpu-M_archer2-R-90pc/](cirrus-cpu-M_archer2-R-10pc/) | Cirrus jobs moldable. ARCHER2 mobile jobs: 90% of Cirrus resource use |
| [cirrus-cpu-M_archer2-R-100pc/](cirrus-cpu-M_archer2-R-10pc/) | Cirrus jobs moldable. ARCHER2 mobile jobs: 100% of Cirrus resource use |

## Model description

The Elastisim scheduler model consists of a number of different components:

- Scheduler algorithm definition
- Cirrus cluster definition
- Application performance model(s)
- Job list to simulate

### Scheduler algorithm description

The file [algorithm/algorithm.py] describes how jobs are scheduled. The algorithm is:

```
- Loop over jobs in the queue in order of submission:
  - If a moldable job:
      - Loop from smallest to largest job size and try to fit into available slots
      - If it cannot be fit into available slots, move on to next queued job
  -If a rigid job:
      -Try to fit into available slots
      - If it cannot be fit into available slots, move onto next queued job
```

### Cirrus cluster definition

### Application performance model

### Job list to simulate
    