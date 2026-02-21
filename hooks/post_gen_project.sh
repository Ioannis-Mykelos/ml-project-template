#!/bin/bash
#echo "# {{ cookiecutter.project_slug }}" >> README.md
git config --global user.name "{{cookiecutter.full_name}}"
git config --global user.email {{cookiecutter.email}}
git config --global init.defaultBranch main
git config --global --add --bool push.autoSetupRemote true


path="/mnt/batch/tasks/shared/LS_root/mounts/clusters/"
path+="{{cookiecutter.compute_instance_name}}"
path+="/code/Users/"
path+="{{cookiecutter.short_name}}"
path+="/"
path+="{{cookiecutter.project_slug}}"

echo $path
git config --global --add safe.directory $path
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.git
git push -u origin main

