import json
import socket
from contextlib import contextmanager

class LocalApi:
    HOST = 'localhost'
    PORT = 25258

    class EntryPoint:
        CREATE_PROJECT = 'create_project'
        RUN_PIPELINE = 'run_pipeline'
        RUN_MODULE = 'run_module'
        TASK_INFO = 'task_info'
        TASK_DETAILS = 'task_details'

    class Error:
        class ApiError(Exception):
            pass

        class UnknownDataError(ApiError):
            def __str__(self):
                return 'Unknown data or empty request message. This could be an internal error.'

        class UnknownBodyError(ApiError):
            def __str__(self):
                return 'Cannot decode message body. This could be an internal error.'

        class UnknownEntryPointError(ApiError):
            def __str__(self):
                return 'Unknown entry point.'

        class IncorrectFormatError(ApiError):
            def __init__(self, msg):
                self.message = msg

            def __str__(self):
                return f"Incorrect request format: {self.message}"

        class InternalError(ApiError):
            def __init__(self, msg):
                self.message = msg

            def __str__(self):
                return f"Internal error: {self.message}"

    class MessageProtocol:
        @staticmethod
        def read_from_socket(sock):
            # read length
            len_hex = sock.recv(8).decode()
            length = int(len_hex, 16)
            if length == 0:
                raise LocalApi.Error.UnknownDataError
            # read body
            body = sock.recv(length).decode()
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                raise LocalApi.Error.UnknownBodyError

        @staticmethod
        def write_to_socket(sock, message):
            json_str = json.dumps(message)
            sock.sendall(f"{len(json_str):08x}{json_str}".encode())

        @staticmethod
        def write_error(sock, message):
            LocalApi.MessageProtocol.write_to_socket(sock, {"status": "error", "message": message})

        @staticmethod
        def write_success(sock, message):
            LocalApi.MessageProtocol.write_to_socket(sock, {"status": "success", "message": message})

    class Client:
        def __init__(self):
            self.host = LocalApi.HOST
            self.port = LocalApi.PORT

        @contextmanager
        def connect(self):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.host, self.port))
                yield sock
            except:
                yield {"status": "error", "message": f"Cannot connect to {self.host}:{self.port}."}
            finally:
                if isinstance(sock, socket.socket):
                    sock.close()

        def create_project(self, uid, name):
            with self.connect() as server:
                LocalApi.MessageProtocol.write_to_socket(server,
                    {"entry_point": LocalApi.EntryPoint.CREATE_PROJECT, "arguments": {"uid": uid, "name": name}})
                return LocalApi.MessageProtocol.read_from_socket(server)

        def run_pipeline(self, uid, proj_id, pipeline_id, inputs, params):
            with self.connect() as server:
                LocalApi.MessageProtocol.write_to_socket(server,
                    {"entry_point": LocalApi.EntryPoint.RUN_PIPELINE,
                    "arguments": {"uid": uid, "proj_id": proj_id, "pipeline_id": pipeline_id, "inputs": inputs,
                                "params": params}})
                return LocalApi.MessageProtocol.read_from_socket(server)

        def run_module(self, uid, proj_id, app_id, inputs, params):
            with self.connect() as server:
                LocalApi.MessageProtocol
        def run_module(self, uid, proj_id, app_id, inputs, params):
            with self.connect() as server:
                LocalApi.MessageProtocol.write_to_socket(server,
                    {"entry_point": LocalApi.EntryPoint.RUN_MODULE,
                    "arguments": {"uid": uid, "proj_id": proj_id, "app_id": app_id, "inputs": inputs,
                    "params": params}})
                return LocalApi.MessageProtocol.read_from_socket(server)

        def task_info(self, uid, tid, type):
            with self.connect() as server:
                LocalApi.MessageProtocol.write_to_socket(server,
                    {"entry_point": LocalApi.EntryPoint.TASK_INFO, "arguments": {"uid": uid, "tid": tid, "type": type}})
                return LocalApi.MessageProtocol.read_from_socket(server)

        def task_details(self, uid, tid, type):
            with self.connect() as server:
                LocalApi.MessageProtocol.write_to_socket(server,
                    {"entry_point": LocalApi.EntryPoint.TASK_DETAILS, "arguments": {"uid": uid, "tid": tid, "type": type}})
                return LocalApi.MessageProtocol.read_from_socket(server)

    @staticmethod
    def port_open():
        import os
        return os.system(f"lsof -i:{LocalApi.PORT}") != 0
