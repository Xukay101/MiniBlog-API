# MiniBlog-API

Una API que permite la creación y gestión de un miniblog personal, incluyendo posts, comentarios y categorías.

## Tabla de Contenidos

- [Descripción del Repositorio](#descripción-del-repositorio)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Endpoints](#endpoints)
- [Configuración Inicial](#configuración-inicial)
- [Testing](#testing)
- [Tecnologias Utilizadas](#tecnologías-utilizadas)

## Descripción del Repositorio

Este repositorio contiene una aplicación en Flask que permite a los usuarios crear, gestionar y interactuar con un miniblog personal. La aplicación ofrece funcionalidades de autenticación, gestión de posts, comentarios y categorías.
La documentación detallada del proyecto está disponible en [documentacion](https://Xukay101.github.io/MiniBlog-API/).

## Estructura del Proyecto

- **app**: Directorio principal de la aplicación.
  - **auth**: Módulo para autenticación, incluyendo handlers y vistas.
  - **categories**: Módulo para gestionar categorías de posts.
  - **comments**: Módulo para gestionar comentarios en posts.
  - **posts**: Módulo para gestionar posts.
  - **config.py**: Configuraciones generales de la aplicación.
  - **models.py**: Define los modelos de la base de datos.
  - **schemas.py**: Esquemas Pydantic para validación y serialización.
  - **utils.py**: Utilidades varias.

- **docker-compose.yml**: Define y configura los servicios de Docker.
- **Dockerfile**: Instrucciones para construir la imagen Docker de la aplicación.
- **docs**: Contiene documentación adicional y archivos relacionados.
- **Makefile**: Comandos útiles para gestionar y desplegar la aplicación.
- **migrations**: Contiene archivos relacionados con las migraciones de la base de datos.
  - **backup**: Backups de migraciones anteriores.
  - **versions**: Scripts específicos de migración para actualizar la base de datos.

- **README.md**: Documentación principal del proyecto.
- **requirements.txt**: Lista de dependencias del proyecto.

## Endpoints

### Módulo de Auth:
- `POST /api/auth/register`: Registrar un nuevo usuario.
- `POST /api/auth/login`: Iniciar sesión (Obtiene un JWT Token).
- `POST /api/auth/verify`: Verifica un JWT Token.
- `POST /api/auth/logout`: Revoca un token por el tiempo de vida que le queda.

### Módulo de Posts:
- `GET /api/posts`: Listar todos los posts.
- `POST /api/posts`: Crear un nuevo post.
- `GET /api/posts/{post_id}`: Obtener detalles de un post específico.
- `PUT /api/posts/{post_id}`: Actualizar un post específico.
- `DELETE /api/posts/{post_id}`: Eliminar un post específico.

### Módulo de Comentarios:
- `GET /api/posts/{post_id}/comments/`: Listar todos los comentarios de una publicación.
- `GET /api/posts/{post_id}/comments/{comment_id}`: Obtener comentario especifico.
- `POST /api/posts/{post_id}/comments/`: Crear un nuevo comentario en una publicación.
- `PUT /api/posts/{post_id}/comments/{comment_id}`: Actualizar un comentario.
- `DELETE /api/posts/{post_id}/comments/{comment_id}`: Eliminar un comentario.

### Módulo de Categorías:
- `GET /api/categories`: Listar todas las categorías.
- `GET /api/categories/{category_id}`: Obtener categoria especifica.
- `POST /api/categories`: Crear una nueva categoría.
- `PUT /api/categories/{category_id}`: Actualizar una categoría.
- `DELETE /api/categories/{category_id}`: Eliminar una categoría.

## Configuración Inicial
1. Clona este repositorio:
```bash
git clone https://github.com/Xukay101/MiniBlog-API.git
cd MiniBlog-API
```
2. Construye los servicios:
```bash
make build
```
3. Inicia los servicios:
```bash
make up
```
4. Aplica las migraciones:
```bash
make upgrade
```

## Testing
Para ejecutar las pruebas dentro del contenedor Docker, ejecute:
```bash
make test
```
Después de configurar con make build y make up, puede ejecutar las pruebas. Es importante asegurarse de que la aplicación se construye y se inicia primero para que las pruebas funcionen correctamente.

## Tecnologías Utilizadas
*  Flask
*  PostgreSQL
*  Redis
