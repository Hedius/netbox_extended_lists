from extras.plugins import PluginConfig

version = '1.0.0'


class NetBoxExtendedLists(PluginConfig):
    name = 'netbox_extended_lists'
    verbose_name = ' NetBox Extended Lists'
    description = 'Adds additional views to netbox with extended information'
    version = version
    base_url = 'extended-lists'
    author = 'Hedius & pheeef'
    author_email = 'git@hedius.eu'


config = NetBoxExtendedLists
