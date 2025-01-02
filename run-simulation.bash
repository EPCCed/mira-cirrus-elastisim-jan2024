#!/bin/bash

model=$1

# Cleanup
# rm -f $PWD/$model/data/output/*.csv

# Create directory if we need to
outdir=${model}/data/output
if [[ ! -e $outdir ]]; then
    echo "Creating: $outdir"
    mkdir -p $outdir
elif [[ ! -d $dir ]]; then
    echo "$outdir already exists but is not a directory" 1>&2
fi

docker run -v $PWD/$model/data:/data -v $PWD/algorithm:/algorithm --name $model --detach elastisim /data/input/configuration.json --log=root.thresh:warning 
sleep 20
docker container ls
echo "[$(date)] Starting running $model"

docker exec $model python3 /algorithm/algorithm.py

echo "[$(date)] Finished running $model"

docker logs $model


