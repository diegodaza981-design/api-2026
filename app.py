#!/usr/bin/env python3
"""Servicio web simple para registro e inicio de sesión.

Este servidor expone dos endpoints:
- POST /register
- POST /login

El cuerpo debe enviarse en JSON con los campos:
{
  "usuario": "nombre",
  "contrasena": "secreta"
}
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from typing import Dict


# Almacenamiento en memoria para los usuarios registrados.
# Clave: nombre de usuario, Valor: contraseña.
USERS: Dict[str, str] = {}


class AuthHandler(BaseHTTPRequestHandler):
    """Maneja las solicitudes HTTP para registro y autenticación."""

    def _send_json(self, code: int, payload: dict) -> None:
        """Envía una respuesta JSON con el código HTTP indicado."""
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        """Lee y valida el cuerpo JSON de la solicitud."""
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            return None

        raw_body = self.rfile.read(content_length)
        try:
            data = json.loads(raw_body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None

        if not isinstance(data, dict):
            return None
        return data

    def do_POST(self) -> None:  # noqa: N802 (firma requerida por BaseHTTPRequestHandler)
        """Gestiona peticiones POST para /register y /login."""
        data = self._read_json_body()
        if data is None:
            self._send_json(400, {"error": "Cuerpo JSON inválido"})
            return

        usuario = data.get("usuario")
        contrasena = data.get("contrasena")

        # Validamos que ambos campos existan y sean texto no vacío.
        if not isinstance(usuario, str) or not usuario.strip():
            self._send_json(400, {"error": "El campo 'usuario' es obligatorio"})
            return
        if not isinstance(contrasena, str) or not contrasena:
            self._send_json(400, {"error": "El campo 'contrasena' es obligatorio"})
            return

        if self.path == "/register":
            self._handle_register(usuario, contrasena)
            return

        if self.path == "/login":
            self._handle_login(usuario, contrasena)
            return

        self._send_json(404, {"error": "Endpoint no encontrado"})

    def _handle_register(self, usuario: str, contrasena: str) -> None:
        """Registra un nuevo usuario en memoria."""
        if usuario in USERS:
            self._send_json(409, {"error": "El usuario ya existe"})
            return

        USERS[usuario] = contrasena
        self._send_json(201, {"mensaje": "Usuario registrado correctamente"})

    def _handle_login(self, usuario: str, contrasena: str) -> None:
        """Valida credenciales y responde según el resultado."""
        if USERS.get(usuario) == contrasena:
            self._send_json(200, {"mensaje": "Autenticación satisfactoria"})
            return

        self._send_json(401, {"error": "Error en la autenticación"})


def run_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    """Inicia el servidor HTTP."""
    server = HTTPServer((host, port), AuthHandler)
    print(f"Servidor de autenticación activo en http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
