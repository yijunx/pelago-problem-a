# How to use



- Open this repo in vscode devcontainer (it will spin up postgre db as well as pgadmin4 for some UI help on postgres, details can be found in .devcontainer/docker-compose-yml)
- Run test 

        make test
- Run script to pull data from cran (it takes sometime to do the 50 packages...)

        make pull_data
- Run the flask app

        make up
        
- Now we can use it

        curl --location --request GET 'localhost:8000/api/packages?keyword=measure'

        curl --location --request GET 'localhost:8000/api/packages/<package_id>'

# About design

- db
    - 4 tables, author and maintainer table associate package table and developer table. So one developer can be author or maintainer for one or more packages
    - Unique constraints are added to make sure no duplicates
    - Used session scope to make sure transactional behavior
- app
    - Used blue print to aggregate apis
    - Used pydantic to check / convert incoming json payload to pydantic models
    - api layer -> service layer -> repo layer -> db
    - Used standard response type to have consistent response (for frontend to use)
    - Exceptions handling are not done yet, now the api sends the raw error if there is issue
    - Gunicorn with async worker
- deployment
    - Dockerfile is created
    - InitContainer is needed for migration and pull data into the database (if deploy to k8s)
