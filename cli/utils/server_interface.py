import sys
from queue import Queue, Empty
from threading import Thread
import time
import paramiko
import logging
from cli.utils.server import Server


logging.getLogger("paramiko").setLevel(logging.WARNING)


def stream_output(chan, queue):
    """Stream output from channel to queue."""
    while True:
        if chan.exit_status_ready():
            break
        try:
            data = chan.recv(1024)
            if not data:
                break
            queue.put(('stdout', data))
        except Exception as e:
            queue.put(('error', str(e)))
            break


def stream_error(chan, queue):
    """Stream stderr from channel to queue."""
    while True:
        if chan.exit_status_ready():
            break
        try:
            data = chan.recv_stderr(1024)
            if not data:
                break
            queue.put(('stderr', data))
        except Exception as e:
            queue.put(('error', str(e)))
            break


class ServerInterface:
    def __init__(self, server: Server):
        self.server = server
        self.ssh = None

    def __enter__(self):
        self._init_ssh_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ssh.close()

    def _init_ssh_session(self, timeout=5):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        start_time = time.time()
        while True:
            try:
                self.ssh.connect(self.server.hostname, username=self.server.username, port=22)
                break
            except paramiko.ssh_exception.NoValidConnectionsError:
                time.sleep(1)
            except paramiko.ssh_exception.AuthenticationException as e:
                raise Exception(f"Authentication failed for {self.server.username}@{self.server.hostname}") from e
            except paramiko.ssh_exception.SSHException:
                time.sleep(1)
            if time.time() - start_time > timeout:
                raise Exception(f"Could not connect to {self.server.hostname}")
    def run_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        if exit_status != 0:
            raise Exception(f"Command '{command}' failed with status {exit_status} ({stderr.read().decode('utf-8')})")
        return (
            stdout.read().decode('utf-8').strip(),
            stderr.read().decode('utf-8').strip(),
        )

    def run_command_stream(self, command):
        channel = self.ssh.get_transport().open_session()
        channel.get_pty()
        channel.exec_command(command)

        # Create output queue and threads
        output_queue = Queue()
        stdout_thread = Thread(target=stream_output, args=(channel, output_queue))
        stderr_thread = Thread(target=stream_error, args=(channel, output_queue))

        # Start threads
        stdout_thread.start()
        stderr_thread.start()

        # Process output as it comes in
        while not channel.exit_status_ready() or not output_queue.empty():
            try:
                source, data = output_queue.get(timeout=0.1)
                if source == 'stdout':
                    sys.stdout.buffer.write(data)
                    sys.stdout.buffer.flush()
                elif source == 'stderr':
                    sys.stderr.buffer.write(data)
                    sys.stderr.buffer.flush()
                elif source == 'error':
                    print(f"Error: {data}", file=sys.stderr)
            except Empty:
                continue
            except Exception as e:
                print(f"Error processing output: {e}", file=sys.stderr)
                break

        # Wait for threads to complete
        stdout_thread.join()
        stderr_thread.join()

        # Get exit status
        exit_status = channel.recv_exit_status()
        return exit_status

    def upload_file(self, local_path, remote_path):
        sftp = self.ssh.open_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()

    def download_file(self, remote_path, local_path):
        sftp = self.ssh.open_sftp()
        sftp.get(remote_path, local_path)
        sftp.close()

    def reboot(self):
        self.run_command('sudo reboot')
        self.ssh.close()
        self.ssh = None
        self._init_ssh_session(timeout=60)
