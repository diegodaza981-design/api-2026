# Servicio web de registro e inicio de sesión

Este proyecto implementa un servicio web básico en Python para:

- Registrar usuarios (`POST /register`)
- Iniciar sesión (`POST /login`)

> El servicio recibe `usuario` y `contrasena`. Si la autenticación es correcta, responde con `Autenticación satisfactoria`; si no, devuelve `Error en la autenticación`.

## Ejecutar

```bash
python3 app.py
```

Servidor por defecto en `http://0.0.0.0:8000`.

## Ejemplos de uso

### 1) Registrar usuario

```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"usuario":"ana","contrasena":"1234"}'
```

### 2) Login correcto

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"usuario":"ana","contrasena":"1234"}'
```

### 3) Login incorrecto

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"usuario":"ana","contrasena":"otro"}'
```
