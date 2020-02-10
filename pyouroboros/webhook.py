from logging import getLogger
import threading
import json, ssl

from http.server import BaseHTTPRequestHandler, HTTPStatus, ThreadingHTTPServer


class HookHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.server.config.webhook_insecure:
            resp = {"status": "success", "path": self.path}
            status = HTTPStatus.OK

            for mode in self.server.config.modes:
                self.server.config.scheduler.add_job(mode.update, name=f'Webhook triggered update for {mode.socket}')
        else:
            try:
                if self.server.config.webhook_users is not None:
                    c = self.request.getpeercert()
                    cn=list(filter(lambda x: x[0][0] == "commonName", c["subject"]))
                    if len(cn) == 1:
                        if cn[0][0][1] not in self.server.config.webhook_users:
                            raise Exception("Unauthorized")
                    else:
                        raise Exception("Malformed Cert")
            except Exception as e:
                resp = {"status":"unauthorized"}
                status = HTTPStatus.UNAUTHORIZED
            else:
                resp = {"status": "success", "path": self.path}
                status = HTTPStatus.OK

                for mode in self.server.config.modes:
                    self.server.config.scheduler.add_job(mode.update, name=f'Webhook triggered update for {mode.socket}')
                #return 'updated'

        dresp = json.dumps(resp).encode("utf8")
        self.send_response(status)
        self.send_header("Content-type", "application/json; charset=utf8")
        self.send_header("Content-Length", str(len(dresp)))
        self.end_headers()
        self.wfile.write(dresp)


class HookManager(object):

    def serve(self, config):
        httpd = ThreadingHTTPServer((config.webhook_addr, config.webhook_port), HookHandler)
        if not config.webhook_insecure:
            args = {}
            if config.webhook_cacert:
                args = {"cert_reqs": ssl.CERT_REQUIRED, "ca_certs": config.webhook_cacert}
            httpd.socket = ssl.wrap_socket(httpd.socket, certfile=config.webhook_cert, keyfile=config.webhook_key, ssl_version=ssl.PROTOCOL_TLSv1_2,
                                           server_side=True, **args)

        httpd.config = config
        httpd.serve_forever()

    def __init__(self, config, modes, scheduler):
        self.config = config
        self.logger = getLogger()
        if not config.webhook:
            return

        self.config.scheduler = scheduler
        self.config.modes = modes

        threading.Thread(target=self.serve, kwargs=dict(config=self.config), daemon=True).start()

