#!/bin/bash
TAMANHO=5 # cada corte terá essa duração (em segundos)

#rm -rf wav${TAMANHO}s; mkdir wav${TAMANHO}s
dirsaida="wav"
#dirsaida="wav${TAMANHO}s"
if [ ! -d $dirsaida ]; then mkdir $dirsaida; fi

#for entrada in `find mp3/ -name "*.mp3" | head -1`
for entrada in `find -L mp3/ -name "*.mp3"`
do
  saida=`echo $entrada | sed 's/mp3/wav/g'`
  dirsaida=`dirname $saida`
  echo "[$entrada] -> [$saida]"
  #if [ ! -d $dirsaida ]; then mkdir $dirsaida; fi

  # extrair a duração do áudio e calcular a quantidade de cortes necessários
  duracao=`ffprobe -i $entrada -show_format -v quiet | sed -n 's/^duration=\([0-9]\+\).*$/\1/p' 2> /dev/null`
  #duracao=`ffprobe -i $entrada -show_format -v quiet | sed -n 's/duration=//p'`
  echo "duração: $duracao s"
  let cortes=duracao/TAMANHO
  #echo "cortes: $cortes"

  inicio=0
  for corte in `seq 1 $cortes`
  do
    let inicio=(corte-1)*TAMANHO
    let termino=inicio+TAMANHO
    saidacorte=`echo $saida | sed -e 's/^wav/wav'$TAMANHO's/' -e 's/.wav$/-'$corte'.wav/'`

    # se for o primeiro corte, cria o diretório (se não existente)
    if [ $corte -eq 1 ]
    then
      dirsaidacorte=`dirname $saidacorte`
      if [ ! -d $dirsaidacorte ]; then mkdir $dirsaidacorte; fi
    fi

    # se já existe arquivo cortado, pular    
    if [ -f $saidacorte ]; then break; fi

    echo "corte $corte: $saidacorte"
    #echo "trecho: $inicio .. $termino"

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
