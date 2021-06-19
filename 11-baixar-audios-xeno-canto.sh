#!/bin/bash

ESPECIES=`cat especies-oiapoque.txt`

''' 
ESPECIES="
Mimus saturninus
Columba livia
Caracara plancus
Megarynchus pitangua
Vanellus chilensis
Pitangus sulphuratus
Turdus rufiventris
Furnarius rufus
Theristicus caudatus
"
'''

#echo "[$ESPECIES]"
#exit

while IFS= read -r especie
do
  if [ "$especie" == "" ]; then continue; fi
  echo "[$especie]"
  python xcdl.py $especie
done <<< $ESPECIES
