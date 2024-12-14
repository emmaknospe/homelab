import socket
from typing import Optional

from cli.utils.ssh import SSHUtil
from cli.utils.server import Server, ServerStatus, K3SServerStatus, K3SAgentStatus, HostInfo


def get_systemctl_service_status(ssh: SSHUtil, service_name: str) -> tuple[Optional[bool], Optional[bool], Optional[bool]]:
    stdout, stderr = ssh.run_command(f'systemctl list-units --all {service_name}.service')
    if service_name not in stdout:
        return False, None, None
    active = None
    try:
        stdout, stderr = ssh.run_command(f'systemctl status {service_name}')
    except Exception:
        return False, None, None
    if 'Active: active (running)' in stdout:
        active = True
    elif 'Active: inactive (dead)' in stdout:
        active = False

    enabled = None
    try:
        stdout, stderr = ssh.run_command(f'systemctl is-enabled {service_name}')
    except Exception:
        return False, None, None
    if 'enabled' in stdout:
        enabled = True
    elif 'disabled' in stdout:
        enabled = False
    return True, active, enabled


def get_server_status(server: Server) -> ServerStatus:
    host_info = check_host(server.hostname)
    try:
        with SSHUtil(server) as ssh:
            k3s_server_status = None
            k3s_server_present, k3s_server_active, k3s_server_enabled = get_systemctl_service_status(ssh, 'k3s')
            if k3s_server_present:
                version = ssh.run_command('k3s --version')[0].strip()
                k3s_server_status = K3SServerStatus(active=k3s_server_active, enabled=k3s_server_enabled, version=version)
            k3s_agent_status = None
            k3s_agent_present, k3s_agent_active, k3s_agent_enabled = get_systemctl_service_status(ssh, 'k3s-agent')
            if k3s_agent_present:
                version = ssh.run_command('k3s --version')[0].strip()
                k3s_agent_status = K3SAgentStatus(active=k3s_agent_active, enabled=k3s_agent_enabled, version=version)
            return ServerStatus(server=server, host_info=host_info, k3s_server_status=k3s_server_status, k3s_agent_status=k3s_agent_status)
    except socket.gaierror:
        return ServerStatus(server=server, host_info=host_info, k3s_server_status=None, k3s_agent_status=None)


def check_host(ip: str, timeout: float = 1.0) -> HostInfo:
    """Check if a host is up and resolve its hostname"""
    try:
        # Try to get hostname
        hostname = socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror):
        hostname = None

    # Check if host is up using TCP connection to port 22 (SSH)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, 22))
        is_up = (result == 0)
    except socket.error:
        is_up = False
    finally:
        sock.close()

    return HostInfo(ip=ip, hostname=hostname, is_up=is_up)
