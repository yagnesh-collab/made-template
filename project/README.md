# Project work check
## Project work 3
### In Pipeline(Actions)
If you want to check the project work 3 then simply go to Actions. There you can see in the actions, I am pulling the datasets from the kaggle. To check my datasets are pulled successfully I have mentioned 1 test case `Check file existence`.

### locally
create the .kaggle folder and copy your credentials into it.
```sh
mkdir ./~.kaggle
cp kaggle.json ~/.kaggle/ 
```

### To download kaggle.json file
`Go to Kaggle -> settings -> Create New Token`

## Project work 4 & 5 
### Project work 4 
In project work 4,  I have added the `test_pipeline.py` file for the testing the project work 4. To execute the `test_pipeline.py` i have added the `tests.sh`.

### Project work 5
In project work 5, I have added te `test_pipeline.yml` file got the github actions that executes the `tests.sh` on every push on the main branch.