# tinker
my small tinkerings

## Installation

1. **Install docker**, see [get docker](https://docs.docker.com/get-docker/)
2. **Check out this repo to `whatever_repo_path_you_like`**
3. **Set up the modified `datascience jupyter lab`** by navigating to` whatever_repo_path_you_like` and executing
```bash
docker build --tag tinker/datascience-notebook:latest .
```
4. **Run the jupyter lab** by executing
```bash
docker run --rm --name tinker -p 8888:8888 -e JUPYTER_ENABLE_LAB=yes --mount type=bind,source="whatever_repo_path_you_like",target=/home/jovyan/tinker tinker/datascience-notebook:latest
```

## Usage

1. Using a different terminal, enter the container running the jupyter lab by executing
```bash
docker exec -it thinker bash
```
2. Inside the container navigate to `~/tinker/thermos` and run
```bash
jupytext --to notebook thermos.Rmd && touch thermos.Rmd
```
to generate the `.ipynb` file from the versioned `.Rmd` file
3. To run the notebook via the commandline execute
```bash
papermill thermos.ipynb thermos.ipynb
```
4. To generate an html file form the jupyter notebook execute
```bash
jupyter nbconvert thermos.ipynb --to html
```
5. Profit
