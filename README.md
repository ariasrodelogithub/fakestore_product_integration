# Integración de Productos con Fake Store API en Odoo

## Instalación y Configuración

1. **Instalación del Módulo:**
   - Clona el repositorio en el directorio de addons de Odoo:
     ```bash
     git clone git@github.com:ariasrodelogithub/fakestore_product_integration.git
     ```

2. **Configuración del Módulo:**
   - Navega a **Configuración > Ajustes de la compañía** en Odoo.
   - Activa la integración en la pestaña "API de Fake Store" y proporciona la URL de la API. Por defecto, la URL es `https://fakestoreapi.com/products`, pero puedes editarla según tus necesidades.
   - Guarda los cambios.

## Descripción del Módulo

Este módulo permite la integración de productos con la API de Fake Store en Odoo. Automáticamente crea o actualiza productos con los datos más recientes de la API diariamente.

## Características

- Creación de nuevos productos si no existen en Odoo.
- Actualización de productos existentes con la información más reciente de la API.
- Actualización diaria automatizada de productos.
- Configuración de credenciales y URL de la API desde los ajustes de la compañía.
- Activación o desactivación de la API desde la configuración de la compañía.
- Los productos se crean o actualizan con todos los datos retornados por la API.
- Carga de la imagen del producto desde la URL proporcionada por la API.
- Exportación de la lista de productos a un archivo de Excel.
- Botón en el sitio web para exportar los productos a Excel.

## Actualización Automática de Datos

Los productos creados o actualizados a través de la API se sincronizan automáticamente con los datos de la API al día siguiente. Cualquier cambio realizado en los datos del producto será sobrescrito con los datos más recientes de la API en la próxima sincronización programada.

## Uso

- Los productos se actualizarán diariamente automáticamente. También puedes forzar una actualización manual ejecutando la acción planificada llamada "Update Products from Fake Store API" desde **Configuración > Técnicas > Automatizaciones programadas**.
- Para exportar la lista de productos creados o actualizados a un archivo de Excel, simplemente ve al sitio web y haz clic en el botón "Exportar Productos a Excel". Este botón se encuentra en el header, al lado del botón "Contact us", y te permitirá descargar los datos de los productos actualizados mediante la API.

