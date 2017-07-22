#!/bin/bash

g_ssh_port=$1
g_user=$2
s_ip=$3
project=$4
parentproject=$5

runtime=$6
runuser=$7
django_path=$8

echo "project:${project}  parentproject:${parentproject} " >> "${django_path}/static/log/gerrit/createproject/${runtime}-${runuser}-${s_ip}.txt"

ssh -p $g_ssh_port ${g_user}@${s_ip} gerrit create-project $project --parent $parentproject --empty-commit >> "${django_path}/static/log/gerrit/createproject/${runtime}-${runuser}-${s_ip}.txt" 2>&1

