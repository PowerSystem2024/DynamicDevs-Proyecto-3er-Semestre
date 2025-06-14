## Guía para Desarrolladores

### Clonar el Repositorio
Clonar el repositorio con uno de los siguientes comandos:
> Opción HTTPS <br> `git clone https://github.com/PowerSystem2024/DynamicDevs-Proyecto-3er-Semestre.git`

> Opción SSH <br> `git clone git@github.com:PowerSystem2024/DynamicDevs-Proyecto-3er-Semestre.git`

### Estructura del Proyecto
El proyecto va a contener la siguiente estructura de carpetas:
```
enertech
├── src
│   ├── domain
│   └── repository
```
Para trabajar, crear las clases/entidades dentro de la carpeta `domain`. Las clases que van a interactuar con la base de datos irán en `repository`.

### Estructura de Ramas
Las ramas están compuestas por la rama principal (`main`), la rama `dev` y desde ésta nacen las demás ramas.
![Diagrama que muestra la estructura de ramas del proyecto](diagrams/branches.svg)
Cada rama de cada desarrollador contiene el siguiente formato: nombre-apellido (ejemplo: `john-doe`).
Si se quieren descargar las ramas de los demás desarrolladores, se puede utilizar el siguiente comando:
> `git fetch orogin`

Esto descargará todas las ramas del repositorio remoto y las mostrará en tu repositorio local.

### Flujo de Trabajo
El flujo de trabajo que se debe tener es el siguiente:
> `git checkout nombre-apellido` para cambiar a la rama que les pertenezca

Una vez situado en la rama correspondiente, actualizar la rama para sincronizar los cambios que contiene la rama remota `dev` utilizando el siguiente comando:
> `git pull origin dev`

Completado el desarrollo de la funcionalidad en la que se estuvo trabajando, subir el código a la rama que contiene su nombre, que fue en la que se trabajó. Ejemplo:
> `git push origin john-doe`

Ir a GitHub y levantar una petición de fusión de ramas (Pull Request). La petición debe ser la fusión de la rama que contiene el nombre del desarrollador hacia la rama `dev` (_john-doe -> dev_)

Una vez creada la PR (pull request), asignar la revisión de dicha PR al responsable correspondiente.

### Importante
Actualizar tu rama es crucial y siempre tiene que ser lo primero a realizar antes de comenzar a trabajar.
El proyecto puede ser desarrollado en el IDE de tu preferencia (IntelliJ, NetBeans o Visual Studio Code).

Se tiene que recordar que las PR se realizan únicamente a la rama `dev`, por lo tanto se debe prestar mucha atención porque se puede realizar una petición a una rama erronea.