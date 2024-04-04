from extras.plugins import PluginMenuItem

menu_items = (
    PluginMenuItem(
        link='plugins:netbox_extended_lists:prefix_list',
        link_text='Prefix List',
        permissions=('ipam.view_prefix', 'ipam.view_ipaddress')
    ),
)
