import os
#import sys
import numpy as np
#import pandas as pd
import librosa
#import librosa.display
import soundfile as sf
#import matplotlib.pyplot as plt
#import IPython.display as ipd
import argparse

import warnings
warnings.filterwarnings('ignore')

# diretório de entrada
DIR_ENTRADA = 'mp3'

# diretório de saída
DIR_SAIDA = 'wavbal5'

# duração de cada trecho de áudio
DURACAO_TRECHO = 5 # segundos
SAMPLE_RATE = 16000 # 16 kHz

# calcular a quantidade de pontos na onda
PONTOS_ONDA = SAMPLE_RATE * DURACAO_TRECHO # 16 kHz * 5 s = 80000


def processar_arquivo_especie(especie):

    if not especie:
        return 0

    print("[%s] iniciado" % especie)
    qtde_arquivos = 0
#    return 0

    for arquivo in os.listdir(os.path.join(DIR_ENTRADA, especie)):

        # montar nome do arquivo de entrada
        entrada = os.path.join(DIR_ENTRADA, especie, arquivo)
        if not entrada.endswith('.mp3'):
            continue
        #print("entrada:", entrada)

        prefixo_saida = os.path.join(DIR_SAIDA, especie, arquivo.replace('.mp3', ''))
        #print("prefixo_saida:", prefixo_saida)
        
        # carregar áudio original em formato MP3
        try:
            y, sr = librosa.load(entrada, sr=SAMPLE_RATE, mono=True)
        except:
            print("Erro ao ler arquivo:", entrada)
            continue

        # remover silêncio nas extremidades do áudio
        yt, index = librosa.effects.trim(y)
        duracao = yt.shape[0] / sr
        
        # calcular o número de cortes a serem efetuados no áudio
        numero_cortes = round(duracao / DURACAO_TRECHO)
        if numero_cortes == 0:
            continue
        
        for corte in np.arange(1, numero_cortes + 1):
            saida = "%s-%02d-%03d.wav" % (prefixo_saida, 0, corte)
            
            # calcular trechos de início e fim no áudio
            inicio = PONTOS_ONDA * (corte - 1)
            termino = PONTOS_ONDA * corte
            ytc = yt[inicio:termino]
            
            # gravar arquivo de áudio em formato WAV
            sf.write(saida, ytc, sr, format='wav', subtype='PCM_16')
            qtde_arquivos += 1
            if qtde_arquivos % 29 == 0:
                print("--", saida)

    print("-> qtde_arquivos:", qtde_arquivos, "\n")
    return qtde_arquivos


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--especie', help='Nome científico da espécie a ser processada', type=str, required=True)
    args = parser.parse_args()
    especie = args.especie.strip().lower().replace(' ', '_')
    processar_arquivo_especie(especie)
