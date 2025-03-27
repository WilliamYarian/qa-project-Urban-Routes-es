**Proyecto Urban Routes**

**Descripción**

Urban Routes es un proyecto de automatización de pruebas diseñado para validar la funcionalidad de una aplicación de rutas urbanas. Utiliza Selenium para automatizar la interacción con el sitio web y verificar distintos flujos como búsqueda de taxis, manejo de tarifas, y más.

**Tecnologías utilizadas**

-Python 3.x

-Selenium

-WebDriver para navegadores (Chrome, Firefox, etc.)

-pytest

**Ejecución de Pruebas**

Para ejecutar las pruebas, asegúrate de tener instalados los paquetes pytest y Selenium.

pip install pytest o desde Python Packages buscar 'pytest' e instalar

pip install selenium o desde Python packages buscar 'selenium' e instalar


**Estructura del Proyecto**

-**methods.py:** 
Contiene métodos de interacción con los elementos de la página.

-**-test_main.py:** 
Contiene los casos de prueba que utilizan los métodos definidos.

-**data.py:** Archivos de datos que almacenan constates utilizadas en las pruebas.

**Funcionalidad de las Pruebas**

Las pruebas automatizadas cubren los siguientes pasos del flujo de solicitud de un taxi:

-Configurar la dirección:
Se simula la configuración de la dirección de origen asi como el destino del viaje .

-Seleccionar la tarifa Comfort.

-Completar el número de teléfono.

-Agregar una tarjeta de crédito: Se simula la interacción con el pop up de "Agregar una tarjeta" y se asegura que el campo CVV (id="code" class="card-input") pierda el enfoque para habilitar el botón de enlace.

-Escribir un mensaje para el conductor.

-Solicitar una manta y pañuelos.

-Añadir amenidades, en este caso son 2 helados.

-Esperar la búsqueda de un taxi: Se asegura que el modal de búsqueda de conductor aparezca correctamente y que la cuenta regresiva se inicie hasta confirmar que un conductor sea asignado.

**Problemas Comunes**

ElementClickInterceptedException: 
Asegúrate de que los elementos no están cubiertos por otros elementos o que las animaciones estén completas antes de realizar acciones de clic.

TimeoutException: Revisa los tiempos de espera para asegurarte de que la página haya cargado completamente.

**Clonar el repositorio:**

-git clone git@github.com:username/qa-project-Urban-Routes-es.git

-Abrir PyCharm

-Ir a File, Open, Buscar la carpeta donde guardamos los archivos clonados del repositorio, seleccionar los archivos, data, main, urbanroutes, utilities y readme.

-Seleccionar el archivo main.py

-Asegurarse de que es el archivo actual (current file).

-Presionar play para comenzar la ejecucion del programa main.py