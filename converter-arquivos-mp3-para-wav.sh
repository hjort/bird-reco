#!/bin/bash
for entrada in `find mp3 -name "*.mp3"`
do
  saida=`echo $entrada | sed 's/mp3/wav/g'`
  dirsaida=`dirname $saida`
  echo "[$entrada] -> [$saida]"
  if [ ! -d $dirsaida ]; then mkdir $dirsaida; fi
  ffmpeg -i "$entrada" \
    -acodec pcm_s16le \
    -ac 1 \
    -ar 16000 \
    -y -hide_banner \
    "$saida"
  echo
done
