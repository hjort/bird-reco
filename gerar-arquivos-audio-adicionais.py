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
DIR_SAIDA2 = 'wavbal5a'

# duração de cada trecho de áudio
DURACAO_TRECHO = 5 # segundos
SAMPLE_RATE = 16000 # 16 kHz

# calcular a quantidade de pontos na onda
PONTOS_ONDA = SAMPLE_RATE * DURACAO_TRECHO # 16 kHz * 5 s = 80000

def produzir_arquivos_adicionais(especie, qtde_necessaria):

    if not especie:
        return 0
    
    dir_especie = os.path.join(DIR_SAIDA, especie)
    qtde_existente = len(os.listdir(dir_especie))
    qtde_faltante = (qtde_necessaria - qtde_existente if qtde_necessaria > qtde_existente else 0)
    
    print("[%s] iniciado (necessaria: %d, existentes: %d, faltantes: %d)" % (
        especie, qtde_necessaria, qtde_existente, qtde_faltante))
    qtde_arquivos = 0
    
    variacao = 0

    while (qtde_arquivos < qtde_faltante):
        variacao += 1

        # ler arquivos de entrada em MP3
        for arquivo in os.listdir(os.path.join(DIR_ENTRADA, especie)):

            # sair do laço se atingir a quantidade necessária
            if qtde_arquivos >= qtde_faltante:
                break
            
            # montar nome do arquivo de entrada
            entrada = os.path.join(DIR_ENTRADA, especie, arquivo)
            if not entrada.endswith('.mp3'):
                continue
            #print("entrada:", entrada)

            prefixo_saida = os.path.join(DIR_SAIDA2, especie, arquivo.replace('.mp3', ''))
            #print("prefixo_saida:", prefixo_saida)

            # carregar áudio original em formato MP3
            try:
                y, sr = librosa.load(entrada, sr=SAMPLE_RATE, mono=True)
            except:
                print("Erro ao ler arquivo:", entrada)
                continue
        
            #numero_pontos = y.shape[0]
            #print("-> numero_pontos:", numero_pontos)
            duracao = y.shape[0] / sr
            #print("-> duracao:", duracao, "seg")

            # calcular o número de cortes a serem efetuados no áudio
            numero_cortes = round(duracao / DURACAO_TRECHO)
            #print("-> numero_cortes:", numero_cortes)

            # deslocar o sinal (roll)
            tamanho_roll = variacao * int(PONTOS_ONDA / (variacao + 1))
            #print("--> tamanho_roll:", tamanho_roll)
            yr = np.roll(y, tamanho_roll)
            
            # adicionar ruído ao sinal
            yrs = yr + 0.009 * np.random.normal(0, 1, len(yr))
            
            for corte in np.arange(1, numero_cortes + 1):

                # sair do laço se atingir a quantidade necessária
                if qtde_arquivos >= qtde_faltante:
                    break
                    
                saida = "%s-%02d-%03d.wav" % (prefixo_saida, variacao, corte)
                    
                # calcular trechos de início e fim no áudio
                inicio = PONTOS_ONDA * (corte - 1)
                termino = PONTOS_ONDA * corte
                yrc = yrs[inicio:termino]
                
                duracao = yrc.shape[0] / sr
                if (duracao / DURACAO_TRECHO < 0.3):
                    break

                # gravar arquivo de áudio em formato WAV
                sf.write(saida, yrc, sr, format='wav', subtype='PCM_16')
                qtde_arquivos += 1
                if qtde_arquivos % 29 == 0:
                    print("--", saida)                

    print("[%s] finalizado -> qtde_arquivos: %d\n" % (especie, qtde_arquivos))
    return qtde_arquivos


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--especie', help='Nome científico da espécie a ser processada', type=str, required=True)
    parser.add_argument('--quantidade', help='Quantidade de arquivos necessários', type=int, required=True)
    args = parser.parse_args()
    especie = args.especie.strip().lower().replace(' ', '_')
    qtde = args.quantidade
    produzir_arquivos_adicionais(especie, qtde)
