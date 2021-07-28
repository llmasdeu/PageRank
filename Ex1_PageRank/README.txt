# Mineria de Dades
# Exercici 1: PageRank
# Nom: Lluís Masdeu
# Login: lluis.masdeu
# Data: 19/10/2019
# Python version: 2.7

Fent proves amb la BETA, he pogut comprovar com, a mesura que s'incrementa el seu valor, el nombre d'iteracions per calcular el PageRank incrementa, així com el valor resultant de les seves planes.

Això es pot deure a que la BETA augmenta la precisió de càlcul dels "nous" rangs. L'algorisme, que té en compte la diferència entre els "nous" i els "vells", i va iterant mentre la seva diferència sigui major que EPSILON, veu retardat el moment d'aturar la comprovació.