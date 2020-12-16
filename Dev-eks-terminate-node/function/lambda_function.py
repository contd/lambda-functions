import logging
import boto3
from botocore.config import Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def list_instances(client):
    response = client.describe_instances(
        Filters=[
            {
                'Name': 'tag:eks:cluster-name',
                'Values': [
                    'Dev_eks_cluster',
                ]
            },
        ]
    )
    return response

def terminate(instanceId='', client=''):
    if instanceId:
        response = client.terminate_instances(
            InstanceIds=[
                instanceId,
            ],
            DryRun=False
        )
        return response

def lambda_handler(event, context):
    config = Config( region_name = 'us-east-2' )
    client = boto3.client('ec2', config=config)
    nodes = {}
    logger.info("##########  DEV EKS Terminate Node  #################")

    response = list_instances(client)
    if not response:
        logger.info('Nothing found with that filter.')
    else:
        for reservations in response['Reservations']:
            for instances in reservations['Instances']:
                nodes[instances['InstanceId']] = instances['State']['Name']
        for id,state in nodes.items():
            if state != 'pending' and state != 'running' and state != 'shutting-down' and state != 'terminated' and state != 'stopping' and state != 'stopped':
                logger.info('Time to terminate: %s: %s' % (id, state))
                tresp = terminate(instanceId=id, client=client)
                if tresp:
                    logger.info('Termination response: {}'.format(tresp))
            else:
                logger.info("%s - %s" % (id, state))
    logger.info("--------------- event   ------------------------")
    logger.info(event)
    logger.info("--------------- context ------------------------")
    logger.info(context)
    logger.info("##########  END  ######################")
