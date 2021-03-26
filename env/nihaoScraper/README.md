# NiahaoScraper guide

La spider que analiza todos los detalles de los productos desde el link padre es `nihao`, esta regresa un `NihaoscraperItem` el cual tiene las siguientes variables


- `category`
- `subcategory`
- `product_id`
- `name`
- `link`
- `price`
- `currencyRate`
- `priceDiscount`
- `specialPrice`
- `productPrice`
- `weight`
- `stock`

Esto con la facilidade de evitar después una limpieza de variables como se hacía anteriormente en las spiders: `categorySpider`, `subcategorySpider`, `productsSpider` y `detailsSpider`. Igual anida los valores de cada una de estas para poder heredar valores entre funciones y facilitar la categorización de estos agregándoles de una vez el link del producto, su categoría y subcategoría, para correrlo es recomendable abrir un env de python en el cual tengamos instalado scrapy, después de esto solo es cosa de correr


				scrapy crawl categorySpider -O <name>.json


El nombre y el tipo de archivo puede ser cualquiera, hasta un csv, recomiendo usar un json por si alguno de los productos tenga alguna coma o algún valor que pueda aterar los datos.


# Otras spiders

Las otras 4 diferentes spiders: `categorySpider`, `subcategorySpider`, `productsSpider` y `detailsSpider`.

Cada una de ellas (salvo `categorySpider`) necesita un archivo .json donde se encuentren los links que se desean investigar, por ejemplo `categorySpider` está diseñada para imprimir las categorías de productos que la página maneja, esto corréndolo desde la terminal con el comando:

				scrapy crawl categorySpider -O categories.json

Esto genera el json con el nombre de cada categoría con su respectivo url, el nombre del archivo necesariamente tiene que ser categories.json, ya que `subcategorySpider` busca uno llamado así. 

Se decidió usar una spider por cada adentramiento a la página, ya que se le da al usuario mas libertad de decidir más específicamente los productos que desea investigar, por ejemplo, al correr `categorySpider` y obtener su respectivo json podemos modificar las categorías existentes que nos ofrece la página; esto para investigar todas o solo algunas, para esto solo es necesario entrar en el json y borrar la línea de la o las categorías que no nos interesen.

Como se mencionó anteriormente, cada spider requiere de un comando diferente para poder acceder a dicha categoría, dichos comando se listan a continuación

				scrapy crawl categorySpider -O categories.json


				scrapy crawl subcategorySpider -O subcategories.json


				scrapy crawl productsSpider -O products.json


				scrapy crawl detailsSpider -O details.json

No es necesario correr los comandos en ese orden ya que existen los archivos de links correspondientes en el repositorio, pero se recomienda correrlos así por si la página cambiase algo en su estructura.

Al igual que podemos modificar categories.json se puede modificar subcategories.json para que solo inspeccione subcategorías de las categorías listadas en categories.json. Esto es solo con el fin de reducir el tiempo de adiquisión de datos, ya que la página tiene un stock mayor 108,000 productos; lo cual puede resultar bastante tardado si sólo se desea por ejemplo ver los anillos que vende.
