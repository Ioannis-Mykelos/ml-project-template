# How to use UV

Official documentation [here](https://docs.astral.sh/uv/getting-started/)

## 1 ) Make sure you have uv installed :

- Depending on what you use there are different ways, some popular ones are :
```
pip install uv
```
```
brew install uv
```
```
conda install uv
```
- More info can be found here: https://docs.astral.sh/uv/getting-started/

## OBS: At this point of writing this documentation we are using:
```
uv == 0.10.9
```

## 2 ) Initialize uv to your existing project.
UV can be used to ‘initialise’ a pre-populated directory. To interactively create a pyproject.toml file in directory of the pre-existing-project:
```
cd pre-existing-project
uv init
```

or if you already have the `pyproject.toml` file (as in this template) use:
```
uv venv
```
to syncronize and create your `.venv` file and the environment



## 3 ) Specifying dependencies.
You can use the add command to Specify dependencies one by one or by a requirements.txt file.
```
uv add pandas
```
or
```
uv add $(cat requirements.txt)
```

If you want to add dependencies in the dev environments you should use the command:
```
uv add "pandas>=2.0.0" --group dev
```

If you make changes manually to your pyproject.toml you can update the file with the command:
```
uv lock
```

## 4 ) Create your lock file.
Create your lock file with
```
uv lock
```

## 5 ) Syncronize your virtuall environment with the lates additions.
```
uv sync
```