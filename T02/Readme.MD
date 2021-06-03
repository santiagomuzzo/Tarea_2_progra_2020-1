# Tarea 02: DCCAFÉ :school_satchel:


**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

## Consideraciones generales :octocat:

* El mesero camina fluidamente, y cumple con los choques y choques especiales. La entidad cliente también fue desarrollada de forma completa. La entidad chef también fue desarrollada de forma completa. La entidad bocadillo no la alcance a terminar , pero aparecen en la mesa luego de que mi mesero se la lleva. Entidad mesa hecha completa, y enitdad DCCafe también a no ser por la funciones que hubiera agregado de bocadillos si es que era necesario (para enviar una señal tal vez).

* Se cumple con Pep8 y extensión de 400 lineas.

* Los archivos se actualizan correctamente y se guarda la partida.

* Drag and drop bien realizado. Lo hice de manera que al lado derecho vayan los chefs con sus mesones y a la izquierda las mesas del café (de manera que sea un café más ordenado). Con el click izquierdo se arrastran y con el derecho se eliminan, pudiendo solo eliminarse hasta quedar una mesa o un chef (siempre va a haber mínimo un chef y una mesa).

* Las interfaces se actualizan y funcionan correctamente y con entendimiento para el jugador. Botón "PAUSAR" sin utilidad. La ventana pre ronda, ronda, y post ronda, llevadas a cabo correctamente. Ventana incicial puede iniciar una nueva partida comenzando la ronda al instante (sin pre ronda), aunque existe la posibilidad de que se genere un mapa con cruce de mesas y mesero, o cruce de chef y mesero :(, no pude implementar eso, pero casi siempre se genera uno que no se cruzan entre si.

* Mi tarea hace casi todo lo que se pidió, excepto tiempos de preparación, pausar, y combinación F+I+N.

* Hice muy pocos comentarios en mi código, sobre todo para cumplir con las 400 lineas de codigo y para cumplir con el pep8. De ser esta decisión, una decisión mala, le pido por favor ayudante si me puede informar eso en el feedback que realices para estar informado para la proxima y última tarea. Y perdón si se le hace muy difícil la comprensión de mi código.

* Detalle de ultimo minuto: Creo que en mi módulo main hay unas líneas comentadas que superan los 100 carácteres. Se me olvido borrarlas, por si podrías no considerarlas, gracias.

<Descripción de lo que hace y que **_no_** hace la tarea que entregaron junto
con detalles de último minuto y consideraciones como por ejemplo cambiar algo
en cierta línea del código o comentar una función>

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Flujo del juego: Hecho completo.

* Entidades:
1. Jugador. Hecho completo.
2. Chef. Hecho completo.
3. Bocadillos. Incompleto; sin tiempo de preparación, sin calidad de pedido.
4. Clientes. Hecho completo.
5. Mesas. Hecho completo.
6. DCCafé. Hecho completo.

* Interfaz:
1. Modelación del programa. Bien modularizado, es cohesivo y poco acoplado; sin embargo presenta un poco de acomplamientoya que hay entidades que instancio en el front-end (ojalá no sea muy grave). Buen uso de señales y threading.

2. Ventanas:
**Ventana Inicio:** Hecha completa.
**Ventana Juego:** Hecha completa(pre-ronda, ronda, y post-ronda).

* Interacción del usuario:
1. Drag and drop: Hecho completo. *a la derecha los chefs y a la izquierda las mesas.*

2. Click: Hecho completo. *con click derecho se eliminan mesa y chef en mesón*

3. Movimiento: Hecho completo *chef usa 16 sprites para cocinar y terminar. Mesero cambia de sprite cuando lleva alimento*
**Colisiones:** Hecho completo
**Colisiones especiales** Hecho completo. *Solo ocurren cuando deben ocurrir; por ejemplo, el mesero no puede entregar un bocadillo si es que no hay cliente, o el cliente ya tiene alimento.*

4. Pausa: No implementado.

* Archivos:
1. mapa.csv: Se actualiza,se recrea y se lee de forma correcta.

2. datos.csv: Se actualiza, recrea y se lee de forma correcta.

3. Parámetros: Hecho complento a excepción de los path de movimiento (y unos pocos números al aire).

* Otras funcionalidades: Hechas todas menos F+I+N *traté pero no me funcionaba bien y además me pasaba de las 400 líneas en módulo mainWindow*

* Bonus: No realizado

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Todos los modulos necesarios se enviaron al repositorio y tienen ubicacion ```T02```
* ```Ventana_Final.ui```, ```Ventana_Perdedor.ui```, ```Ventana_Principal.ui```, ```VentanaInicio.ui``` *Interfaces gráficas requeridad para poder ejecutar correctamente el programa, con ubicacion ```T02```*
* ```mapa.csv```, ```datos.csv```, ```sprites```, *archivos entregados para la correcta realizacion de la tarea, con ubicaion ```T02```*

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```PyQt5.QtGui```: ```QPixmap(), QDrag(), QPainter()```
2. ```PyQt5.QtWidgets```:```QLabel()``` *el resto de la funciones se realizan a través de QtDesigner*
3.  ``` PyQt5.QtCore```: ```Qt, pyqtSignal(), QObject(), QMimeData(), QPoint(), QSize(), QThread(), QRect()``` *se usaron varias funciones de Qt que no la pongo para no hacer tan exteno el readme*
4.  ```PyQt5```:  ```uic```
5.  ```sys```: ```exit()```
6.  ```time```: ```sleep()```
7. ```math```: ```floor()```
8. ```random```: ```randint() , random()```
9. ```os```: ```path / join()```


### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```main.py```: Hecha para <correr el juego.>
2. ```mainWindow.py```: Contiene a ```MainWindow```, que maneja la ventana principal.
3. ```inicial_window.py```: Contiene a ```InicialWindow```, que maneja la ventana principal.
4. ```final_window.py```: Contiene a ```FinalWindow```, que maneja la ventana post-ronda.
5. ```classes_enities.py ```: Contiene todas las entidades del juego excepto ```DCC```.
6. ```entidad_dcc.py```: Contiene a ```DCC```, entidad manejadora de la otras entidades.
7. ```funciones.py```: Hecha para <actualizar y leer los mapas.> Contiene 4 funciones que se encargan de esto.
8. ```el_que_perdio_es_malo.py```: Contiene a ```TheLoserGuy```, que maneja la ventana de perdedor.
9. ```drag_drop.py```: Hecha para <llevar a cabo el drag an drop>, contiene a ```ChefMove``` y a ```TableMove```.

## Supuestos y consideraciones adicionales :thinking: 
Los supuestos que realicé durante la tarea son los siguientes:

1. <El dinero en la interfaz aumenta al instante luego de que el cliente haya recibido su bocadillo y se haya retirado. Esto debido a que mis clientes son respetuosos y siempre pagan su alimento> 
2. <El mapa se divide en: iquierda mesas, derechea mesones con chef. Así tenemos un Café más ordenado y agradable para el consumidor>
3. <Para realizar una compra se realiza con el click izquierdo del mouse, y para quitar un objeto se hace con el click derecho del mouse. Así el jugador creo que se confundirá menos al momento de comprar y retirar>
4. <Mis chefs cocinan solo si los choco sin tener ningún alimento en mano>
5. <Solo puedo entregar bocadillo si es que mi cliente no ha recibido alguno>
6. <A mi Café no le gusta desperdiciar, así que existe la posibilidad, de que mis chefs tengan platos preparados para la siguente ronda, en el caso de que los haya hecho cocinar y no se haya entregado el alimento>


PD: <Hay unos pequeños problemas que ojalá que no afecten: como por ejemplo que **a veces** mis clientes aparecen en el mismo instante a sentarse a sus respectivas mesas en vez de aparecer separadamente. También pasa que **a veces** el sprite de mi chef con la comida lista es un sprite distinto, pero en general es el correcto; esto puede pasar porque relaciono dos clases distintas de chef (Chef, ChefMove)>
<Por último, pedir perdón si es que mi código está un poco complicado de entender y le faltan comentarios. Prometo para la tarea 3 realizar uno mucho más ordenado. Saludos>


-------



