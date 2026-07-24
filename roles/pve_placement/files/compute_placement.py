import json
import subprocess
import sys

source_node = sys.argv[1]
target_nodes = sys.argv[2].split(',')

def get_node_status(node):
    raw = subprocess.check_output(['pvesh', 'get', f'/nodes/{node}/status', '--output-format', 'json'])
    return json.loads(raw)

def get_node_vms(node):
    raw = subprocess.check_output(['pvesh', 'get', f'/nodes/{node}/qemu', '--output-format', 'json'])
    return json.loads(raw)

def get_vms_to_evacuate(node):
    vms = get_node_vms(node)
    return [vm for vm in vms if vm.get('status') == 'running']

vms_to_move = get_vms_to_evacuate(source_node)

# Track free memory per target node, updated as we assign VMs
node_free_mem = {}
node_vm_count = {}
for node in target_nodes:
    status = get_node_status(node)
    node_free_mem[node] = status['memory']['free']
    node_vm_count[node] = len(get_node_vms(node))

placements = []
for vm in vms_to_move:
    vm_mem = vm.get('maxmem', 0)
    # Pick the target node with the most free memory (tie-break: fewest VMs)
    best_node = max(target_nodes, key=lambda n: (node_free_mem[n], -node_vm_count[n]))
    placements.append({
        'vmid': vm['vmid'],
        'name': vm.get('name', f"vm-{vm['vmid']}"),
        'mem_required': vm_mem,
        'target_node': best_node
    })
    node_free_mem[best_node] -= vm_mem
    node_vm_count[best_node] += 1

print(json.dumps(placements, indent=2))
