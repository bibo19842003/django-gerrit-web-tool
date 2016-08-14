#!/bin/bash

MANIFEST_NAME=$1
TAG_NAME=$2
OB_NAME=$3
NB_NAME=$4
SERVER_IP=$5
GERRIT_USER=$6
GERRIT_PORT=$7
DJANGO_PATH=$8


WORK_SPACE="${DJANGO_PATH}/common/createbranch"
PROJECT_LIST="${WORK_SPACE}/project-list.txt"

echo "git clone manifest project "
cd ${WORK_SPACE}
rm -rf "${MANIFEST_NAME}"
git clone ssh://${SERVER_IP}/${MANIFEST_NAME} -b ${OB_NAME} ${MANIFEST_NAME}

if [ "$?" != "0" ]; then
    echo "download ssh://${SERVER_IP}/${MANIFEST_NAME} failed"
    exit 1
fi

if [ ! -f "${WORK_SPACE}/${MANIFEST_NAME}/${TAG_NAME}" ]; then
    echo "${TAG_NAME} is not exist !!!"
    exit 1
fi

# project create branch
echo "project create branch"
${WORK_SPACE}/parsexml.py ${WORK_SPACE}/${MANIFEST_NAME}/${TAG_NAME} > "${PROJECT_LIST}"

for ONELINE in `cat ${PROJECT_LIST}`
do

    PROJECT_NAME=`echo ${ONELINE} | cut -d ":" -f1`
    PROJECT_REVISION=`echo ${ONELINE} | cut -d ":" -f2`

    echo "${PROJECT_NAME} ${PROJECT_REVISION}"
    ssh -p ${GERRIT_PORT} ${GERRIT_USER}@${SERVER_IP} gerrit create-branch ${PROJECT_NAME} ${NB_NAME} ${PROJECT_REVISION}

done

# manifest create branch
echo "manifest project create branch"
cd ${WORK_SPACE}/${MANIFEST_NAME}
git checkout -b ${NB_NAME} ${OB_NAME}
cp ${TAG_NAME} ../
rm -rf *
mv ../${TAG_NAME} create-branch-from-${TAG_NAME}
cp create-branch-from-${TAG_NAME} default.xml
sed -i "s/${OB_NAME}/${NB_NAME}/g" default.xml
let REVISION_LINE=$(cat default.xml | grep -n "<default" | cut -d ":" -f1)+1
sed -i "${REVISION_LINE}, \$s/revision=\".*\"//g" default.xml
git add -A
git commit -m "create branch ${NB_NAME} from ${OB_NAME} , ${TAG_NAME}"
git push -f origin ${NB_NAME}

echo "create branch is finished"
