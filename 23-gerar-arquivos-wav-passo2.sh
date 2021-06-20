#!/bin/bash

especies=`cat especies-oiapoque.txt`

#echo "[$especies]"
#exit

while IFS= read -r especie
do
  if [ "$especie" == "" ]; then continue; fi
  echo "[$especie]"
  python gerar-arquivos-audio-adicionais.py --especie "$especie" --quantidade 591 &
done <<< $especies

wait
echo "Concluído!"
