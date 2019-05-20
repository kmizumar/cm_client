# Stop CDH Cluster(s) and Management Service

Simple Python3 script to stop CDH Cluster(s) and Management Services through [Cloudera Manager API](https://cloudera.github.io/cm_api/).

# Sample output

```text
% python3 stop-all.py
Stopping Cluster(s) managed by 172.31.227.153:
Stopping Cloudera QuickStart..................
Stopped.
Stopping Cloudera Management Service on 172.31.227.153......
Stopped.
```

# How to run this script
## Prerequisites
See `requirements.txt` for dependent pip packages.

## Running it

`stop-all.py` will try to pick necessary information from `config.yaml` file or any file you passed to the script.
The YAML file may hold the following parameters to be used connect to your Cloudera Manager Server instance:

| parameter |default value |
:---:|:---:
| protocol | http |
| api_host | cloudera-manager.example.com |
| api_port | 7180 | 
| api_version | v32 |
| username | admin |
| password | admin |

To avoid writing sensitive information in a file,
`stop-all.py` also recognizes the following OS environment variables in your runtime:

- CM_ADMIN_USERNAME
- CM_ADMIN_PASSWORD

These two environment variables have higher precedence over the username and password parameters in the YAML file,
respectively.

## Usage
```text
% python3 stop-all.py -h
usage: stop-all.py [-h] [configfile]

Cloudera Cluster and Management Service stop commands

positional arguments:
  configfile  CM API access information in YAML (default config.yaml)

optional arguments:
  -h, --help  show this help message and exit  
```
