# Dev-eks-terminate-node

This Lambda function responds to an SNS message which is generated from a CloudWatch alert. The alert is due to one of the nodes in the `Dev EKS cluster` being in a unknown state.  When this function is triggered by the SNS message it is subscribed, it checks all nodes in the cluster and terminates any nodes that are not in a known or normal state.

