# How to use poetry

Official documentation [here](https://python-poetry.org/docs/basic-usage/#project-setup)

## 1 ) Make sure you have poetry installed :

- Depending on what you use there are different ways, some popular ones are :
```
pip install poetry
```
```
brew install poetry
```
```
conda install poetry
```
- More info can be found here: https://python-poetry.org/docs/basic-usage/

## OBS: At this point of writing this documentation we are using:
```
poetry==1.8.2
poetry-core==1.9.0
poetry-plugin-export==1.7.1
```

## 2 ) Initialize poetry to your existing project.
Poetry can be used to ‘initialise’ a pre-populated directory. To interactively create a pyproject.toml file in directory of the pre-existing-project:
```
cd pre-existing-project
poetry init
```

## 3 ) Specifying dependencies.
You can use the add command to Specify dependencies one by one or by a requirements.txt file.
```
poetry add pandas
```
or
```
poetry add $(cat requirements.txt)
```

If you want to add dependencies in the dev environments you should use the command:
```
poetry add "pandas>=2.0.0" --group dev
```

If you make changes manually to your pyproject.toml you can update the file with the command:
```
poetry lock
```