# ¿Cuáles son las palabras más importantes en los cuentos de Manuel Rojas según TF-IDF?

Este repositorio tiene por objetivo mostrar cómo la técnica TF-IDF puede ser utilizada para relevar las palabras de los cuentos de Manuel Rojas. La primera pregunta por responder es cómo saber si una palabra es relevante. Una primera aproximación es considerar que una palabra relevante tiene alta frecuencia, pero como veremos más adelante, esto no siempre es así. Para TF-IDF, la palabra será relevante tomando en consideración su frecuencia dentro del cuento, junto con su frecuencia en los otros documentos. Veamos de qué se trata.

*Instrucciones para utilizar el repositorio y argumentos disponibles, ver al final del readme.*

## TF-IDF

TF-IDF significa Term Frequency - Inverse Document Frequency, y es un valor que asigna la importancia del término para el documento (a mayor valor, mayor importancia). ¿Qué tiene de especial este valor? Que asigna mayor valor a términos que ocurran más veces en el documento, a la vez que ocurran menos veces en los otros documentos. Es decir, hay un valor TF para cada término por documento, y un valor IDF para el término en el corpus completo.

Su fórmula es:

![\Large TF[doc][word]=\frac{freq}{totalWords}](https://latex.codecogs.com/svg.latex?\Large&space;TFIDF[doc][word]=TF[doc][word]*IDF[word]) 

Veamos el detalle. Consideremos:

freq = frecuencia de la palabra en el documento\
totalWords = cantidad total de palabras en el document\
N = número total de documentos en el corpus\
Nt = número total de documentos en lo que el término t ocurre\

![\Large TF[doc][word]=\frac{freq}{totalWords}](https://latex.codecogs.com/svg.latex?\Large&space;TF[doc][word]=\frac{freq}{totalWords}) 

![\Large IDF[word]=log(\frac{N+1}{N_t+1})](https://latex.codecogs.com/svg.latex?\Large&space;IDF[word]=log(\frac{N+1}{N_t+1})) 

TF normaliza la frecuencia dado que en textos más largos esperaríamos ver más ocurrencias de la misma palabra.\
IDF toma el logaritmo para [amortiguar](https://en.wikipedia.org/wiki/Natural_logarithm) grandes valores de IDF.

Veamos un ejemplo calculando el valor TF-IDF para las palabras 'el' y 'vapor' en el cuento 'El vaso de leche':

TF['el vaso de leche']['el'] = 0.07468\
IDF['el'] = log (10 / 10) = log(1) = 0.0\
TFIDF['el vaso de leche']['el'] = 0.07468 * 0.0 = 0.0\

Si bien la palabra es la de mayor frecuencia en este cuento, dado que es también una palabra que ocurre en todos los otros cuentos, no resulta ser un término particularmente importante. Es más, su valor TF es mayor que para la siguiente palabra 'vapor', pero su valor IDF la vuelve irrelevante al considerar el comportamiento de la palabra en el corpus.

TF['vapor'] = 0.00471\
IDF['vapor'] = log (10 / 2) = log(5) = 1.60943\
TFIDF['vapor'] = 0.00471 * 1.60943 = 0.00759\

Para este cuento, la palabra 'vapor' es la de mayor valor para el cuento, dado que su frecuencia es alta y aparece únicamente en este cuento.

## Implementación
Hay algunas variantes de la fórmula de TF-IDF para compensar por palabras que no hemos visto previamente en el corpus, o palabras que tienen alta frecuencia en un documento, pero en el resto aparecen escasas veces.

En este caso, para calcular IDF, hemos:
- sumado 1 al denominador para prevenir divisiones por cero (si la palabra no está en nuestro corpus).
- sumado 1 al denominador para que su valor sea siempre positivo (logaritmo de un número entre 0 y 1 es negativo).
- evitado valores de IDF de 0.0 asignándoles arbitrariamente un bajo valor de 1e-7 (con el fin de no excluir completamente palabras como 'el' en el ejemplo anterior).

## Pre-processing
Una vez obtenemos nuestro corpus, debemos pre-procesar los cuentos para analizarlos. Hemos utilizado PyPDF2 para extraer los cuentos del archivo .pdf y seguido el siguiente preprocesamiento:

- remover puntuación y número (i.e. !,.?-)\
- remover caracteres que no sean del alfabeto español (i.e. ...entendieran. *ﬁ*¡ Ah! *Š*me dije*Š*. He ahí dos compadres...)\
- remover espacios en blanco extras\
- convertir todo a minúscula\
- lematización utilizando el modelo 'es_dep_news_trf' de spaCy

## Resultados: TF-IDF Scores
Veamos, entonces, qué palabras son las más relevantes utilizando TF-IDF por cuento. La siguiente tabla muestra las 10 palabras con mayor valor por cuento.

EL DELINCUENTE | | EL VASO DE LECHE | | UN MENDIGO | | EL TRAMPOLÍN | | EL COLO - COLO | | LA AVENTURA DE MR. JAIVA | | PEDRO EL PEQUENERO | | UN LADRÓN Y SU MUJER | | LA COMPAÑERA DE VIAJES | 
 --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- 
cabo | 0.00552 | vapor | 0.00759 | número | 0.00654 | agente | 0.00672 | colocolo | 0.01137 | mr | 0.01217 | pedro | 0.02940 | córdoba | 0.01167 | milán | 0.00538
conventillo | 0.00525 | marinero | 0.00633 | ramírez | 0.00605 | preso | 0.00434 | josé | 0.00627 | tony | 0.01077 | sed | 0.01585 | pancho | 0.00988 | señorita | 0.00448
ladrón | 0.00446 | hambre | 0.00615 | lucas | 0.00423 | esposa | 0.00336 | colo | 0.00470 | jaiva | 0.01030 | chuico | 0.00995 | cabo | 0.00739 | hotel | 0.00402
sánchez | 0.00421 | leche | 0.00569 | moneda | 0.00363 | tren | 0.00306 | vicente | 0.00469 | circo | 0.00983 | jesús | 0.00744 | indio | 0.00539 | duse | 0.00359
maestro | 0.00394 | vainilla | 0.00443 | hospital | 0.00302 | argolla | 0.00269 | manuel | 0.00431 | raúl | 0.00843 | cantina | 0.00692 | fuga | 0.00404 | viajar | 0.00314
delgado | 0.00260 | mar | 0.00379 | sobretodo | 0.00242 | amigo | 0.00223 | montero | 0.00392 | seguel | 0.00749 | chicha | 0.00605 | calabozo | 0.00369 | muchacha | 0.00314
comisaría | 0.00211 | vaso | 0.00331 | cincuenta | 0.00242 | patrón | 0.00203 | ratón | 0.00353 | público | 0.00735 | vaso | 0.00388 | cárcel | 0.00359 | tren | 0.00306
oficial | 0.00211 | hungry | 0.00253 | hilo | 0.00226 | relato | 0.00202 | antuco | 0.00314 | imitación | 0.00421 | rey | 0.00346 | reja | 0.00359 | compañera | 0.00269
inspector | 0.00211 | muelle | 0.00253 | acera | 0.00208 | conciencia | 0.00202 | candelilla | 0.00314 | cómico | 0.00375 | vicho | 0.00303 | francisco | 0.00336 | revista | 0.00269
patio | 0.00210 | puerto | 0.00237 | crepúsculo | 0.00181 | determinado | 0.00202 | caballo | 0.00304 | griego | 0.00375 | don | 0.00303 | marido | 0.00302 | usted | 0.00230

A partir de estas palabras, ya podemos hacernos una idea sobre las temáticas del cuento. Además, podemos percatarnos que casi no hay palabras repetidas, por lo que TF-IDF prefiere palabras que no aparecen en los otros documentos (una diferente implementación podría variar este comportamiento). 

Para cerciorarnos que TF-IDF es de hecho un mecanismo más efectivo que calcular únicamente las frecuencias, comparamos para el cuento 'El vaso de leche' con y sin stop-words. Resultados en la siguiente tabla.

TF-IDF | con stop-words | sin stop-words
--- | --- | ---
'vapor' | el | ser
'marinero' | él | haber
'hambre' | de | tener
'leche' | y | comer
'vainilla' | uno | hambre
'mar' | que | vapor
'vaso' | en | mirar
'hungry' | a | marinero
'muelle' | su | después
'puerto' | no | poder

El lector podrá determinar si las palabras consideradas por TF-IDF son efectivamente más informativas que calcular únicamente la frecuencia, y si son en sí semánticamente importantes en la narración.

## Créditos
Texto “El delincuente, el vaso de leche, el colo–colo y otros cuentos” extraído de https://colegiochile2010.files.wordpress.com/2010/04/un-mendigo1.pdf

## Utilizar el repositorio
```
git clone https://github.com/PdePinguino/tfidf.git
cd tfidf
./tfidf.py
```

Los argumentos disponibles son:\
`-t, --test` testear el código con un toy-corpus definido en tfidf.py (ver main).\
`-s, --scores` imprime en consola los 10 términos con TF-IDF score más alto por documento en corpus.\
`-q, --query QUERY` texto que será con corpus por medio de `cosine similarity` o `matching score`.\
`-c, --cosine` comparar `query` utilizando distancia coseno.\
`-m, --matching` comparar `query` utilizando TF-IDF scores.

Exemplo de uso:\
`./tfidf.py --test`\
`./tfidf.py --scores`
