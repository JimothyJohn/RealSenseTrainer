#!/bin/bash

read -p "Enter a name for your object: " OBJECT
# Configure environment
if [[ -z "$1" ]]
then
    echo "Enter a name for your object..."
    exit 1
fi

DIR=./datasets/$OBJECT

# Clear output directory or create
if [[ -d $DIR/clean_labels ]]
then
    rm -f $DIR/clean_labels/* # delete the previous frames
else
    mkdir $DIR/clean_labels # create target folder
fi

echo "Moving $OBJECT labels!"
for dir in $DIR/data/*; do

    frame=`echo $dir | egrep -o "[0-9]+"`
    mv $DIR/labels/seg_$frame.png $DIR/clean_labels/seg_$frame.png 2>/dev/null

done

# Remove all irrelevant entries
# rm $DIR/labels/*