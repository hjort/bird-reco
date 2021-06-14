for sp in `sh listar-especies-coletadas.sh`; do mkdir -p wavbal/$sp; done

ls wavbal

for arq in `sh listar-arquivos-limitados-por-especie.sh`; do cp wav/$arq wavbal/$arq; done

du -csh wavbal/*

