#!/bin/bash

especies=`cat especies-oiapoque2.txt`
qtde=914

#echo "[$especies]"
#exit

while IFS= read -r especie
do
  if [ "$especie" == "" ]; then continue; fi
  echo "[$especie]"
  python gerar-arquivos-audio-adicionais.py --especie "$especie" --quantidade $qtde &
done <<< $especies

wait
echo "Concluído!"
