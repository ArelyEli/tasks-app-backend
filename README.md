# Backend - App de Gestión de Tareas

Este repositorio expone una API RESTful construida en Python para gestionar tareas: crear, consultar, actualizar y eliminar. Está diseñada para ejecutarse como funciones Lambda, expuesta usando AWS API Gateway y es protegida con autenticación JWT usando AWS Cognito.

---

##  Endpoints disponibles

| Método | Endpoint       | Descripción                  |
|--------|----------------|------------------------------|
| GET    | /tasks         | Lista todas las tareas       |
| GET    | /tasks/{id}    | Obtiene una tarea por ID     |
| POST   | /tasks         | Crea una nueva tarea         |
| PUT    | /tasks/{id}    | Actualiza una tarea existente|
| DELETE | /tasks/{id}    | Elimina una tarea            |


### `GET /tasks/`

Obtiene la lista de tareas del usuario autenticado.

**Respuesta (200 OK)**
```json
[
  {
    "id": "75fc025a-702a-4d1f-ac22-d2821b6521b1",
    "title": "Comprar leche",
    "description": "Acuérdate",
    "completed": true,
    "created_at": "2025-07-06T18:15:34Z"
  }
]
```

### `GET /tasks/<id>`

Obtiene los detalles de una tarea específica por su ID.
#### Respuesta esperada:
```json
{
  "id": "75fc025a-702a-4d1f-ac22-d2821b6521b1",
  "title": "Comprar leche",
  "description": "Acuérdate",
  "completed": true,
  "created_at": "2025-07-06T18:15:34Z"
}
```

### `POST /tasks`
Crea una nueva tarea.

#### Parámetros esperados
```json
{
  "title": "Comprar leche",
  "description": "Acuérdate",
  "completed": true
}

```

#### Respuesta esperada:
```json
{
    "id": "09f6d48a-2948-4069-b961-22d1842ca812",
    "message": "Task created"
}
```

### `PUT /tasks/<id>`
Actualiza una tarea existente.

#### Parámetros esperados
```json
{
  "title": "Comprar leche",
  "description": "Acuérdate",
  "completed": true
}

```

#### Respuesta esperada:
```json
{
    "id": "09f6d48a-2948-4069-b961-22d1842ca812",
    "message": "Task created"
}
```

### `DELETE /tasks/<id>`
Elimina una tarea existente.

#### Parámetros esperados
```json
{
  "title": "Comprar leche",
  "description": "Acuérdate",
  "completed": true
}

```

#### Respuesta esperada:
```json
{
    "id": "09f6d48a-2948-4069-b961-22d1842ca812",
    "message": "Task created"
}
```


---
## Estructura de datos

Esta aplicación se conecta a una base de datos `MySQL` para almacenar las tareas de cada usuario.
Las credenciales de la base de datos se obtienen dinámicamente desde `AWS Secrets Manager`

| Campo         | Tipo           | Descripción                             |
| ------------- | -------------- | --------------------------------------- |
| `id`          | `CHAR(36)`     | Identificador único (UUID)              |
| `user_id`     | `VARCHAR(100)` | ID del usuario autenticado (de Cognito) |
| `title`       | `VARCHAR(255)` | Título de la tarea                      |
| `description` | `TEXT`         | Descripción opcional                    |
| `completed`   | `BOOLEAN`      | Estado de la tarea (completada o no)    |
| `created_at`  | `TIMESTAMP`    | Fecha de creación                       |

La base de datos se encuentra en AWS RDS, y fue inicializada con el script `schema.sql` que se encuentra en el directorio `core`.

---
## Autenticación y seguridad

Actualmente, la API se encuentra abierta para pruebas, pero está diseñada para utilizar **JWT (JSON Web Tokens)** generados por **AWS Cognito** en producción.

Por lo que ningún usuario no autenticado podrá acceder a los servicios.

---
## Cómo ejecutar 
Descargue y utilice el archivo `tasks.postman_collection.json` incluido en este repositorio.
Debe configurar dos variables de entorno:
- `JWT`: el token JWT obtenido desde AWS Cognito
- `path`: `https://jq2t0u9akl.execute-api.us-east-1.amazonaws.com/Prod`

---
## Documentación de servicios
Se anexa una colección de Postman que puede ser utilizada para probar los servicios.

---
## Ejecución local
Debido a la naturaleza de la aplicación, se debe ejecutar en un entorno de AWS, ya que utiliza servicios de AWS como API Gateway, Lambda y Secrets Manager.

Sin embargo, se puede ejecutar localmente usando SAM.

### Requisitos
- Python 3.12
- SAM CLI
- AWS CLI

### Pasos
1. Instalar SAM CLI
2. Instalar AWS CLI
3. Configurar AWS CLI
4. Ejecutar el siguiente comando:
```bash
sam build
sam local start-api
```

Esto levantará el API Gateway localmente y podrá ser probado usando el archivo `tasks.postman_collection.json`, apuntando al endpoint `http://localhost:3000`.

---
## Despliegue

Esta API se implementará usando SAM, para poder llevar un mejor control de versiones y despliegue.

### Requisitos
- Python 3.12
- SAM CLI
- AWS CLI

### Pasos
1. Instalar SAM CLI
2. Instalar AWS CLI
3. Configurar AWS CLI
4. Ejecutar el siguiente comando:
```bash
sam build
sam deploy
```

Esto desplegará la API en AWS usando servicios como API Gateway, Lambda y Secrets Manager, CloudFormation y podrá ser probada usando el archivo `tasks.postman_collection.json`, apuntando al endpoint en aws.
