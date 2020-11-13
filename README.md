# Tasks Scheduler

[![Build Status](https://travis-ci.com/daniktl/task-scheduler-put-project.svg?branch=main)](https://travis-ci.com/daniktl/task-scheduler-put-project)

Task scheduler algorithm for 1 machine (and other modes soon).

### One-engine mode (mode 1)

**Input data** should be in the next format:

```
p1 r1 d1 w1
p2 r2 d2 w2
...
pn rn dn wn
```

where:

- pi - processing time of the task
- ri - ready time (time when task could be started)
- di - due time (time when task should be finished)
- wi - weight of the task

**Output data** should be in the next format:
```
Sum(wj * Uj)
J(1) J(2) ... J(n)
```

where:

- criterion
- sequence of tasks processing by the machine 

### Parallel engines mode (mode 2)

### Installation

To install this algorithm - simply clone this repository. No additional packages required. 
You have to get python 3.6 or above installed on your computer

### Running

You can read data from the `data/` child directory named with the next template: `[in|out]_LASTNAME_INSTANCES.txt`. 
To run this algorithm from console, use `python3 task_scheduler.py --who LAST_NAME` command. 
Be sure to place your input and output files named properly inside `data/` directory.

### Licence

This project is covered by MIT Licence