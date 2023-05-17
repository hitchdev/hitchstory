from hitchstory import Failure
import time
import socket


def port_open(port_number: int, timeout=2.5):
    try:
        with socket.create_connection(("localhost", port_number), timeout=timeout):
            return True
    except OSError:
        return False


def wait_for_port(port_number: int, timeout=10.0):
    start_time = time.perf_counter()

    while True:
        if not port_open(port_number):
            time.sleep(0.05)
            if time.perf_counter() - start_time >= timeout:
                raise Failure(
                    f"Port {port_number} on localhost not responding after {timeout} seconds."
                )
        else:
            break
