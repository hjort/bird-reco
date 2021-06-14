cd wav; for sp in *; do qtd=`find $sp -type f | wc -l`; echo "$sp,$qtd"; done; cd ..
