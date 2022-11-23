# Setup docker postgres instance
Load and run the postgres docker Database
`docker run --name itmc_project_db -p 127.0.0.1:5432:5432 -e POSTGRES_PASSWORD=pw postgres`

## Loading db schema into docker
Copy the sql script into the docker container
`docker cp schema.sql itmc_project_db:/`

## Run the sql schema file to build the db
`docker exec -it itmc_project_db psql -U postgres -d postgres -f /schema.sql`
