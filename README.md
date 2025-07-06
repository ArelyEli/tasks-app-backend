# Backend - App de Gestión de Tareas

Este repositorio expone una API RESTful construida en Python para gestionar tareas: crear, consultar, actualizar y eliminar. Está diseñada para ejecutarse como funciones Lambda y es protegida con autenticación JWT usando AWS Cognito.

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
{
  "title": "Crear el Frontend",
  "description": "Crear el frontend de la aplicación en Angular",
  "completed": false
}
```

### GET /tasks/<id>

Obtiene los detalles de una tarea específica por su ID.
#### Respuesta esperada:
```json
{
  "title": "Comprar leche",
  "description": "Acuérdate",
  "completed": true
}
```

### POST /tasks
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
  "id": "75fc025a-702a-4d1f-ac22-d2821b6521b1",
  "title": "Comprar leche",
  "description": "Acuérdate",
  "completed": true,
  "created_at": "2025-07-06T18:15:34Z"
}

```
## PUT /tasks/<id>
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
  "id": "75fc025a-702a-4d1f-ac22-d2821b6521b1",
  "title": "Comprar leche",
  "description": "Acuérdate",
  "completed": true,
  "created_at": "2025-07-06T18:15:34Z"
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

---
## Autenticación y seguridad

Actualmente, la API se encuentra abierta para pruebas, pero está diseñada para utilizar **JWT (JSON Web Tokens)** generados por **AWS Cognito** en producción.

---

## Despliegue

Esta API se implementará en AWS API Gateway.

Las funciones individuales pueden estar configuradas como AWS Lambda Functions.

---
## Cómo ejecutar 
Descargue y utilice el archivo `tasks.postman_collection.json` incluido en este repositorio.
Debe configurar dos variables de entorno:
- `JWT`: el token JWT obtenido desde AWS Cognito
- `path`: `https://jq2t0u9akl.execute-api.us-east-1.amazonaws.com/Prod`

