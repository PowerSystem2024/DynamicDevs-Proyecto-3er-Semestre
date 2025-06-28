# EnerTech - Proyecto Integrador 3er Semestre
Proyecto que forma parte del 3er semestre de la Tecnicatura Universitaria en Programación de la UTN San Rafaél, Mendoza.
Desarrollado por el equipo _DynamicDevs_, el proyecto conciste en una aplicación que permita gestionar de forma 
dinámica diferentes órdenes de trabajo que serán creadas por los supervisores y asignadas a los técnicos 
correspondientes. Permite mantener un flujo de trabajo óptimo y una trazabilidad de la actividad de los técnicos 
y las órdenes. Diseñada con motivo de apuntar a empresas de cualquier índole que necesite un control centralizado 
de los mantenimientos y reparaciones realizados a los diversos equipos y activos de la empresa.
## 🚀 Configuración Inicial del Proyecto
Sigue estos pasos para configurar el entorno de desarrollo:
### 1. 📥 Clona el repositorio
```
  git clone git@github.com:PowerSystem2024/DynamicDevs-Proyecto-3er-Semestre.git
```
### 2. 📂 Navega al directorio del proyecto
```
cd DynamicDevs-Proyecto-3er-Semestre
```
### 3. 🐍 Crea el entorno virtual
```
python -m venv .venv
```
### 4. 🔄 Actualiza pip (antes de instalar dependencias)
```
python -m pip install --upgrade pip
```
### 5. ⚡ Activa el entorno virtual
- Windows (PowerShell/CMD)
    ```
    .venv\Scripts\activate
    ```
- Linux/macOS:
    ```
    source .venv/bin/activate
    ```
### 6. 📦 Instala las dependencias
```
pip install -e .
```
### 7. ✅ Verificar instalación (opcional pero recomendado)
```
pip list  # Muestra paquetes instalados
```
> **📝 Nota:** El comando `pip install -e .` instalará todas las dependencias listadas en `setup.py`.
## 🔧 </> Instrucciones para Desarrolladores
[Ir a la documentación técnica del proyecto](enertech/DEVELOPERS.md)
## 🖍️ Diagramas UML
Los diagramas se encuentran en la ruta `enertech\diagrams\`.
### Diagrama de entidades
![Diagrama UML de las entidades](enertech/diagrams/entities-uml.svg)
### Diagrama de repositorios y servicios
![Diagrama UML de los servicios y repositorios](enertech/diagrams/services-and-repos-uml.svg)
