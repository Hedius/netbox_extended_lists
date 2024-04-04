from extras.plugins import PluginConfig


class NetBoxExtendedLists(PluginConfig):
    name = 'netbox_extended_lists'
    verbose_name = ' NetBox Extended Lists'
    description = 'Shows all prefixes and their IP addresses for a filtered view.'
    version = '0.1'
    base_url = 'extended-lists'


config = NetBoxExtendedLists
