from pyvcloud.vcd.client import Client, BasicLoginCredentials, QueryResultFormat
from pyvcloud.vcd.client import NSMAP
from pyvcloud.vcd.org import Org
from pyvcloud.vcd.vdc import VDC
from pyvcloud.vcd.vm import VM

# VMware Cloud Director details
host = 'your_cloud_director_host'
org = 'your_organization_name'
user = 'your_username'
password = 'your_password'
vdc_name = 'your_vdc_name'
catalog_name = 'your_catalog_name'
template_name = 'your_template_name'
vm_name = 'your_new_vm_name'

# Connect to VCD
client = Client(host, api_version='33.0', verify_ssl_certs=False)
client.set_credentials(BasicLoginCredentials(user, org, password))

try:
    # Get the organization and VDC
    org_resource = Org(client, resource=client.get_org())
    vdc_resource = VDC(client, resource=org_resource.get_vdc(vdc_name))

    # Get the catalog and template
    catalog_item = org_resource.get_catalog_item(catalog_name, template_name)
    vapp_template = vdc_resource.get_vapp_template(catalog_item.Entity.get('href'))

    # Instantiate the VM from template
    print("Creating VM...")
    instantiate_params = {
        'name': vm_name,
        'description': 'New VM from template',
        'power_on': False,  # Do not power on immediately after creation
        'deploy': True,
        'memory': 2048,
        'cpu': 2,
        'network': 'your_network_name',
        'ip_allocation_mode': 'DHCP'  # Change as required
    }
    vapp = vdc_resource.instantiate_vapp(vm_name, vapp_template, **instantiate_params)
    print(f"VM '{vm_name}' created successfully.")

    # Power on the VM
    vm = VM(client, href=vapp.get_vm(vm_name).get('href'))
    task = vm.power_on()
    client.get_task_monitor().wait_for_status(task)
    print(f"VM '{vm_name}' powered on successfully.")

finally:
    # Logout from client
    client.logout()
