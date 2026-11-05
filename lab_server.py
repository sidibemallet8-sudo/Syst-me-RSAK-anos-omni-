
"""Serveur local de laboratoire pour ANOS OMNI RSAK V1."""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from anos_omni_rsak import AnosOmniRSAK


def create_lab():
    ai = AnosOmniRSAK()

    rule_id = ai.add_rule(
        {"wheels": 4},
        "motorized"
    )

    ai.add_example(
        {"wheels": 4, "engine": True},
        "motorized"
    )

    ai.add_example(
        {"wheels": 4, "engine": False},
        "not_motorized"
    )

    proposal = ai.propose_reorganization(rule_id)

    return {
        "engine": ai,
        "proposal_id": proposal["id"] if proposal else None
    }


LAB = create_lab()


class RSAKHandler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_GET(self):
        if self.path == "/api/state":
            self.send_json(LAB["engine"].state())
            return

        if self.path in ("/", "/index.html"):
            file_path = Path(__file__).parent / "interface" / "index.html"

            if not file_path.exists():
                self.send_error(404, "Interface introuvable")
                return

            content = file_path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        self.send_error(404, "Route introuvable")

    def do_POST(self):
        global LAB

        try:
            data = self.read_json()

            if self.path == "/api/reset":
                LAB = create_lab()
                self.send_json({
                    "message": "Laboratoire réinitialisé",
                    "state": LAB["engine"].state()
                })
                return

            if self.path == "/api/query":
                attributes = data.get("attributes", {})

                if not isinstance(attributes, dict):
                    self.send_json({"error": "Attributs invalides"}, 400)
                    return

                result = LAB["engine"].query(attributes)
                self.send_json(result)
                return

            if self.path == "/api/validate":
                proposal_id = LAB["proposal_id"]

                if not proposal_id:
                    self.send_json({"error": "Aucune proposition disponible"}, 400)
                    return

                approved = data.get("approved")

                if not isinstance(approved, bool):
                    self.send_json({"error": "Validation booléenne requise"}, 400)
                    return

                result = LAB["engine"].validate(proposal_id, approved)
                self.send_json({
                    "message": "Décision enregistrée",
                    "proposal": result,
                    "state": LAB["engine"].state()
                })
                return

            self.send_error(404, "Route introuvable")

        except (ValueError, KeyError, json.JSONDecodeError) as error:
            self.send_json({"error": str(error)}, 400)

    def log_message(self, format, *args):
        print("[RSAK]", format % args)


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), RSAKHandler)

    print("ANOS OMNI RSAK V1")
    print("Ouvre http://127.0.0.1:8000 dans ton navigateur.")
    print("Arrêt : Ctrl+C")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt du laboratoire.")
        server.server_close()
