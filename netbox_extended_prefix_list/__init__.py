from extras.plugins import PluginConfig


class NetBoxExtendedPrefixList(PluginConfig):
    name = 'netbox_extended_prefix_list'
    verbose_name = ' NetBox Extended Prefix List'
    description = 'Shows all prefixes and their IP addresses for a filtered view.'
    version = '0.1'
    base_url = 'prefix-list'


config = NetBoxExtendedPrefixList
