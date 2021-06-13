#!/bin/bash
TAMANHO=5 # em segundos

#rm -rf wav${TAMANHO}s; mkdir wav${TAMANHO}s
dirsaida="wav${TAMANHO}s"
if [ ! -d $dirsaida ]; then mkdir $dirsaida; fi

#for entrada in `find mp3/ -name "*.mp3" | head -1`
for entrada in `find -L mp3/ -name "*.mp3"`
do
  saida=`echo $entrada | sed 's/mp3/wav/g'`
  dirsaida=`dirname $saida`
  echo "[$entrada] -> [$saida]"
  #if [ ! -d $dirsaida ]; then mkdir $dirsaida; fi

  duracao=`ffprobe -i $entrada -show_format -v quiet | sed -n 's/^duration=\([0-9]\+\).*$/\1/p' 2> /dev/null`
  #duracao=`ffprobe -i $entrada -show_format -v quiet | sed -n 's/duration=//p'`
  echo "duração: $duracao s"
  let cortes=duracao/TAMANHO
  echo "cortes: $cortes"

  inicio=0
  for corte in `seq 1 $cortes`
  do
    let inicio=(corte-1)*TAMANHO
    let termino=inicio+TAMANHO
    saidacorte=`echo $saida | sed -e 's/^wav/wav'$TAMANHO's/' -e 's/.wav$/-'$corte'.wav/'`
    echo "corte $corte: $saidacorte"
    #echo "trecho: $inicio .. $termino"

    if [ $corte -eq 1 ]
    then
      dirsaidacorte=`dirname $saidacorte`
      if [ ! -d $dirsaidacorte ]; then mkdir $dirsaidacorte; fi
    fi
    
    ffmpeg -i "$entrada" \
      -acodec pcm_s16le \
      -ac 1 \
      -ar 16000 \
      -y -hide_banner \
      -ss $inicio \
      -to $termino \
      -v quiet \
      "$saidacorte"
    #echo
  done
  echo
done
