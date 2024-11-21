# Laboratorio 2: Sistema de Gestión de Proyectos de Software

Construir un sistema de gestión de proyectos de software que implique asignación y gestión de tareas por parte de los miembros del equipo. Las acciones que se podran realizar con las tareas son:

- Crear
- Listar
- Marcar como completada
- Editar
- Eliminar

## Requisitos Funcionales

1. **Autenticación de usuarios (Desarrolladores):** Debe existir un usuario administrador que registre
líderes de proyecto. Ésto de debe desarrollar dentro de su propia aplicación. No se debe de usar el admin de
django.

2. Los líderes de proyecto, pueden registrar a los desarrolladores y todos deben poder iniciar sesión
en el sistema con su correo y la contraseña: `12345`.

3. Los líderes pueden crear equipos y asignar desarrolladores. Un desarrollador puede pertenecer a
más de un equipo.

2. **Creación de tareas:** Los líderes deben poder crear tareas con un título, descripción, fecha límite,
prioridad, estado, y observaciones. Para cada equipo.

3. **Listado de tareas:** Los desarrolladores deben poder ver un listado de todas las tareas creadas en
su equipo y las que tiene a su cargo resaltadas para él.

4. **Edición de tareas:** Los desarrolladores deben poder editar las tareas existentes, pero sólo en sus
observaciones y marcarlas como completadas (cambio de estado).

5. **Eliminación de tareas:** Los líderes deben poder eliminar tareas (pero si están asignadas debe
poder desactivarlas y no eliminarlas).

## Docente
Jorge Antonio García Cárdenas.

## Integrantes
- Juan Sebastian Rios Valencia([@Juansecod](https://github.com/Juansecod))