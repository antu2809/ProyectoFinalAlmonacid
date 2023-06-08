Proyecto de Desarrollo Web con Django
Este proyecto es una aplicación web desarrollada con Django, un framework de Python para desarrollo web. La aplicación muestra obras de arte disponibles y permite a los usuarios comprar las obras seleccionadas. A continuación se muestra el orden en el que se prueban las funcionalidades del proyecto:

Para comenzar, abre el siguiente enlace en tu navegador: http://127.0.0.1:8000/view_presentacion/. Aquí verás una página de presentación donde puedes avanzar hacia la página principal haciendo clic en el botón de una rosa.

Después de avanzar hacia la página principal, puedes encontrar las obras de arte disponibles. Para acceder a la tienda, haz clic en el botón de la rosa nuevamente o visita el siguiente enlace: http://127.0.0.1:8000/tienda/.

En la página de la tienda, puedes navegar por las obras de arte y seleccionar las que desees comprar. Cuando encuentres una obra que te interese, haz clic en el botón de "Agregar al carrito" para confirmar tu compra. Esto te llevará a la página de confirmación de compra.

En la página de confirmación de compra, puedes revisar los detalles de tu compra y proporcionar la cantidad que deseas comprar. Al enviar el formulario, se procesará la compra y se creará una orden en la base de datos. Luego, serás redirigido a la página del carrito.

En la página del carrito, puedes completar tu transacción y finalizar la compra.

Además, el proyecto contiene los siguientes archivos y configuraciones importantes:

settings.py: En este archivo, se configuran los ajustes generales de la aplicación, como la configuración de la base de datos, las rutas estáticas, etc.
views.py: Este archivo contiene las funciones de vista que se utilizan para manejar las solicitudes HTTP y renderizar las plantillas correspondientes.
presentacion.html: Este archivo HTML define la estructura y el estilo de la página de presentación.
combined.html: Este archivo HTML es la plantilla principal de la aplicación y muestra la combinación de varias funcionalidades, como información de Instagram, fecha y hora actual, imagen personalizada, saludo personalizado y resultados de búsqueda.
models.py: Este archivo define los modelos de datos utilizados en la aplicación, como las obras de arte, los clientes y las órdenes.
forms.py: En este archivo se definen los formularios utilizados en la aplicación, como el formulario de búsqueda y el formulario de datos del cliente.
