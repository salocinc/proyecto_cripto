## Introducción a la criptografía CC5301-1 - Otoño 2023
**Integrantes:**  
- Nicolás Calbucura  
- Ignacio Gutiérrez

##### _Fecha:_ 17-07-2023   

## Cómo correr el proyecto
Para correr el proyecto, se tiene que ejecutar la siguiente instrucción usando algún entorno virtual:

```python
pip install -r requirements.txt
```
Además, se tiene que instalar rsa ejecutando:

```python
pip install rsa
```
O, utilizando conda:

```python
conda install rsa
```

Luego, para ejecutar el proyecto y poder verlo desplegado en una página web, se tienen que correr los siguientes
comandos, dentro de la carpeta que contiene manage.py:

```python
python manage.py makemigrations app_inicial
python manage.py migrate
python runserver
```