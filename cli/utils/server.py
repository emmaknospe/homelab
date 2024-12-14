import dataclasses
import enum
import json
from typing import Optional, Literal
import textwrap
from cli.constants import SERVERS_FILE


@dataclasses.dataclass
class HostInfo:
    ip: str
    hostname: Optional[str]
    is_up: bool


@dataclasses.dataclass
class Server:
    hostname: str
    username: str
    kind: Literal['k3s_agent'] | Literal['k3s_server'] = 'k3s_agent'

    def save(self):
        servers = Server._load_all_raw()
        servers[self.hostname] = dataclasses.asdict(self)
        SERVERS_FILE.write_text(json.dumps(servers, indent=2))

    def delete(self):
        servers = Server._load_all_raw()
        del servers[self.hostname]
        SERVERS_FILE.write_text(json.dumps(servers, indent=2))

    @staticmethod
    def _load_all_raw():
        if not SERVERS_FILE.exists():
            return {}
        return json.loads(SERVERS_FILE.read_text())

    @staticmethod
    def load_all():
        return [Server(**server) for server in Server._load_all_raw().values()]


@dataclasses.dataclass
class K3SServerStatus:
    active: bool
    enabled: bool
    version: str


@dataclasses.dataclass
class K3SAgentStatus:
    active: bool
    enabled: bool
    version: str


@dataclasses.dataclass
class ServerStatus:
    server: Server
    host_info: HostInfo
    k3s_server_status: K3SServerStatus
    k3s_agent_status: K3SAgentStatus

    def __str__(self):
        header = f"{self.server.hostname} ({self.server.username})"
        lines = []
        if self.host_info:
            lines.append(f"Up: {self.host_info.is_up}")
        if self.k3s_server_status:
            lines.append("K3S Server:")
            sublines = [
                f"Active: {self.k3s_server_status.active}",
                f"Enabled: {self.k3s_server_status.enabled}",
                f"Version: {self.k3s_server_status.version}",
            ]
            lines.extend(textwrap.indent(subline, "  ") for subline in sublines)
        if self.k3s_agent_status:
            lines.append("K3S Agent:")
            sublines = [
                f"Active: {self.k3s_agent_status.active}",
                f"Enabled: {self.k3s_agent_status.enabled}",
                f"Version: {self.k3s_agent_status.version}",
            ]
            lines.extend(textwrap.indent(subline, "  ") for subline in sublines)
        return header + "\n" + textwrap.indent("\n".join(lines), "  ")
