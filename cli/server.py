import concurrent.futures
import ipaddress
import os
import re
import socket
import sys
from typing import List, Optional

import click
import dotenv

from cli.utils.monitoring import get_server_status, check_host
from cli.utils.server import Server
from cli.utils.ssh import SSHUtil

dotenv.load_dotenv()


@click.group()
def server():
    """
    Manage servers
    """
    pass


@server.command()
@click.argument('hostname', required=False)
def register(hostname: Optional[str] = None):
    """
    Register a new server.
    """
    if not hostname:
        hostname = click.prompt("Hostname")
    username = click.prompt("Username")

    server = Server(hostname, username)
    server.save()
    click.echo(f"Server {hostname} registered successfully.")


@server.command()
def delete():
    """
    Delete a server.
    """
    servers = Server.load_all()
    if not servers:
        click.echo("No servers registered.")
        return

    server_choices = {server.hostname: server for server in servers}
    server_name = click.prompt(
        "Select a server to delete",
        type=click.Choice(server_choices),
        show_choices=True
    )

    server = server_choices[server_name]
    server.delete()
    click.echo(f"Server {server_name} deleted successfully.")


@server.command()
def modify():
    """
    Modify an existing server.
    """
    servers = Server.load_all()
    if not servers:
        click.echo("No servers registered.")
        return

    server_choices = {server.hostname: server for server in servers}
    server_name = click.prompt(
        "Select a server to modify",
        type=click.Choice(server_choices),
        show_choices=True
    )

    server = server_choices[server_name]
    new_username = click.prompt("New username", default=server.username)
    server.username = new_username
    click.echo(f"Server {server_name} modified successfully.")


@server.command()
@click.argument('host')
@click.option(
    '-s',
    '--server-url',
    '--url',
    required=True,
    default=os.environ.get("K3S_SERVER_URL"),
    help='Target K3S server URL (e.g. https://my-k3s-server:6443), required, can also be set via K3S_SERVER_URL env var'
)
@click.option(
    '-t',
    '--token',
    required=True,
    default=os.environ.get("K3S_TOKEN"),
    help='K3s cluster token (e.g. K1029384756...), required, can also be set via K3S_TOKEN env var'
)
def install_k3s_agent(host: str, server_url: str, token: str):
    """
    SSH into a server and install K3s agent node.

    HOST: The hostname or IP address of the target server
    """
    # get the server we are installing on
    servers = Server.load_all()
    server = next((s for s in servers if s.hostname == host), None)

    try:
        with SSHUtil(server) as ssh:
            # Construct the K3s installation command
            install_cmd = f'curl -sfL https://get.k3s.io | K3S_URL={server_url} K3S_TOKEN={token} sh -'

            # Execute the command
            click.echo(f"Installing K3s agent on {host}...")
            ssh.exec_command(install_cmd)

            click.echo("K3s agent installation completed successfully!")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


