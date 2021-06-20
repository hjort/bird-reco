#!/bin/bash

dirpasso1="wavbal5"
dirpasso2="wavbal5a"
dirfinal="wavbal5f"

rm -rf $dirfinal

cp -r $dirpasso2 $dirfinal

cd $dirpasso1
for especie in */
do
  echo "[$especie]"
  for arq in `find $especie/ -type f -name "*.wav" | sort | head -591`
  do
    cp "$arq" ../$dirfinal/$especie/ 
  done
done
cd ..

du -csh $dirfinal/*
