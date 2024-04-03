from django.utils.translation import gettext_lazy as _
from django.core.paginator import PageNotAnInteger, EmptyPage
from django.shortcuts import render
import django_tables2 as tables

from ipam import filtersets
from ipam.filtersets import PrefixFilterSet
from ipam.forms import PrefixFilterForm
from ipam.models import Prefix, IPAddress
from ipam.tables import ip as ip_table
from ipam.utils import add_available_ipaddresses
from netbox.tables import NetBoxTable, columns
from netbox.views import generic
from tenancy.tables import TenancyColumnsMixin
from utilities.paginator import get_paginate_count, EnhancedPaginator


class IPAddressTable(TenancyColumnsMixin, NetBoxTable):
    address = tables.TemplateColumn(
        template_code=ip_table.IPADDRESS_LINK,
        verbose_name=_('IP Address')
    )
    vrf = tables.TemplateColumn(
        template_code=ip_table.VRF_LINK,
        verbose_name=_('VRF')
    )
    status = columns.ChoiceFieldColumn(
        verbose_name=_('Status'),
        default=ip_table.AVAILABLE_LABEL
    )
    role = columns.ChoiceFieldColumn(
        verbose_name=_('Role'),
    )
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_('Interface')
    )
    assigned_device = tables.Column(
        linkify=True,
        orderable=False,
        accessor='assigned_object__device',
        verbose_name=_('Device / VM')
    )
    assigned_object_parent = tables.Column(
        accessor='assigned_object__parent_object',
        linkify=True,
        orderable=False,
        verbose_name=_('Parent')
    )
    nat_inside = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name=_('NAT (Inside)')
    )
    nat_outside = tables.ManyToManyColumn(
        linkify_item=True,
        orderable=False,
        verbose_name=_('NAT (Outside)')
    )
    assigned = columns.BooleanColumn(
        accessor='assigned_object_id',
        linkify=lambda record: record.assigned_object.get_absolute_url(),
        verbose_name=_('Assigned')
    )
    comments = columns.MarkdownColumn(
        verbose_name=_('Comments'),
    )
    tags = columns.TagColumn(
        url_name='ipam:ipaddress_list'
    )
    actions = columns.ActionsColumn(
        extra_buttons=ip_table.IPADDRESS_COPY_BUTTON
    )

    class Meta(NetBoxTable.Meta):
        model = IPAddress
        fields = (
            'pk', 'id', 'address', 'vrf', 'status', 'role', 'tenant', 'tenant_group', 'nat_inside', 'nat_outside',
            'assigned', 'assigned_device', 'assigned_object', 'dns_name', 'description', 'comments', 'tags', 'created', 'last_updated',
        )
        default_columns = (
            'pk', 'address', 'vrf', 'status', 'role', 'tenant', 'assigned', 'assigned_device', 'assigned_object', 'description',
        )
        row_attrs = {
            'class': lambda record: 'success' if not isinstance(record, IPAddress) else '',
        }


class ExtendedPrefixListView(generic.ObjectListView):
    """
    Display a set of rack elevations side-by-side.
    """
    queryset = Prefix.objects.prefetch_related(
        'site', 'vrf__tenant', 'tenant', 'vlan', 'role', 'tags'
    )
    filterset = PrefixFilterSet
    filterset_form = PrefixFilterForm

    def get(self, request):

        prefixes = filtersets.PrefixFilterSet(request.GET, self.queryset).qs
        total_count = prefixes.count()

        # Ordering
        ORDERING_CHOICES = {
            # 'name': 'Name (A-Z)',
            # '-name': 'Name (Z-A)',
            # 'facility_id': 'Facility ID (A-Z)',
            # '-facility_id': 'Facility ID (Z-A)',
        }
        # sort = request.GET.get('sort', 'name')
        # if sort not in ORDERING_CHOICES:
        #     sort = 'name'
        # sort_field = sort.replace("name", "_name")  # Use natural ordering
        # racks = racks.order_by(sort_field)

        # Pagination
        per_page = get_paginate_count(request)
        page_number = request.GET.get('page', 1)
        paginator = EnhancedPaginator(prefixes, per_page)
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        ip_tables = []
        for prefix in page:
            ips = prefix.get_child_ips().restrict(request.user, 'view').prefetch_related('vrf', 'tenant', 'tenant__group', 'assigned_object')
            ips = add_available_ipaddresses(prefix.prefix, ips, prefix.is_pool)
            ip_tables.append({
                'prefix': prefix,
                'table': IPAddressTable(ips)
            })

        # Determine rack face
        return render(request, 'netbox_extended_prefix_list/prefix_list.html', {
            'paginator': paginator,
            'page': page,
            'total_count': total_count,
            'sort_choices': ORDERING_CHOICES,
            'filter_form': PrefixFilterForm(request.GET),
            'model': self.queryset.model,
            'tables': ip_tables
        })