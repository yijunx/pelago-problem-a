# pelago-problem-a



- open this repo in devcontainer (it will spin up postgre db as well as pgadmin4 for some UI help on postgres, details can be found in .devcontainer/docker-compose-yml)
- run test 

        ```make test```
- run script to pull data from cran (it takes sometime to do the 50 packages...)

        ```make pull_data```
- run the flask app

        ```make up```
