# How to use cookiecutter with  **ml-project-template**

## 1 ) Make sure you have cookiecutter installed :

- Depending on what you use there are different ways, some popular ones are :
```
pip install cookiecutter
```
```
brew install cookiecutter
```
```
conda install cookiecutter
```
- More info can be found here: https://cookiecutter.readthedocs.io/en/1.7.2/installation.html

### If you want to use a local version of **ml-project-template**, clone it to your computer:

```
git clone https://github.com/Ioannis-Mykelos/ml-project-template.git
```
or if you're using ssh:

```
git clone git@github.com:Ioannis-Mykelos/ml-project-template.git
```

### OBS: If you want the project to be automatically pushed to a repo then create an empty repo, with the same name as the project.

## 2 ) Generate the project using cookiecutter:

- Open a terminal and travel/navigate to the place where you want to place the project using the command cd
```
cd Users/YOUR_EMAIL_PREFIX_NAME/DIRECTORY_YOU_WANT_TO_CREATE_THE_PROJECT
```
- You can generate a project with a repo, use the following command:
```
cookiecutter git@github.com:nuuday/ml-project-template.git
```
and even select a specific branch you want to use :
```
cookiecutter git@github.com:nuuday/ml-project-template.git --checkout dev
```
- You can also use a local cloned version of the  **ml-project-template** by running the cookiecutter command plus the path to the template so for example if you are in the directory where the folder is you can run :
```
cookiecutter ml-project-template
```
- If the command worked, you will be prompted to put in the required information **line by line** in the command prompt:
  - What is written in [ ] is the **default value**, so if you just press **enter** it will take that value.
  - The first 3 lines are the easiest (**full_name**, **email**, & **short_name**).
  - For **github_username** press **Enter** if you wish to push to the Nuuday repo, otherwise replace it with your own username.
  - The **project_name** MUST match the name of the empty repository you created (This is important).
  - The **project_slug** generates itself from the **project_name** so unless you want different names or something went wrong with naming you can just press enter.
  - The **project_short_description** and **version** are optional (fill in anything you think is usefull).
  - **REMINDER**: if you want it to be pushed to a repo you need to match the name of the repo with the **project_slug** and/or **project_name**.
As a reference you can see the following pictures:
<br/>
	<img src=images/cookie1.png width="1100" height="350">
<br/>









## 3 ) How to install pre-commits:

- After the project was generated, clone it down to whatever compute you want to develop on (if it wasn't generated there already). Make sure you have the pre-commit package installed:
```
pip install pre-commit
```
- Then install the pre-commit commands that are included in the template by running:
```
pre-commit install
```
- Now the pre-commits should run automatically everytime something is commited to git. No need to re-install if you make changes to .pre-commit-config.yaml, it will automatically re-install.

- *OBS!*:
If you need to add the pre-commits to an already existing project, download the `.pre-commit-config.yaml` & `setup.cfg` files into the root directory of the project and then, follow the steps above.
