# Taller_1-Topicos_Ing.Software

## 1. Autores
---
[<img src="https://avatars.githubusercontent.com/u/81777898?s=400&u=2eeba9c363f9c474c7fb419ef36562e2d2b6b866&v=4" width=115><br><sub>Mauricio David Correa Hernández.</sub>](https://github.com/MauricioDCH) | [<img src="https://avatars.githubusercontent.com/u/88986744?v=4" width=115><br><sub>Camilo Ortegon Saugter.</sub>](https://github.com/cortegons) |  
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |

## 2. Ejecución.

### Ejecutar el entorno virtual.
Estando dentro de la carpeta de Taller_1-Topicos_Ing.Software.
``` bash
cd /ruta/a/Taller_1-Topicos_Ing.Software
```

En Linux:

``` bash
source venv/bin/activate
```

En Windows:

``` bash
venv\Scripts\activate
```

Para desactivar el entorno.
``` bash
deactivate
```

**En caso de que no esté el entorno virtual.**

Crear el entorno virtual
``` bash
python -m venv venv
```

Actualiza pip

``` bash
pip install --upgrade pip
```

Instalar los requerimientos.
``` bash
pip install -r requirements.txt
```

Ejecuta las migraciones a la base de datos.

``` bash
cd Mrfeast
python manage.py makemigrations
python manage.py migrate
```

Ejecuta el servidor.
Estando dentro del directorio de Mrfeast, ejecutar.

``` bash
python manage.py runserver
```

La ruta inicial es:

``` bash
http://127.0.0.1:8000
```

# Solución de actividades.
Para ver la información de la solución de las actividades, ir a la Wiki del proyecto.

[Link a la Wiki](https://github.com/MauricioDCH/Taller_1-Topicos_Ing.Software/wiki)