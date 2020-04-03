# Clase 1 - Color

Los dispositivos que reproducen imágenes cuentan con un _espacio cromática_, en RGB signigica que cada color cuenta con una componente perteneciente a cada color.

La luz visible es parte del espectro electromagnetico (de 380 y 730 nanometros).

Estas longitudes de onda específicas son las que pueden interactuar con los pigmentos de la retina y producir una visualización de color por nuestra parte.

Cada objeto en el mundo emiten diferentes cantidades de energía de cada una de esas longitudes de onda, conodicas como _distribución espectral_ o espectro.

Entonces, el "color" con el que vemos un objeto depende de:

* La luz que lo ilumina
* La luz que refleja

¿Cómo podemos representar con tres componentes (RGB) el infinito espectro de colores?

La retina tiene tres tipos distintos de receptores, uno rojo, uno azúl y otro rojo. También hay otros, que se usan para situaciones de poca iluminación.

La sensibilidad de los bastones receptores está desde el azúl al rojo de menor a mayor sensibilidad.

Al fenómo de engañar al ojo simulando la luz de algun objeto se llama _metamerismo_, dos o más estímulos sean percibidos de la misma forma. Sin esto no sería posible ver el amarillo en las pantallas. Acá también influye la luz que ilumina al objeto.


Aún así, con el espacio RGB no se pueden representar todos los colores percibidos por el ojo humano. Esto se debe a que no podemos replicar estimulos con componente negativa.

Otro espacio puede ser XYZ

* X: sensibilidad del cono rojo
* Y: sensibilidad del cono verde
* Z: sensibilidad del cono azúl

Este espacio tridimensional marca una zona de la cual se puede percibir el color y donde no. Este brinda todos los atributos cromáticos, también los distintos niveles de luminancia. Esto implica que podemos modificar la luminancia sin modificar el color.

Estos tres cuestiones dan lugar a

* Luminancia: Apariencia que no cambia el color
* Saturación: Pureza del color
* Crominancia: El color propiamente dicho

Esto crea aún otro espacio cromático.

## Cuál es el espacio adecuado para el PDI?

Si ploteamos un gran conjunto de imágenes podemos ver que un alto nivel un color implica también un alto valor de los otros componentes. Pero con mucha reduncia. Por eso se utilizar el siguiente espacio

### Espacio YIQ

* Y: eje de luminancia de XYZ. 80% de atención
* I: Rojo - Cyan. 15% de atención
* Q: Magenta - Verde. 5% de atención

La transformación de RGB a YIQ es simplemente cambiar el sistema de coordenadas, se pueden representar en una matríz de 3x3.

$
\begin{bmatrix}
R\\
G\\
B
\end{bmatrix} = 
\begin{bmatrix}
1 & 0.9663 & 0.6210 \\
1 & -0.2721 & -0.6474 \\
1 & -1.1070 & 1.7046
\end{bmatrix}
\begin{bmatrix}
Y\\
I\\
Q
\end{bmatrix}
$

$
\begin{bmatrix}
Y\\
I\\
Q
\end{bmatrix}=
\begin{bmatrix}
0.299 & 0.587 & 0.114 \\
0.595716 & -0.274453 & -0.321263 \\
0.211456 & -1.522591 & 0.311135
\end{bmatrix}
\begin{bmatrix}
R\\
G\\
B
\end{bmatrix}
$

### Actividad práctica

* Tomar una imagen
* Convertirla al espacio YIQ
* Manipularla
* Deconvertir
* Guardar

Llamando $\alpha$ al coeficiente de luminancia y $\beta$ al coeficiente de saturación.

1. normalizar los valores RGB
3. RGB -> YIQ (utilizando la matriz)
4. $Y'=\alpha Y$
5. $I'=\beta I ; Q'=\beta Q$
4. $\alpha$ <= 1
5. Chequear $Y' \le 1$
6. Chequear $-0.5957 \lt I' \lt 0.5957 ; -0.5226 \lt Q' \lt 0.5226$
7. Y'I'Q' -> R'G'B' (rgb normalizado)
8. Llevar de $[0,1]$ a $[0,255]$
