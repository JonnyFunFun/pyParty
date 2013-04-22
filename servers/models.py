from django.db import models
from django.contrib.auth.models import User
from servers.query.source import SourceQuery
from servers.query.minecraft import MinecraftQuery
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM, socket


SERVER_TYPES = (
    ('HLDS', 'HLDS/Source'),
    ('MINE', 'Minecraft'),
    ('OTHR', 'Other')
)


class Server(models.Model):
    name = models.CharField(max_length=128)
    desc = models.TextField(blank=True, default="")
    operator = models.ForeignKey(User)
    address = models.IPAddressField(null=True)
    port = models.IntegerField(null=True)
    game = models.CharField(max_length=128)
    server_type = models.CharField(max_length=4, choices=SERVER_TYPES, null=False, default='OTHR')
    mod_approved = models.BooleanField(default=False, verbose_name="Approval Status")

    def info(self):
        if self.server_type == 'HLDS':
            # query HLDS server
            try:
                q = SourceQuery(self.address, self.port or 27015)
                return q.getInfo()
            except:
                raise
                return None
        elif self.server_type == 'MINE':
            # query minecraft
            try:
                q = MinecraftQuery(self.address, self.port or 25565)
                return q.get_rules()
            except:
                return None
        # default stuff
        return None

    @property
    def host_alive(self):
        return (socket(AF_INET, SOCK_STREAM).connect_ex((self.address, self.port)) == 0) or (socket(AF_INET, SOCK_DGRAM).connect_ex((self.address, self.port)) == 0)