def get_network_cidr() -> str:
    """Get the local network CIDR by checking the machine's IP address"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't actually connect but gets local IP
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        # Assume /24 network for typical local networks
        return f"{local_ip.rsplit('.', 1)[0]}.0/24"
    except Exception:
        return "192.168.1.0/24"  # Fallback to common local network
    finally:
        s.close()


@server.command()
@click.option('--pattern', '-p', default=".*",
              help='Regex pattern to match hostnames (default: match all)')
@click.option('--network', '-n',
              help='Network CIDR to scan (default: auto-detect)')
@click.option('--timeout', '-t', default=1.0,
              help='Timeout in seconds for each host check')
@click.option('--workers', '-w', default=50,
              help='Number of concurrent workers')
@click.option('--ssh-only/--all-hosts', default=True,
              help='Show only hosts with SSH port open (default: True)')
def scan(pattern: str, network: Optional[str], timeout: float,
                 workers: int, ssh_only: bool):
    """Scan local network for hosts matching the given hostname pattern"""
    try:
        # Compile regex pattern
        host_pattern = re.compile(pattern, re.IGNORECASE)
    except re.error as e:
        click.echo(f"Error in regex pattern: {e}", err=True)
        return

    # Get network to scan
    if not network:
        network = get_network_cidr()

    click.echo(f"Scanning network: {network}")
    click.echo(f"Hostname pattern: {pattern}")

    # Generate list of IPs to scan
    try:
        ips = [str(ip) for ip in ipaddress.IPv4Network(network)]
    except ValueError as e:
        click.echo(f"Invalid network format: {e}", err=True)
        return

    # Scan hosts concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_ip = {
            executor.submit(check_host, ip, timeout): ip
            for ip in ips
        }

        hosts = []
        with click.progressbar(length=len(ips),
                               label='Scanning hosts') as bar:
            for future in concurrent.futures.as_completed(future_to_ip):
                host_info = future.result()
                if (not ssh_only or host_info.is_up) and \
                        (host_info.hostname is None or
                         host_pattern.search(host_info.hostname)):
                    hosts.append(host_info)
                bar.update(1)

    # Display results
    click.echo("\nResults:")
    if not hosts:
        click.echo("No matching hosts found.")
        return

    for host in sorted(hosts, key=lambda h: ipaddress.IPv4Address(h.ip)):
        status = "UP" if host.is_up else "DOWN"
        hostname = host.hostname or "No hostname"
        click.echo(f"{host.ip:15} {status:4} {hostname}")


@server.command()
def list():
    """
    List all registered servers.
    """
    servers = Server.load_all()
    if not servers:
        click.echo("No servers registered.")
        return

    click.echo("Registered servers:")
    for server in servers:
        status = get_server_status(server)
        click.echo()
        click.echo(status)
        click.echo()


@server.command()
def cleanup():
    """
    Clean up all registered servers.
    """
    servers = Server.load_all()
    if not servers:
        click.echo("No servers registered.")
        return

    for server in servers:
        # try to uninstall k3s
        try:
            with SSHUtil(server) as ssh:
                click.echo(f"Uninstalling K3s from {server.hostname}...")
                try:
                    ssh.run_command("/usr/local/bin/k3s-uninstall.sh")
                except Exception:
                    ssh.run_command("/usr/local/bin/k3s-agent-uninstall.sh")
                click.echo("K3s uninstalled successfully!")
        except Exception as e:
            click.echo(f"Error: {str(e)}", err=True)


@server.command()
def setup():
    """
    Setup all registered servers.
    """
    servers = Server.load_all()
    if not servers:
        click.echo("No servers registered.")
        return

    # find the server that is a k3s server
    server = next((s for s in servers if s.kind == 'k3s_server'), None)
    if not server:
        click.echo("No K3s server registered.")
        return

    # get the server status
    status = get_server_status(server)

    if not status.host_info.is_up:
        click.echo("Primary node is not reachable. Please check the connection.")
        return

    with SSHUtil(server) as ssh:
        if not (status.k3s_server_status is not None and status.k3s_server_status.active):
            # try to install k3s
            try:

                click.echo(f"Installing K3s server on {server.hostname}...")
                install_cmd = 'curl -sfL https://get.k3s.io | sh -'
                ssh.run_command(install_cmd)

            except Exception as e:
                click.echo(f"Error: {str(e)}", err=True)
        else:
            click.echo(f"K3s server is already installed on {server.hostname}. Skipping...")
        stdout, _ = ssh.run_command("sudo cat /var/lib/rancher/k3s/server/node-token")
        token = stdout.strip()

    # install k3s agents
    for agent in (s for s in servers if s.kind == 'k3s_agent'):
        status = get_server_status(agent)
        if not status.host_info.is_up:
            click.echo(f"Node {agent.hostname} is not reachable. Skipping...")
            continue
        with SSHUtil(agent) as ssh:
            if status.k3s_agent_status is not None and status.k3s_agent_status.active:
                click.echo(f"K3s agent is already installed on {agent.hostname}. Checking configuration...")
                stdout, _ = ssh.run_command("sudo cat /etc/rancher/k3s/k3s.yaml")
                print(stdout)
            try:

                click.echo(f"Installing K3s agent on {agent.hostname}...")
                install_cmd = f'curl -sfL https://get.k3s.io | K3S_URL=https://{server.hostname} K3S_TOKEN={token} sh -'
                ssh.run_command_stream(install_cmd)
            except Exception as e:
                click.echo(f"Error: {str(e)}", err=True)

    click.echo("K3s setup completed successfully!")