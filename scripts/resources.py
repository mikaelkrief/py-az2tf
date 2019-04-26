#from azure.common.client_factory import get_client_from_cli_profile
#from azure.mgmt.compute import ComputeManagementClient
#from azure.mgmt.resource import ResourceManagementClient
import subprocess
import requests
import adal
import os
import json
import sys
import glob
import argparse


parser = argparse.ArgumentParser(description='terraform sub rg')
parser.add_argument('-s', help='Subscription Id')
parser.add_argument('-g', help='Resource Group')
parser.add_argument('-r', help='Filter azurerm resource')
parser.add_argument('-d', help='Debug')
args = parser.parse_args()
csub=args.s
crg=args.g
crf=args.r
deb=args.d

cde=False

if csub is not None:
    print("sub=" + csub) 
    # validate sub
if crg is not None:
    print("resource group=" + crg)
    # validate rg
if crf is not None:
    print("resource filter=" + crf)
    # validate rg
if deb is not None:
    cde=True

if sys.version_info[0] > 2:
    #raise Exception("Must be using Python 2")
    print("Python version ", sys.version_info[0], " version 2 required, Exiting")
    exit()

def printf(format, *values):
    print(format % values )

#with open(filename, 'w') as f:
    #print >> f, 'Filename:'


#tenant = os.environ['TENANT']
#authority_url = 'https://login.microsoftonline.com/' + tenant
#client_id = os.environ['CLIENTID']
#client_secret = os.environ['CLIENTSECRET']
#resource = 'https://management.azure.com/'
#context = adal.AuthenticationContext(authority_url)
#token = context.acquire_token_with_client_credentials(resource, client_id, client_secret)
#headers = {'Authorization': 'Bearer ' + token['accessToken'], 'Content-Type': 'application/json'}
#params = {'api-version': '2016-06-01'}
#url = 'https://management.azure.com/' + 'subscriptions'
#r = requests.get(url, headers=headers, params=params)
#print(json.dumps(r.json(), indent=4, separators=(',', ': ')))
print "Access Token"
p = subprocess.Popen('az account get-access-token -o json', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
c=0
for line in p.stdout.readlines():
    if "accessToken" in line:
        tk=line.split(":")[1].strip(' ",')
        tk2=tk.replace(",", "")
        bt2=tk2.replace('"', '')
    if "subscription" in line:
        tk=line.split(":")[1].strip(' ",')
        tk2=tk.replace(",", "")
        sub2=tk2.replace('"', '')
retval = p.wait()
if csub is not None:
    sub=csub
else:
    sub=sub2.rstrip('\n')

bt=bt2.rstrip('\n')
print "Subscription:",sub
headers = {'Authorization': 'Bearer ' + bt, 'Content-Type': 'application/json'}
print "REST Resources ",

fresfilename="data.json"
fres=open(fresfilename, 'w')
url="https://management.azure.com/subscriptions/" + sub + "/resources"
params = {'api-version': '2018-11-01'}
try: 
    r = requests.get(url, headers=headers, params=params)
    res= r.json()["value"]
except KeyError:
    print "Error getting resources"
    exit()
fres.write(json.dumps(res, indent=4, separators=(',', ': ')))
fres.close()


rfilename="resources2.txt"
fr=open(rfilename, 'w')
nprfilename="noprovider2.txt"
np=open(nprfilename, 'w')


count=len(res)
print count
for j in range(0, count):
    t1=res[j]
    name=res[j]['name']
    id=res[j]['id']
    rg1=id.split("/")[4]
    try:
        isext=id.split("/")[9]
    except IndexError:
        isext=""

    loc=res[j]['location']
    rtype=res[j]['type']
    rg=rg1.replace(".","-")
    #print rtype

    if rtype == "Microsoft.Compute/availabilitySets":
        prov="azurerm_availability_set"
        fr.write(rg + ":" + prov + "\n")
    elif rtype == "Microsoft.Network/networkSecurityGroups":
        prov="azurerm_network_security_group"
        fr.write(rg + ":" + prov + "\n")

    elif rtype == "Microsoft.Storage/storageAccounts": 
        prov="azurerm_storage_account"
        fr.write(rg + ":" + prov + "\n")
        prov="azurerm_storage_share"
        fr.write(rg + ":" + prov + "\n")
        prov="azurerm_storage_container"
        fr.write(rg + ":" + prov + "\n")

    elif rtype == "Microsoft.Network/networkSecurityGroups":
        prov="azurerm_network_security_group"
        fr.write(rg + ":" + prov + "\n")

    elif rtype == "Microsoft.Compute/virtualMachines": 
        #echo $isext
        if isext != "extensions":
            prov="azurerm_virtual_machine"
            fr.write(rg + ":" + prov + "\n")
                
    elif rtype == "Microsoft.Network/networkInterfaces": 
        prov="azurerm_network_interface"
        fr.write(rg + ":" + prov + "\n")
    
    elif rtype == "Microsoft.Compute/disks":
        prov="azurerm_managed_disk"
        fr.write(rg + ":" + prov + "\n")
        
    elif rtype == "Microsoft.Automation/automationAccounts": 
        prov="azurerm_automation_account"
        fr.write(rg + ":" + prov + "\n")
          
    elif rtype == "Microsoft.Network/virtualNetworks":
        prov="azurerm_virtual_network"
        fr.write(rg + ":" + prov + "\n")
        prov="azurerm_subnet"
        fr.write(rg + ":" + prov + "\n")
        prov="azurerm_virtual_network_peering"
        fr.write(rg + ":" + prov + "\n")

    elif rtype == "Microsoft.Network/publicIPAddresses":
        prov="azurerm_public_ip"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.Network/loadBalancers":
        prov="azurerm_lb"
        fr.write(rg + ":" + prov + "\n")
        prov="azurerm_lb_nat_rule"
        fr.write(rg + ":" + prov + "\n")
        prov="azurerm_lb_nat_pool"
        fr.write(rg + ":" + prov + "\n")
        prov="azurerm_lb_backend_address_pool"
        fr.write(rg + ":" + prov + "\n")
        prov="azurerm_lb_probe"
        fr.write(rg + ":" + prov + "\n")
        prov="azurerm_lb_rule"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.Network/virtualNetworkGateways":
        prov="azurerm_virtual_network_gateway"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.Network/connections":
        prov="azurerm_virtual_network_gateway_connection"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.Network/routeTables": 
        prov="azurerm_route_table"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.OperationalInsights/workspaces":
        prov="azurerm_log_analytics_workspace"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype ==  "Microsoft.OperationsManagement/solutions":
        prov="azurerm_log_analytics_solution"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.KeyVault/vaults":
        prov="azurerm_key_vault"
        fr.write(rg + ":" + prov + "\n")
        prov="azurerm_key_vault_secret"
        fr.write(rg + ":" + prov + "\n")

    elif rtype == "Microsoft.RecoveryServices/vaults":
        prov="azurerm_recovery_services_vault"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.ContainerRegistry/registries":
        prov="azurerm_container_registry"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.ContainerService/managedClusters":
        prov="azurerm_kubernetes_cluster"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.Network/localNetworkGateways":
        prov="azurerm_local_network_gateway"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.Network/expressRouteCircuits":
        prov="azurerm_express_route_circuit"
        fr.write(rg + ":" + prov + "\n")
        prov="azurerm_express_route_circuit_authorization"
        fr.write(rg + ":" + prov + "\n")
        prov="azurerm_express_route_circuit_peering"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.Compute/images": 
        prov="azurerm_image"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.Network/networkWatchers": 
        prov="azurerm_network_watcher"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.Network/applicationSecurityGroups":
        prov="azurerm_application_security_group"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.ContainerInstance/containerGroups":
        prov="azurerm_container_group"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.Network/applicationGateways": 
        prov="azurerm_application_gateway"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.DocumentDb/databaseAccounts":
        prov="azurerm_cosmosdb_account"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.ServiceBus/namespaces": 
        prov="azurerm_servicebus_namespace"
        fr.write(rg + ":" + prov + "\n")
        prov="azurerm_servicebus_queue"
        fr.write(rg + ":" + prov + "\n")
                  
    elif rtype == "Microsoft.Network/trafficmanagerprofiles":
        prov="azurerm_traffic_manager_profile"
        fr.write(rg + ":" + prov + "\n")
        prov="azurerm_traffic_manager_endpoint"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.Web/serverFarms": 
        prov="azurerm_app_service_plan"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.Web/sites": 
        prov="azurerm_app_service"
        fr.write(rg + ":" + prov + "\n")
        prov="azurerm_function_app"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.Compute/virtualMachineScaleSets":
        prov="azurerm_virtual_machine_scale_set"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.ManagedIdentity/userAssignedIdentities":
        prov="azurerm_user_assigned_identity"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.Compute/snapshots":
        prov="azurerm_snapshot"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.Databricks/workspaces":
        prov="azurerm_databricks_workspace"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.Sql/servers": 
        prov="azurerm_sql_server"
        fr.write(rg + ":" + prov + "\n")
        prov="azurerm_sql_database"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype == "Microsoft.Network/dnszones": 
        prov="azurerm_dns_zone"
        fr.write(rg + ":" + prov + "\n")
            
    elif rtype ==  "microsoft.insights/autoscalesettings":
        prov="azurerm_monitor_autoscale_setting"
        fr.write(rg + ":" + prov + "\n")
            
    else:
        np.write(rtype + "\n")

fr.close()
np.close()

print "Optimizing Resources ..."
# sort unique and filter for Resource Group
rfilename="resources.txt"
fr=open(rfilename, 'w')
with open('resources2.txt', 'r') as r:
    for line in sorted(set(r)):
        trg=line.split(":")[0]
        trt=line.split(":")[1]
        #print trt
        if crg is not None:   # Resource Group Filter
            if trg == crg :
                if crf is not None:   # Resource Filter
                    if crf in trt:
                        fr.write(line,)
                else:
                    fr.write(line,)
        else:
            if crf is not None:   # Resource Filter
                if crf in trt :
                    fr.write(line,)
            else:
                fr.write(line,)
r.close()
fr.close()


if crf is None:
    crf="azurerm"


# sort unique and fileter for Resource Group
rfilename="noprovider.txt"
fr=open(rfilename, 'w')
with open('noprovider2.txt', 'r') as r:
    for line in sorted(set(r)):
        fr.write(line,)

r.close()
fr.close()
if os.path.exists("tf-staterm.sh"):
    os.remove('tf-staterm.sh')
if os.path.exists("tf-stateimp.sh"):
    os.remove('tf-stateimp.sh')



#
# handle resource groups
#

tfp="azurerm_resource_group"
print tfp,
tfrmf="001-"+tfp+"-staterm.sh"
tfimf="001-"+tfp+"-stateimp.sh"
tfrm=open(tfrmf, 'a')
tfim=open(tfimf, 'a')
url="https://management.azure.com/subscriptions/" + sub + "/resourceGroups"
params = {'api-version': '2014-04-01'}
r = requests.get(url, headers=headers, params=params)
rgs= r.json()["value"]

#frgfilename=tfp+".json"
#frg=open(frgfilename, 'w')
#frg.write(json.dumps(rgs, indent=4, separators=(',', ': ')))
#frg.close()
if cde:
    print(json.dumps(rgs, indent=4, separators=(',', ': ')))

tffile=tfp+"*.tf"
#fileList = glob.glob(tffile) 
# Iterate over the list of filepaths & remove each file.
#for filePath in fileList:
#    try:
#        os.remove(filePath)
#    except:
#        print("Error while deleting file : ", filePath)

count=len(rgs)
print count
for j in range(0, count):
    
    name=rgs[j]["name"]
    rg=name
    loc=rgs[j]["location"]
    id=rgs[j]["id"]
    if crg is not None:
        if rg != crg:
            continue
    
    rname=name.replace(".","-")
    prefix=tfp+"."+rname
    
    rfilename=prefix+".tf"
    fr=open(rfilename, 'w')
    fr.write("")
    fr.write('resource "' + tfp + '" "' + rname + '" {\n')
    fr.write('\t name = "' + name + '"\n')
    fr.write('\t location = "'+ loc + '"\n')
 

# tags block
    try:
        mtags=rgs[j]["tags"]
    except:
        mtags="{}"
    tcount=len(mtags)-1
    if tcount > 1 :
        fr.write('tags { \n')
        print tcount
        for key in mtags.keys():
            tval=mtags[key]
            fr.write('\t "' + key + '"="' + tval + '"\n')
        #print(json.dumps(mtags, indent=4, separators=(',', ': ')))
        fr.write('}\n')
    
    fr.write('}\n') 
    fr.close()  # close .tf file

    tfrm.write('terraform state rm '+tfp+'.'+rname + '\n')
    tfim.write('echo "importing ' + str(j) + ' of ' + str(count-1) + '"' + '\n')
    tfcomm='terraform import '+tfp+'.'+rname+' '+id+'\n'
    tfim.write(tfcomm)

# end for
tfrm.close()
tfim.close()
#end resource group

# management locks


tfp="azurerm_management_lock"
azr=""

p = subprocess.Popen('az lock list -o json', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
output, errors = p.communicate()
azr=json.loads(output)

if cde:
    print(json.dumps(azr, indent=4, separators=(',', ': ')))

tfrmf="002-"+tfp+"-staterm.sh"
tfimf="002-"+tfp+"-stateimp.sh"
tfrm=open(tfrmf, 'a')
tfim=open(tfimf, 'a')
print tfp,
count=len(azr)
print count
for j in range(0, count):
    
    name=azr[j]["name"]
    #loc=azr[j]["location"]
    id=azr[j]["id"]
    rg=azr[j]["resourceGroup"]
    level=azr[j]["level"]
    notes=azr[j]["notes"]
    scope1=id.split("/Microsoft.Authorization")[0].rstrip("providers")
    scope=scope1.rstrip("/")


    if crg is not None:
        print "rgname=" + rg + " crg=" + crg
        if rg != crg:
            continue  # back to for
    

    rname=name.replace(".","-")
    prefix=tfp+"."+rg+'__'+rname
    #print prefix
    rfilename=prefix+".tf"
    fr=open(rfilename, 'w')
    fr.write("")
    fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
    fr.write('\t name = "' + name + '"\n')
    #fr.write('\t location = "'+ loc + '"\n')
    fr.write('\t lock_level = "'+ level + '"\n')   
    fr.write('\t notes = "'+ notes + '"\n') 
    fr.write('\t scope = "'+ scope + '"\n')
# tags block
    try:
        mtags=azr[j]["tags"]
    except:
        mtags="{}"
    tcount=len(mtags)-1
    if tcount > 1 :
        fr.write('tags { \n')
        print tcount
        for key in mtags.keys():
            tval=mtags[key]
            fr.write('\t "' + key + '"="' + tval + '"\n')
        #print(json.dumps(mtags, indent=4, separators=(',', ': ')))
        fr.write('}\n')
    
    fr.write('}\n') 
    fr.close()  # close .tf file

    tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')
    
    tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
    tfim.write('echo "importing ' + str(j) + ' of ' + str(count-1) + '"' + '\n')
    tfim.write(tfcomm)  

# end for
tfrm.close()
tfim.close()
#end management locks

# 015 user assigned identity
tfp="azurerm_user_assigned_identity"
azr=""

p = subprocess.Popen('az identity list -o json', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
output, errors = p.communicate()
azr=json.loads(output)
if cde:
    print(json.dumps(azr, indent=4, separators=(',', ': ')))

tfrmf="015-"+tfp+"-staterm.sh"
tfimf="015-"+tfp+"-stateimp.sh"
tfrm=open(tfrmf, 'a')
tfim=open(tfimf, 'a')
print tfp,
count=len(azr)
print count
for j in range(0, count):
    
    name=azr[j]["name"]
    loc=azr[j]["location"]
    id=azr[j]["id"]
    rg=azr[j]["resourceGroup"]

    if crg is not None:
        print "rgname=" + rg + " crg=" + crg
        if rg != crg:
            continue  # back to for
    
    rname=name.replace(".","-")
    prefix=tfp+"."+rg+'__'+rname
    #print prefix
    rfilename=prefix+".tf"
    fr=open(rfilename, 'w')
    fr.write("")
    fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
    fr.write('\t name = "' + name + '"\n')
    fr.write('\t location = "'+ loc + '"\n')
    fr.write('\t resource_group_name = "' + rg + '"\n')
# tags block
    try:
        mtags=azr[j]["tags"]
    except:
        mtags="{}"
    tcount=len(mtags)-1
    if tcount > 1 :
        fr.write('tags { \n')
        print tcount
        for key in mtags.keys():
            tval=mtags[key]
            fr.write('\t "' + key + '"="' + tval + '"\n')
        #print(json.dumps(mtags, indent=4, separators=(',', ': ')))
        fr.write('}\n')
    
    fr.write('}\n') 
    fr.close()  # close .tf file

    tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')
    
    tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
    tfim.write('echo "importing ' + str(j) + ' of ' + str(count-1) + '"' + '\n')
    tfim.write(tfcomm)  

# end for
tfrm.close()
tfim.close()
#end user assigned identity




#  020 ASG's
tfp="azurerm_availability_set"
azr=""
if crf in tfp:

    print "REST Avail Set"
    url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Compute/availabilitySets"
    params = {'api-version': '2018-10-01'}
    r = requests.get(url, headers=headers, params=params)
    azr= r.json()["value"]
    if cde:
        print(json.dumps(azr, indent=4, separators=(',', ': ')))

    tfrmf="020-"+tfp+"-staterm.sh"
    tfimf="020-"+tfp+"-stateimp.sh"
    tfrm=open(tfrmf, 'a')
    tfim=open(tfimf, 'a')
    print tfp,
    count=len(azr)
    print count
    for i in range(0, count):

        name=azr[i]["name"]
        loc=azr[i]["location"]
        id=azr[i]["id"]
        #rg=azr[i]["resourceGroup"]
        rg=id.split("/")[4].replace(".","-")
        fd=str(azr[i]["properties"]["platformFaultDomainCount"])
        ud=str(azr[i]["properties"]["platformUpdateDomainCount"])
        #avm=azr[i]["virtualMachines"]
        skuname=azr[i]["sku"]["name"]
        rmtype="false"
        if "Aligned" in skuname:
            #print "skuname is true"
            rmtype="true"

        if crg is not None:
            if rg != crg:
                continue  # back to for
        
        rname=name.replace(".","-")
        prefix=tfp+"."+rg+'__'+rname
        #print prefix
        rfilename=prefix+".tf"
        fr=open(rfilename, 'w')
        fr.write("")
        fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
        fr.write('\t name = "' + name + '"\n')
        fr.write('\t location = "'+ loc + '"\n')
        fr.write('\t resource_group_name = "'+ rg + '"\n')   
        fr.write('\t platform_fault_domain_count = "' + fd + '"\n')
        fr.write('\t platform_update_domain_count = "' + ud + '"\n')
        fr.write('\t managed = "' + rmtype + '"\n')

    # tags block
        
        try:
            mtags=azr[i]["tags"]
            fr.write('tags { \n')
            for key in mtags.keys():
                tval=mtags[key]
                fr.write('\t "' + key + '"="' + tval + '"\n')
                #print tval
            #print(json.dumps(mtags, indent=4, separators=(',', ': ')))
            fr.write('}\n')
        except KeyError:
            pass
        
        fr.write('}\n') 
        fr.close()   # close .tf file

        tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')
            
        tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
        tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
        tfim.write(tfcomm)  

    # end for i loop

    tfrm.close()
    tfim.close()
#end Avail Set


#  030 Route Table
tfp="azurerm_route_table"
azr=""
if crf in tfp:
    # REST
    print "REST ASG"
    url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Network/routeTables"
    params = {'api-version': '2018-07-01'}
    r=requests.get(url, headers=headers, params=params)
    azr=r.json()["value"]
    if cde:
        print(json.dumps(azr, indent=4, separators=(',', ': ')))


#############
    tfrmf="030-"+tfp+"-staterm.sh"
    tfimf="030-"+tfp+"-stateimp.sh"
    tfrm=open(tfrmf, 'a')
    tfim=open(tfimf, 'a')
    print tfp,
    count=len(azr)
    print count
    for i in range(0, count):

        name=azr[i]["name"]
        loc=azr[i]["location"]
        id=azr[i]["id"]
        rg=id.split("/")[4].replace(".","-")
  
        if crg is not None:
            if rg != crg:
                continue  # back to for
        
        rname=name.replace(".","-")
        prefix=tfp+"."+rg+'__'+rname
        #print prefix
        rfilename=prefix+".tf"
        fr=open(rfilename, 'w')
        fr.write("")
        fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
        fr.write('\t name = "' + name + '"\n')
        fr.write('\t location = "'+ loc + '"\n')
        fr.write('\t resource_group_name = "'+ rg + '"\n')   

       #
        # Interate routes
        #
        routes=azr[i]["properties"]["routes"]
        rcount=len(routes)
        for j in range(0, rcount):
            rtname=routes[j]["name"]
            adpr=routes[j]["properties"]["addressPrefix"]
            nhtype=routes[j]["properties"]["nextHopType"]

            fr.write('\t route {' + '\n')
            fr.write('\t\t name = "' + rtname + '"\n')
            fr.write('\t\t address_prefix = "' + adpr + '"\n')
            fr.write('\t\t next_hop_type = "' + nhtype + '"\n')
            try:
                nhaddr=routes[j]["properties"]["nextHopIpAddress"]
                fr.write('\t\t next_hop_in_ip_address = "' +  nhaddr + '"\n')
            except KeyError:
                pass             
            fr.write('\t }' + '\n')

    # tags block
        
        try:
            mtags=azr[i]["tags"]
            fr.write('tags { \n')
            for key in mtags.keys():
                tval=mtags[key]
                fr.write('\t "' + key + '"="' + tval + '"\n')
                #print tval
            #print(json.dumps(mtags, indent=4, separators=(',', ': ')))
            fr.write('}\n')
        except KeyError:
            pass
        
        fr.write('}\n') 
        fr.close()   # close .tf file

        tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')
            
        tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
        tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
        tfim.write(tfcomm)  

    # end for i loop

    tfrm.close()
    tfim.close()
#end route table



#  040 ASG's
tfp="azurerm_application_security_group"
azr=""
if crf in tfp:
    # REST
    print "REST ASG"

    url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Network/applicationSecurityGroups"
    params = {'api-version': '2018-07-01'}
    r = requests.get(url, headers=headers, params=params)
    azr= r.json()["value"]
    if cde:
        print(json.dumps(azr, indent=4, separators=(',', ': ')))


    tfrmf="040-"+tfp+"-staterm.sh"
    tfimf="040-"+tfp+"-stateimp.sh"
    tfrm=open(tfrmf, 'a')
    tfim=open(tfimf, 'a')
    print tfp,
    count=len(azr)
    print count
    for i in range(0, count):

        name=azr[i]["name"]
        loc=azr[i]["location"]
        id=azr[i]["id"]
    #    rg=azr[i]["resourceGroup"]
        rg=id.split("/")[4].replace(".","-")
        #print rg

        if crg is not None:
            if rg != crg:
                continue  # back to for
        
        rname=name.replace(".","-")
        prefix=tfp+"."+rg+'__'+rname
        #print prefix
        rfilename=prefix+".tf"
        fr=open(rfilename, 'w')
        fr.write("")
        fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
        fr.write('\t name = "' + name + '"\n')
        fr.write('\t location = "'+ loc + '"\n')
        fr.write('\t resource_group_name = "'+ rg + '"\n')   
        

    # tags block
        
        try:
            mtags=azr[i]["tags"]
            fr.write('tags { \n')
            for key in mtags.keys():
                tval=mtags[key]
                fr.write('\t "' + key + '"="' + tval + '"\n')
                #print tval
            #print(json.dumps(mtags, indent=4, separators=(',', ': ')))
            fr.write('}\n')
        except KeyError:
            pass
        
        fr.write('}\n') 
        fr.close()   # close .tf file

        tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')
            
        tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
        tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
        tfim.write(tfcomm)  

    # end for i loop

    tfrm.close()
    tfim.close()
#end ASG

#  050 NSG's
tfp="azurerm_network_security_group"
azr=""
if crf in tfp:
    # REST
    print "REST NSG"

    url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Network/networkSecurityGroups"
    params = {'api-version': '2018-07-01'}
    r = requests.get(url, headers=headers, params=params)
    azr= r.json()["value"]
    if cde:
        print(json.dumps(azr, indent=4, separators=(',', ': ')))




    tfrmf="050-"+tfp+"-staterm.sh"
    tfimf="050-"+tfp+"-stateimp.sh"
    tfrm=open(tfrmf, 'a')
    tfim=open(tfimf, 'a')
    print tfp,
    count=len(azr)
    print count
    for i in range(0, count):

        name=azr[i]["name"]
        loc=azr[i]["location"]
        id=azr[i]["id"]
    #    rg=azr[i]["resourceGroup"]
        rg=id.split("/")[4].replace(".","-")
        #print rg

        if crg is not None:
            if rg != crg:
                continue  # back to for
        
        rname=name.replace(".","-")
        prefix=tfp+"."+rg+'__'+rname
        #print prefix
        rfilename=prefix+".tf"
        fr=open(rfilename, 'w')
        fr.write("")
        fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
        fr.write('\t name = "' + name + '"\n')
        fr.write('\t location = "'+ loc + '"\n')
        fr.write('\t resource_group_name = "'+ rg + '"\n')   
        #
        # Security Rules
        #
        #try:
        srules=azr[i]["properties"]["securityRules"]
        #print srules
        scount=len(srules)
        for j in range(0, scount):  
            #print "j=" + str(j)            
            fr.write('\t security_rule {'  + '\n')
            srname=srules[j]["name"]  
            #print "Security Rule " + srname                   
            fr.write('\t\t name = "' +  srname + '"\n')
            try:
                srdesc=srules[j]["properties"]["description"]                    
                fr.write('\t\t description = "' + srdesc + '"\n')
            except KeyError:
                pass

            sraccess=srules[j]["properties"]["access"]                       
            fr.write('\t\t access = "' +  sraccess + '"\n')
            srpri=str(srules[j]["properties"]["priority"])
            fr.write('\t\t priority = "' + srpri + '"\n')
            srproto=srules[j]["properties"]["protocol"]
            fr.write('\t\t protocol = "' + srproto + '"\n')
            srdir=srules[j]["properties"]["direction"] 
            fr.write('\t\t direction = "' +  srdir + '"\n')
    #source address block
            try:
                srsp=str(srules[j]["properties"]["sourcePortRange"])
                fr.write('\t\t source_port_range = "' + srsp + '"\n')
            except KeyError:
                pass
                
            srsps=str(srules[j]["properties"]["sourcePortRanges"])
            if srsps != "[]" :
                fr.write('\t\t source_port_ranges = "' + srsps + '"\n')
                
            try:
                srsap=srules[j]["properties"]["sourceAddressPrefix"] 
                fr.write('\t\t source_address_prefix = "'+ srsap + '"\n')
            except KeyError:
                pass
                
            srsaps=str(srules[j]["properties"]["sourceAddressPrefixes"]) 
            if srsaps != "[]" :
                fr.write('\t\t source_address_prefixes = "' + srsaps + '"\n')

#destination address block
            try:
                srdp=str(srules[j]["properties"]["destinationPortRange"]) 
                fr.write('\t\t destination_port_range = "' + srdp + '"\n')
            except KeyError:
                pass
            
            srdps=str(srules[j]["properties"]["destinationPortRanges"])
            if srdps != "[]" :
                fr.write('\t\t destination_port_ranges = "' + srdps + '"\n')

            try:
                srdap=srules[j]["properties"]["destinationAddressPrefix"]
                fr.write('\t\t destination_address_prefix = "'+ srdap + '"\n')
            except KeyError:
                pass
            
            srdaps=str(srules[j]["properties"]["destinationAddressPrefixes"]) 
            if srdaps != "[]" :
                fr.write('\t\t source_address_prefixes = "' + srdaps + '"\n')

    # source asg's
            try:
                srsasgs=srules[j]["properties"]["sourceApplicationSecurityGroups"]
                kcount=len(srsasgs)
            except KeyError:
                kcount=0

            for k in range(0, kcount):
                #print "in k k=" + str(k)
                asgnam=srules[j]["properties"]["sourceApplicationSecurityGroups"][k]["id"].split("/")[8].replace(".","-")
                asgrg=srules[j]["properties"]["sourceApplicationSecurityGroups"][k]["id"].split("/")[4].replace(".","-")    
                fr.write('\t\t source_application_security_group_ids = ["${azurerm_application_security_group.' + asgrg + '__' + asgnam + '.id}"]' + '\n')
                    
    # destination asg's
            try:
                srdasgs=srules[j]["properties"]["destinationApplicationSecurityGroups"]
                kcount=len(srdasgs)
            except KeyError:
                kcount=0
            for k in range(0, kcount):
                asgnam=srules[j]["properties"]["destinationApplicationSecurityGroups"][k]["id"].split("/")[8].replace(".","-")
                asgrg=srules[j]["properties"]["destinationApplicationSecurityGroups"][k]["id"].split("/")[4].replace(".","-")    
                fr.write('\t\t destination_application_security_group_ids = ["${azurerm_application_security_group.' + asgrg + '__' + asgnam + '.id}"]' + '\n')
                    
            fr.write('\t}' + '\n')
            
            # end for j loop   
        #except KeyError:
        #    print "No security rules"

    # tags block       
        try:
            mtags=azr[i]["tags"]
            fr.write('tags { \n')
            for key in mtags.keys():
                tval=mtags[key]
                fr.write('\t "' + key + '"="' + tval + '"\n')
                #print tval
            #print(json.dumps(mtags, indent=4, separators=(',', ': ')))
            fr.write('}\n')
        except KeyError:
            pass
        
        fr.write('}\n') 
        fr.close()   # close .tf file

        tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

        tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
        tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
        tfim.write(tfcomm)  

    # end for i loop

    tfrm.close()
    tfim.close()
    #end NSG

#  060 Virtual Networks
tfp="azurerm_virtual_network"
azr=""
if crf in tfp:
    # REST
    print "REST VNets"

    url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Network/virtualNetworks"
    params = {'api-version': '2018-07-01'}
    r = requests.get(url, headers=headers, params=params)
    azr= r.json()["value"]
    if cde:
        print(json.dumps(azr, indent=4, separators=(',', ': ')))


    tfrmf="060-"+tfp+"-staterm.sh"
    tfimf="060-"+tfp+"-stateimp.sh"
    tfrm=open(tfrmf, 'a')
    tfim=open(tfimf, 'a')
    print tfp,
    count=len(azr)
    print count
    for i in range(0, count):

        name=azr[i]["name"]
        loc=azr[i]["location"]
        id=azr[i]["id"]
        rg=id.split("/")[4].replace(".","-")

        if crg is not None:
            if rg != crg:
                continue  # back to for
        
        rname=name.replace(".","-")
        prefix=tfp+"."+rg+'__'+rname
        #print prefix
        rfilename=prefix+".tf"
        fr=open(rfilename, 'w')
        fr.write("")
        fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
        fr.write('\t name = "' + name + '"\n')
        fr.write('\t location = "'+ loc + '"\n')
        fr.write('\t resource_group_name = "'+ rg + '"\n')
        
        addsp=azr[i]["properties"]["addressSpace"]["addressPrefixes"]
        laddsp='['
        for x in addsp:
            laddsp=laddsp+'"'+x+'",'
        laddsp=laddsp+']'
        #print laddsp
        fr.write('\taddress_space =  ' + laddsp + '\n')
        try:
            dns=str(azr[i]["properties"]["dhcpOptions"]["dnsServers"])
            if "[]" not in dns:
                fr.write('\t dns_servers =  "' + dns + '"\n')
        except KeyError:
            pass        


        #
        #loop around subnets
        #
        subs=azr[i]["properties"]["subnets"]
        jcount=len(subs)
        for j in range(0,jcount):
            snname=subs[j]["name"]
            snaddr=subs[j]["properties"]["addressPrefix"]

            fr.write('\tsubnet {'  + '\n')
            fr.write('\t\t name = "'+ snname + '"\n')
            fr.write('\t\t address_prefix = "' + snaddr + '"\n')
            try:
                snnsgid=subs[j]["properties"]["networkSecurityGroup"]["id"]
                nsgnam=snnsgid.split("/")[8].replace(".","-")
                nsgrg=snnsgid.split("/")[4].replace(".","-")          
                fr.write('\t\t security_group = "${azurerm_network_security_group.' + nsgrg + '__' + nsgnam + '.id}"' + '\n')
            except KeyError: 
                pass
            
            fr.write('\t}' + '\n')

    # tags block       
        try:
            mtags=azr[i]["tags"]
            fr.write('tags { \n')
            for key in mtags.keys():
                tval=mtags[key]
                fr.write('\t "' + key + '"="' + tval + '"\n')
            fr.write('}\n')
        except KeyError:
            pass

        fr.write('}\n') 
        fr.close()   # close .tf file

        tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

        tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
        tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
        tfim.write(tfcomm)  

    # end for i loop

    tfrm.close()
    tfim.close()
#end VNET
#############


#  070 subnets
tfp="azurerm_subnet"
if crf in tfp:
# subnet in vnet
    tfrmf="070-"+tfp+"-staterm.sh"
    tfimf="070-"+tfp+"-stateimp.sh"
    tfrm=open(tfrmf, 'a')
    tfim=open(tfimf, 'a')
    print tfp,
    count=len(azr)
    print count
    for i in range(0, count):
        subs=azr[i]["properties"]["subnets"]
        vnetname=azr[i]["name"]
        jcount=len(subs)
        #print "subs="+str(jcount)
        #print (json.dumps(subs, indent=4, separators=(',', ': ')))
        for j in range(0, jcount):
            name=subs[j]["name"]
            #loc=subs[j]["location"] subnets don't have location
            id=subs[j]["id"]
            rg=id.split("/")[4].replace(".","-")

            if crg is not None:
                if rg != crg:
                    continue  # back to for
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t virtual_network_name = "' + vnetname + '"\n') 
            fr.write('\t resource_group_name = "' +  rg + '"\n')

            sprefix=subs[j]["properties"]["addressPrefix"]
            fr.write('\t address_prefix = "' +  sprefix + '"\n')
            rtbid="null"
            try:
                seps=subs[j]["properties"]["serviceEndpoints"]
                kcount=len(seps)
                #print (json.dumps(seps, indent=4, separators=(',', ': ')))
                #print kcount
                lseps='['
                for k in range(0, kcount):
                    x=seps[k]["service"]
                    lseps=lseps+'"'+x+'",'
                lseps=lseps+']'
                fr.write('\t service_endpoints = '+ lseps + '\n')
            except KeyError:
                pass
            
            try:
                snsgid=subs[j]["properties"]["networkSecurityGroup"]["id"].split("/")[8].replace(".","-")
                snsgrg=subs[j]["properties"]["networkSecurityGroup"]["id"].split("/")[4].replace(".","-")
                fr.write('\t network_security_group_id = "${azurerm_network_security_group.' + snsgrg + '__' + snsgid +'.id}"' + '\n')
            except KeyError:
                pass
            
            try:
                rtbid=subs[j]["properties"]["routeTable"]["id"].split("/")[8].replace(".","-")
                rtrg=subs[j]["properties"]["routeTable"]["id"].split("/")[4].replace(".","-")
                fr.write('\t route_table_id = "${azurerm_route_table.' + rtrg + '__' + rtbid +'.id}"' + '\n')
            except KeyError:
                pass         

            fr.write('}' + ' \n')

# azurerm_subnet_network_security_group_association
     
            r1="skip"
            try:
                snsgid=subs[j]["properties"]["networkSecurityGroup"]["id"].split("/")[8].replace(".","-")
                r1="azurerm_subnet_network_security_group_association"
                fr.write('resource ' + r1 + ' ' + rg + '__' + rname + '__' + snsgid + ' {\n') 
                fr.write('\tsubnet_id = "${azurerm_subnet.' + rg + '__' + rname + '.id}"' + '\n')
                fr.write('\tnetwork_security_group_id = "${azurerm_network_security_group.' + snsgrg + '__' + snsgid +'.id}"' + '\n')
                fr.write('}' + ' \n')
            except KeyError:
                pass
                

# azurerm_subnet_route_table_association

            r2="skip"
            try:
                rtbid=subs[j]["properties"]["routeTable"]["id"].split("/")[8].replace(".","-")
                r2="azurerm_subnet_route_table_association"
                fr.write('resource ' + r2 + ' ' + rg + '__' + rname + '__' + rtbid + ' {\n') 
                fr.write('\tsubnet_id = "${azurerm_subnet.' + rg + '__' + rname + '.id}"' + '\n')
                fr.write('\troute_table_id = "${azurerm_route_table.' + rtrg + '__' + rtbid +'.id}"' + '\n')
                fr.write('}' + ' \n')
            except KeyError:
                pass
            

            #fr.write('}\n') 
            fr.close()   # close .tf file


            # azurerm_subnet

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(j) + ' of ' + str(jcount-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm) 

# azurerm_subnet_network_security_group_association

            if "skip" not in r1:
       
                tfrm.write('terraform state rm ' + r1 + '.' + rg + '__' + rname + '__' + snsgid + '\n')
                tfcomm='terraform import '+r1 +'.'+rg+'__'+rname+'__'+snsgid+' '+id+'\n'
                tfim.write(tfcomm)
        

# azurerm_subnet_route_table_association

            if "skip" not in r2:

                tfrm.write('terraform state rm ' + r2 + '.' + rg + '__' + rname + '__' + rtbid + '\n')
                tfcomm='terraform import '+r2 +'.'+rg+'__'+rname+'__'+rtbid+' '+id+'\n'
                tfim.write(tfcomm)
            

        # end j

    ###############
    # specific code end
    ###############
 

    # end for i loop

    tfrm.close()
    tfim.close()
#end subnet


#############
#  080 vnet peering
tfp="azurerm_virtual_network_peering"
if crf in tfp: 
# peering in vnet
    tfrmf="080-"+tfp+"-staterm.sh"
    tfimf="080-"+tfp+"-stateimp.sh"
    tfrm=open(tfrmf, 'a')
    tfim=open(tfimf, 'a')
    print tfp,
    count=len(azr)
    print count
    for i in range(0, count):
        peers=azr[i]["properties"]["virtualNetworkPeerings"]
        vnetname=azr[i]["name"]
        jcount=len(peers)
        for j in range(0, jcount):
            name=peers[j]["name"]
            #loc=peers[j]["location"] peers don't have a location
            id=peers[j]["id"]
            rg=id.split("/")[4].replace(".","-")

            if crg is not None:
                if rg != crg:
                    continue  # back to for
                
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
                
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write("")
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t resource_group_name = "'+ rg + '"\n')
            fr.write('\t virtual_network_name = "' + vnetname + '"\n')


            rvnid=peers[j]["properties"]["remoteVirtualNetwork"]["id"]
            aft=str(peers[j]["properties"]["allowForwardedTraffic"])
            agt=str(peers[j]["properties"]["allowGatewayTransit"])
            avna=str(peers[j]["properties"]["allowVirtualNetworkAccess"])
            urg=str(peers[j]["properties"]["useRemoteGateways"])

            fr.write('\t remote_virtual_network_id = "' +  rvnid + '"\n')
            fr.write('\t allow_forwarded_traffic = "' +  aft + '"\n')
            fr.write('\t allow_gateway_transit = "' +  agt + '"\n')
            fr.write('\t allow_virtual_network_access = "' +  avna + '"\n')
            fr.write('\t use_remote_gateways = "' +  urg + '"\n')
                        
            fr.write('}\n') 
            fr.close()   # close .tf file

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(j) + ' of ' + str(jcount-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  
        # end for j loop
    # end for i loop

    tfrm.close()
    tfim.close()
#end peering

#############
#  090 key vault
tfp="azurerm_key_vault"
azr=""
if crf in tfp:
    # REST or cli
    p = subprocess.Popen('az keyvault list -o json', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, errors = p.communicate()
    azr=json.loads(output)
    if cde:
        print(json.dumps(azr, indent=4, separators=(',', ': ')))
    tfrmf="090-"+tfp+"-staterm.sh"
    tfimf="090-"+tfp+"-stateimp.sh"
    tfrm=open(tfrmf, 'a')
    tfim=open(tfimf, 'a')
    print tfp,
    count=len(azr)
    print count
    for i in range(0, count):

        name=azr[i]["name"]
        loc=azr[i]["location"]
        id=azr[i]["id"]
        rg=id.split("/")[4].replace(".","-")

        if crg is not None:
            if rg != crg:
                continue  # back to for
        
        rname=name.replace(".","-")
        prefix=tfp+"."+rg+'__'+rname
        #print prefix
        rfilename=prefix+".tf"
        fr=open(rfilename, 'w')
        fr.write("")
        fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
        fr.write('\t name = "' + name + '"\n')
        fr.write('\t location = "'+ loc + '"\n')
        fr.write('\t resource_group_name = "'+ rg + '"\n')
        comm="az keyvault show -n "+name+" -o json"
        print comm
        p = subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, errors = p.communicate()
        kvshow=json.loads(output)
        jcount=len(kvshow)
        print(json.dumps(kvshow, indent=4, separators=(',', ': ')))

        sku=kvshow["properties"]["sku"]["name"]
        #if sku" = "premium" : sku="Premium" ; fi
        #if sku" = "standard" : sku="Standard" ; fi
 
        fr.write('\t sku {' + '\n')     
        fr.write('\t\t name="' + sku + '"\n')
        fr.write('\t }' + '\n')

        ten=kvshow["properties"]["tenantId"]     
        fr.write('\t tenant_id="' + ten + '"\n')

        try: 
            endep=str(kvshow["properties"]["enabledForDeployment"])
            fr.write('\t enabled_for_deployment="' +  endep + '"\n')
        except KeyError:
            pass
        
        try:
            endisk=str(kvshow["properties"]["enabledForDiskEncryption"])
            fr.write('\t enabled_for_disk_encryption="' +  endisk + '"\n')
        except KeyError:
            pass       
        
        try:
            entemp=str(kvshow["properties"]["enabledForTemplateDeployment"])
            fr.write('\t enabled_for_template_deployment="' +  entemp + '"\n')
        except KeyError:
            pass

        ap=kvshow["properties"]["accessPolicies"]
                
        #
        # Access Policies
        #
        pcount=len(ap)
        for j in range(0, pcount):    
            fr.write('\t access_policy {' + '\n')
            apten=kvshow["properties"]["accessPolicies"][j]["tenantId"]           
            fr.write('\t\t tenant_id="' + apten + '"\n')
            apoid=kvshow["properties"]["accessPolicies"][j]["objectId"]
            fr.write('\t\t object_id="' + apoid + '"\n')
                
            jkl=kvshow["properties"]["accessPolicies"][j]["permissions"]["keys"]
            jsl=kvshow["properties"]["accessPolicies"][j]["permissions"]["secrets"]
            jcl=kvshow["properties"]["accessPolicies"][j]["permissions"]["certificates"]
                
            kl=len(jkl)
            sl=len(jsl)
            cl=len(jcl)
            print kl  
            fr.write('\t\t key_permissions = [ \n')
            for k in range(0,kl):
                tk=kvshow["properties"]["accessPolicies"][j]["permissions"]["keys"][k]
                fr.write('\t\t\t "' + tk + '",\n')
            fr.write('\t\t ]\n')

            print sl  
            fr.write('\t\t secret_permissions = [ \n')
            for k in range(0,sl):
                tk=kvshow["properties"]["accessPolicies"][j]["permissions"]["secrets"][k]
                fr.write('\t\t\t "' + tk + '",\n')
            fr.write('\t\t ]\n')
            
            print cl  
            fr.write('\t\t certificate_permissions = [ \n')
            for k in range(0,cl):
                tk=kvshow["properties"]["accessPolicies"][j]["permissions"]["certificates"][k]
                fr.write('\t\t\t "' + tk + '",\n')
            fr.write('\t\t ]\n')                          
            fr.write('\t} \n') # end access policy

        
# tags block       
        try:
            mtags=azr[i]["tags"]
            fr.write('tags { \n')
            for key in mtags.keys():
                tval=mtags[key]
                fr.write('\t "' + key + '"="' + tval + '"\n')
            fr.write('}\n')
        except KeyError:
            pass

        

        fr.write('} \n')
        fr.close()   # close .tf file

        if cde:
            with open(rfilename) as f: 
                print f.read()

        tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

        tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
        tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
        tfim.write(tfcomm)  

    # end for i loop

    tfrm.close()
    tfim.close()
#end key vault


#############
#  100 managed disk
tfp="azurerm_managed_disk"
azr=""
if crf in tfp:
# REST or cli
    print "REST Managed Disk"
    url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Compute/disks"
    params = {'api-version': '2017-03-30'}
    r = requests.get(url, headers=headers, params=params)
    azr= r.json()["value"]
    if cde:
        print(json.dumps(azr, indent=4, separators=(',', ': ')))

    tfrmf="100-"+tfp+"-staterm.sh"
    tfimf="100-"+tfp+"-stateimp.sh"
    tfrm=open(tfrmf, 'a')
    tfim=open(tfimf, 'a')
    print tfp,
    count=len(azr)
    print count
    for i in range(0, count):

        name=azr[i]["name"]
        loc=azr[i]["location"]
        id=azr[i]["id"]
        rg=id.split("/")[4].replace(".","-")

        if crg is not None:
            if rg != crg:
                continue  # back to for
        
        rname=name.replace(".","-")
        prefix=tfp+"."+rg+'__'+rname
        #print prefix
        rfilename=prefix+".tf"
        fr=open(rfilename, 'w')
        fr.write("")
        fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
        fr.write('\t name = "' + name + '"\n')
        fr.write('\t location = "'+ loc + '"\n')
        fr.write('\t resource_group_name = "'+ rg + '"\n')

###############
# specific code
###############

# tags block       
        try:
            mtags=azr[i]["tags"]
            fr.write('tags { \n')
            for key in mtags.keys():
                tval=mtags[key]
                fr.write('\t "' + key + '"="' + tval + '"\n')
            fr.write('}\n')
        except KeyError:
            pass

        fr.write('}\n') 
        fr.close()   # close .tf file

        tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

        tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
        tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
        tfim.write(tfcomm)  

    # end for i loop

    tfrm.close()
    tfim.close()
#end managed disk


#############
#  110 storage account
tfp="azurerm_storage_account"
azr=""
if crf in tfp:
# REST or cli
    print "REST Managed Disk"
    url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Storage/storageAccounts"
    params = {'api-version': '2017-10-01'}
    r = requests.get(url, headers=headers, params=params)
    azr= r.json()["value"]
    if cde:
        print(json.dumps(azr, indent=4, separators=(',', ': ')))

    tfrmf="110-"+tfp+"-staterm.sh"
    tfimf="110-"+tfp+"-stateimp.sh"
    tfrm=open(tfrmf, 'a')
    tfim=open(tfimf, 'a')
    print tfp,
    count=len(azr)
    print count
    for i in range(0, count):

        name=azr[i]["name"]
        loc=azr[i]["location"]
        id=azr[i]["id"]
        rg=id.split("/")[4].replace(".","-")

        if crg is not None:
            if rg != crg:
                continue  # back to for
        
        rname=name.replace(".","-")
        prefix=tfp+"."+rg+'__'+rname
        #print prefix
        rfilename=prefix+".tf"
        fr=open(rfilename, 'w')
        fr.write("")
        fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
        fr.write('\t name = "' + name + '"\n')
        fr.write('\t location = "'+ loc + '"\n')
        fr.write('\t resource_group_name = "'+ rg + '"\n')

        satier=azr[i]["sku"]["tier"]
        sakind=azr[i]["kind"]
        sartype=azr[i]["sku"]["name"].split("_")[2]
        saencrypt=azr[i]["properties"]["encryption.services.blob.enabled"]
        fiencrypt=azr[i]["properties"]["encryption.services.file.enabled"]
        sahttps=azr[i]["properties"]["supportsHttpsTrafficOnly"]
        nrs=azr[i]["properties"]["networkAcls"]
        saencs=azr[i]["properties"]["encryption.keySource"]
        
        fr.write('\t account_tier = "' +  satier + '"\n')
        fr.write('\t account_kind = "' +  sakind + '"\n')
        fr.write('\t account_replication_type = "' +  sartype + '"\n')
        fr.write('\t enable_blob_encryption = "' +  saencrypt + '"\n')
        fr.write('\t enable_file_encryption = "' +  fiencrypt + '"\n')
        fr.write('\t enable_https_traffic_only = "' +  sahttps + '"\n')
        fr.write('\t account_encryption_source = "' +  saencs + '"\n')
        
        try:
            byp=azr[i]["properties"]["networkAcls"]["bypass"]

            ipr=azr[i]["properties"]["networkAcls"]["ipRules"]
            vnr=azr[i]["properties"]["networkAcls"]["virtualNetworkRules"]

            icount=len(ipr)
            vcount=len(vnr)
            
            # if the only network rule is AzureServices, dont need a network_rules block
            if byp != "AzureServices" or  icount > 0 or vcount > 0:
                fr.write('\t network_rules { \n')
                byp=byp.replace(",","")
                fr.write('\t\t bypass = ["' +  byp + '"]\n')

                if icount > 0 :
                    for ic in range(0, icount): 
                        ipa=ipr[ic]["ipAddressOrRange"]
                        fr.write('\t\t ip_rules = ["' + ipa + '"]\n')
                    
                
                if vcount > 0 :
                    for vc in range(0,vcount):
                        vnsid=vnr[vc]["virtualNetworkResourceId"]
                        fr.write('\t\t virtual_network_subnet_ids = ["' + vnsid + '"]\n')


        except KeyError:
            pass            

# tags block       
        try:
            mtags=azr[i]["tags"]
            fr.write('tags { \n')
            for key in mtags.keys():
                tval=mtags[key]
                fr.write('\t "' + key + '"="' + tval + '"\n')
            fr.write('}\n')
        except KeyError:
            pass

        fr.write('}\n') 
        fr.close()   # close .tf file

        tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

        tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
        tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
        tfim.write(tfcomm)  

    # end for i loop

    tfrm.close()
    tfim.close()
#end storage account






# ******************************************************************************************
exit()

#rclient = get_client_from_cli_profile(ResourceManagementClient)
#for resource_group in rclient.resource_groups.list():
#    print(resource_group.name)

# template

#############
#  100 managed disk
tfp="azurerm_managed_disk"
azr=""
if crf in tfp:
# REST or cli
    print "REST Managed Disk"
    url="https://management.azure.com/subscriptions/" + sub + "/providers/Microsoft.Compute/disks"
    params = {'api-version': '2017-03-30'}
    r = requests.get(url, headers=headers, params=params)
    azr= r.json()["value"]
    if cde:
        print(json.dumps(azr, indent=4, separators=(',', ': ')))

    tfrmf="100-"+tfp+"-staterm.sh"
    tfimf="100-"+tfp+"-stateimp.sh"
    tfrm=open(tfrmf, 'a')
    tfim=open(tfimf, 'a')
    print tfp,
    count=len(azr)
    print count
    for i in range(0, count):

        name=azr[i]["name"]
        loc=azr[i]["location"]
        id=azr[i]["id"]
        rg=id.split("/")[4].replace(".","-")

        if crg is not None:
            if rg != crg:
                continue  # back to for
        
        rname=name.replace(".","-")
        prefix=tfp+"."+rg+'__'+rname
        #print prefix
        rfilename=prefix+".tf"
        fr=open(rfilename, 'w')
        fr.write("")
        fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
        fr.write('\t name = "' + name + '"\n')
        fr.write('\t location = "'+ loc + '"\n')
        fr.write('\t resource_group_name = "'+ rg + '"\n')

###############
# specific code
###############

# tags block       
        try:
            mtags=azr[i]["tags"]
            fr.write('tags { \n')
            for key in mtags.keys():
                tval=mtags[key]
                fr.write('\t "' + key + '"="' + tval + '"\n')
            fr.write('}\n')
        except KeyError:
            pass

        fr.write('}\n') 
        fr.close()   # close .tf file

        tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

        tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
        tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
        tfim.write(tfcomm)  

    # end for i loop

    tfrm.close()
    tfim.close()
#end managed disk

