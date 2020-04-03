# Clase 1 - Introducción

## Temas del curso

1. Color, espacios cromáticos
2. Arítmetica de pixels y manipulación de histogramas
3. Transformadas de Fourier
4. Procesamiento por convolución
5. Procesamiento morfológico
6. Segmentación, reconocimiento

## Para promocional el curso

Trabajos prácticos y un trabajo final integrador.

Trabajo final de mayor complejidad.

_Propuesta_: proponer un problema y resolverlo, o proponer un tema teórico e investigar, desarrollar alguna monografía. Or something in between. En lo posible la temática del trabajo final se propone que sea un tema concreto.

## Bibliografía

- Rafael González and Richard Woods. Tratamiento Digital de Imágene Addison-Wesley.
- John Russ. The Image Processing Handbook (6th ed)
- También en las filminas se incluyen links a otros recursos.

---

# PDI - Introducción

Una imagen _digital_ es una versión muestreada y cuantizada de una imagen _real_ (continua). Es importante recordar los pasos que llevan del mundo real al discreto y visceversa.

1. Señal
2. Señal muestreada (discreta y analógica)
3. Señal cuantizada (digital)
4. Señal codificada

- 1 a 2: Muestro
- 2 a 3: Cuantización
- 3 a 4: A/D
- 4 a 3: Decodificación
- 3 a 2: D/A
- 2 a 1: Reconstrucción

En lso formatos usuales, el muestreo se hace en _pixels_. Cada pixel contiene valores RGB que conforman su color.

Para entender el efecto del muestreo se puede hacer la analogía con bajar la resolución de una imagen pero mantener el tamaño de cada pixel. Se perderá nitidez.

El deterior producido por tener menos muestras de una imagen se conoce como aliasing, a estudiar cuando veamos eel model frecuencial de las imágenes.

La cuantización reduce el espectro de valores que cada componente puede tomar. Por ejemplo, reducir de 8 a 4 bits cada componente primario del pixel.

Una imagen está representada a través de una matriz. Cada elemento de la matriz cuenta con un componente de cada primario. Puede ser este valor esté representado en un mismo valor escalar.

---

# Investigar

En un lenguaje de programación:

1. Abrir un archivo de imagen y disponer dee la información de una componente imagen
2. Métodos para guardar la información de una componente imagen a un archivo
3. Métodos para acceder a una componente imagen y leer o modificar su contenido
4. Métodos para graficar o modificar una componente imagen

Fundamentalmente se piden los tres primeros.

Esto constituye el **Práctico Cero**.
