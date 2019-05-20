import argparse
import os
import sys
import time
from logging import getLogger, StreamHandler, Formatter, INFO

import cm_client
import yaml
from cm_client.rest import ApiException

logger = getLogger(__name__)
formatter = Formatter('%(asctime)s %(levelname)s %(message)s')
handler = StreamHandler()
handler.setLevel(INFO)
handler.setFormatter(formatter)
logger.setLevel(INFO)
logger.addHandler(handler)


def stop_all_clusters(api_client, api_host):
    api_instance = cm_client.ClustersResourceApi(api_client)
    try:
        # Stop the Clusters managed by this Cloudera Manager.
        api_response = api_instance.read_clusters(view='summary')
        print(f'Stopping Cluster(s) managed by {api_host}:')
        for cluster in api_response.items:
            print(f'Stopping {cluster.display_name}', end='', flush=True)
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


def stop_management_service(api_client, api_host):
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


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(description='Cloudera Cluster and Management Service stop commands')
    parser.add_argument('configfile', nargs='?', default='config.yaml',
                        help='CM API access information in YAML (default config.yaml)')
    args = parser.parse_args()

    try:
        with open(args.configfile, 'r') as f:
            config = yaml.safe_load(f)

        def config_value(key, default):
            return config[key] if key in config else default

        # Configure HTTP basic authentication: basic
        cm_client.configuration.username = os.getenv('CM_ADMIN_USERNAME', config_value('username', 'admin'))
        cm_client.configuration.password = os.getenv('CM_ADMIN_PASSWORD', config_value('password', 'admin'))

        # Create an instance of the API class
        protocol = config_value('protocol', 'http')
        api_host = config_value('api_host', '172.31.227.153')
        api_port = config_value('api_port', '7180')
        api_version = config_value('api_version', 'v32')
        api_uri = f'{protocol}://{api_host}:{api_port}/api/{api_version}'
        logger.debug(f'CM API URI: {api_uri}')
        api_client = cm_client.ApiClient(api_uri)

        stop_all_clusters(api_client, api_host)
        stop_management_service(api_client, api_host)

        return 0

    except IOError as err:
        logger.error(f'IOError: [Errno {err.errno}] {err.strerror}: {args.configfile}')

        return -1


if __name__ == '__main__':
    sys.exit(main())
