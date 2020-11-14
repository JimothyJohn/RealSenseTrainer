#!/bin/bash

if [[ -z "$1" ]]
then
    echo "Enter a name for your object..."
    exit 1
fi

DIR=$HOME/training-data/$1
mkdir -p $DIR

echo $DIR/2D-data
mkdir $DIR/2D-data $DIR/3D-data $DIR/labels $DIR/clean_labels

echo "Training $OBJECT"
python /rst/main.py $DIR
