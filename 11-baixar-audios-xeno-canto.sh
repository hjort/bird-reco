#!/bin/bash

especies=`cat especies-oiapoque2.txt`

#echo "[$especies]"
#exit

while IFS= read -r especie
do
  if [ "$especie" == "" ]; then continue; fi
  echo "[$especie]"
  python xcdl.py $especie &
done <<< $especies

wait
echo "Concluído!"
