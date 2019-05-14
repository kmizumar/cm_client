import cm_client
from cm_client.rest import ApiException
import time

# Configure HTTP basic authentication: basic
cm_client.configuration.username = 'cloudera'
cm_client.configuration.password = 'cloudera'

# Create an instance of the API class
protocol = 'http'
api_host = '172.31.227.153'
api_port = '7180'
api_version = 'v32'
api_uri = f'{protocol}://{api_host}:{api_port}/api/{api_version}'
api_client = cm_client.ApiClient(api_uri)


api_instance = cm_client.ClustersResourceApi(api_client)
try:
    # Stop the Clusters managed by this Cloudera Manager.
    api_response = api_instance.read_clusters(view='summary')
    print(f'Stopping Cluster(s) managed by {api_host}:')
    for cluster in api_response.items:
        print(f'Stopping {cluster.name}', end='', flush=True)
        api_instance.stop_command(cluster.name)
        while True:
            print('.', end='', flush=True)
            time.sleep(1)
            api_response = api_instance.read_cluster(cluster.name)
            if api_response.entity_status == 'STOPPED':
                print('\nStopped.', flush=True)
                break
except ApiException as e:
    print(f'Exception while calling ClusterResourceApi->read_clusters/stop_command: {e}')


api_instance = cm_client.MgmtServiceResourceApi(api_client)
try:
    # Stop the Cloudera Management Services.
    print(f'Stopping Cloudera Management Service on {api_host}', end='')
    api_response = api_instance.stop_command()
    while True:
        print('.', end='', flush=True)
        time.sleep(1)
        api_response = api_instance.read_service(view='summary')
        if api_response.service_state == 'STOPPED':
            print('\nStopped.', flush=True)
            break
except ApiException as e:
    print(f'Exception while calling MgmtServiceResourceApi->stop_command/read_service: {e}')


if __name__ == '__main__':
    print(f'Hello, Python world!')
