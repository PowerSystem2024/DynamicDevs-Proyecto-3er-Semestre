# 🔧 </> Guía para Desarrolladores
Se explican conceptos como estructura de carpetas del proyecto, estructura de las ramas, 
forma de trabajo con Git y GitHub, entre otros.
## Estructura del proyecto
El proyecto contiene la siguiente estructura de carpetas:
```
DynamicDevs-Proyecto-3er-Semestre
├── enertech
    ├── diagrams
│   ├── src
│   │   ├── domain
│   │   └── repository
│   │   └── service
```
- Las entidades estarán dentro de la carpeta `domain`
- Las clases que interactúan con la base de datos irán en `repository`
- Las clases de tipo servicio que van a albergar la lógica de negocio y nuevas funcionalidades estarán en `service`
## Estructura de ramas
Las ramas están compuestas por la rama principal (`main`), la rama `dev` y desde esta nacen las demás ramas.
![Diagrama que muestra la estructura de ramas del proyecto](diagrams/branches.svg)
Cada rama hija de la rama `dev` contiene el siguiente formato: nombre-apellido (ejemplo: `john-doe`).
Si se quieren descargar las ramas de los demás desarrolladores, se puede utilizar el siguiente comando:
```
git fetch origin
```
Esto descargará todas las ramas del repositorio remoto y las mostrará de forma local.
## Flujo de trabajo
### 1. Situarse en la rama correspondiente
```
git checkout nombre-apellido
```
### 2. Actualizar la rama con la rama remota `dev`
```
git pull origin dev
```
> **📝 Nota:** `dev` contendrá el código que cada developer vaya desarrollando.
> El paso siguiente se debe hacer luego de completado el desarrollo de la issue asignada.
### 3. Crear el commit
```
git commit -m "Los usuarios ya se pueden registrar"
```
### 4. Hacer el push a GitHub
```
git push origin nombre-apellido
```
> [!IMPORTANTE] no hacer push a la rama `dev`
### 5. Crear la PR (pull request) en GitHub
Ir a GitHub y levantar una petición de fusión de ramas (Pull Request). 
La petición debe ser la fusión de la rama que contiene el nombre del desarrollador 
hacia la rama `dev` (ej: `john-doe -> dev`). <br>
Una vez creada la PR (pull request), asignar la revisión de dicha PR al responsable correspondiente.