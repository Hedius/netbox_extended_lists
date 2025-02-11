from netbox.plugins import PluginConfig


class NetBoxExtendedLists(PluginConfig):
    name = 'netbox_extended_lists'
    verbose_name = ' NetBox Extended Lists'
    description = 'Adds additional views to netbox with extended information'
    version = '1.1.2'
    base_url = 'extended-lists'
    author = 'Hedius & pheeef'
    author_email = 'git@hedius.eu'
    min_version = 'v4.2.3'


config = NetBoxExtendedLists
