
# Actualizador Masivo de Tickets Zendesk

---

## 🎯 Propósito  
Automatiza la actualización masiva de tickets en Zendesk, copiando el RUT/Cedula desde campos de usuario a un campo personalizado específico en tickets de un formulario designado.

---

## 📂 Estructura del Proyecto  
```plaintext
📂 tu_proyecto/
├── 📂 src/                  # Código principal
│    └── 📄 main.py          # Script de ejecución
├── 📂 config/               # Configuraciones
│    ├── 📄 settings.py      # Variables públicas (ej: URLs, IDs)
│    └── 📄 .env             # Variables sensibles (API keys, credenciales - ignorado por git)
├── 📂 output/               # Resultados generados
│    └── 📄 tickets_actualizado.csv      # Auditoría final
├── 📄 README.md             # Documentación del proyecto
└── .gitignore              # Archivos excluidos del control de versión
```

---

## ⚙️ Configuración
Variables de entorno:

Crea un archivo .env en la carpeta config/ con las credenciales de Zendesk:

```python
ZENDESK_EMAIL = "tu_email@empresa.com"
ZENDESK_API_TOKEN = "tu_token_api"
ZENDESK_SUBDOMAIN = "tusubdominio"
```

Modificar el archivo setting.py

```python
FORM_NAME = "Nombre del formulario a buscar"
CUSTOM_FIELD_ID = "Id del Campo a actualizar en el ticket"
RUT_FIELD_NAME = "Nombre del campo RUT/Cedula en User Fields"
```

---

## 🚀 Ejecución
Instalar dependencias (si aplica):

```python
$ pip install -r requirements.txt  # Si existe un archivo de dependencias
```

Ejecutar el script:

```python
$ python3 -m src.main
```

---

## 📄 Salida
El script genera un archivo tickets_actualizado.csv en la carpeta **output/**, que incluye:

* Auditoría completa de los tickets actualizados.
* Errores y éxitos durante el proceso.

Ejemplo de salida en la consola:

```python
Bienvenido al Sistema de Actualización de Tickets
➤ Instancia configurada: SLS-ZERVIZ-5
➤ Formulario a buscar : Solicitud
➤ Nombre del campo de usuario : RUT/Cedula
➤ ID del campo a actualizar : 360041811351

📝 Tickets encontrados: 107
Progreso: 100.0% (107/107)
✅ Proceso completado. Archivo 'tickets_actualizado.csv' generado
```

---

## ❓ Soporte
Para problemas técnicos o sugerencias, contactar a Jesús Lobatón.

---

**Desarrollado por:** Jesús Lobatón  
**Fecha de creación:** 19/03/2025  

