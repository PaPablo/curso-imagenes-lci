# Clase 2 - Histograma

## Histograma de luminancias

Podemos ver que una imagen que esté "quemada", o "muy oscura" o que no se distingan los objetos presentes porque "le falta contraste".

Existe una forma de describir estas situaciones y poder pensar métodos para poder corregirlas. A través de un "histograma de luminancias". Que muestra la distribución de los valores de la luminancia de cada píxel.

La técnica para manipular este histograma y corregir los defectos de la imagen se llama *ecualización*.

### Cómo encontramos este histograma

En el especio YIQ, el valor Y representa la luminancia. Que se puede hallar con la matriz de la clase anterior.

$Y= 0.299*R+0.587*G+0.114*B$

Se recorre toda la imagen, se calcula el valor Y para todos los píxeles de la imagen, calcular el valor Y.

Luego, se subdivide el rango de posibles valores de Y en rangos de igual tamaño. Se cuenta la cantidad de los valores Y que pertenece a cada rango. Por último se normalizan los valores de los contadores para que representen un valor correspondiente al porcentaje de los valores totales de luminancia generados (0-100%)

* Ejercicio: Hacer un histograma para una imagen, probar con 10, 20  y 50 valores

Una idea para corregir esto es manipular la luminancia:

* Ejercicio: probar esto

Spoiler: no va a andar, porque si se manipula la luminancia, aún así los valores que puede tomar Y no van a cambiar, por lo que la imagen va ser más luminosa pero no mejoró su calidad. El histograma se desplazó pero no se aplanó.

Hay que "desparramar" los píxeles oscuros y "comprimir" los brillantes, en el caso de una imagen oscura. En el caso de una imagen muy quemada, se debe hacer lo opuesto.

*Qué podemos hacer?*

Ninguna función lineal no nos va a ayudar, porque va a desplazar el histograma. 

Para el caso de las imágenes oscuras, podemos usar una función que:

* Arranque en 0,0
* Su valor sea 1 un 1,1
  
Una función de raiz, y un logaritmo desplazado cumple con nuestro cometido.

Entonces podemos utilizar, por ejemplo, la función *raiz cuadrada* para esto.

Este procesamiento se puede aplicar aún sin conocer el histograma, solamente viendo que la imagen está oscura.

Vale la pena observar que la función comienza muy despegada de la identidad y termine muy cercana.

En el caso de una imagen muy luminosa, se puede utilizar una función cuadrado, que nos permite oscurer la imagen, pero haciendo que se oscurezca mucho al principio y poco sobre el final.

### Aplicar estas ideas

Repetir el workflow de la clase pasada, pero sólo transformando Y a Y'

---

Pero qué pasa si queremos comprimir y desparramar en diferentes zonas? En el caso de una imagen mixta.

Se debe usar una función "lineal a trozos", donde hay dos valores umbrales. Fuera de esos valores, es constante 0 y 1, dentro del umbral es lineal.

El problema con este procesamiento es que se deben conocer los valores mínimos y máximos de Luminancia.

* Ejercicio Práctico: Desarrollar un aplicativo que permita cargar una imagen y poder procesarla con los distintos filtros que se propusieron (raíz, cuadrado, o lineal a trozos con los distintos umbrales)

---

Hay otras ideas que se han desarrollado en estos temas.

* Hitograma correcto o adecuado:
  * El histograma debe poder modelarse con una distribución gaussiana con media 0.5 y variancia 1. Normalización del histograma.
  * Todas las luminancias distribuidas con igual frecuencia. Ecualización del histograma.

Estas técnicas no son complejas, en wikipedia se pueden encontrar fácilmente.

-> **Agregar al aplicativo**