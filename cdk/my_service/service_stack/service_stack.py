import os
from pathlib import Path

from aws_cdk import Stack
from constructs import Construct
from git import Repo
from my_service.service_stack.configuration.configuration_construct import ConfigurationStore
from my_service.service_stack.constants import CONFIGURATION_NAME, ENVIRONMENT, SERVICE_NAME
from my_service.service_stack.service_construct import ApiConstruct


def get_stack_name() -> str:
    repo = Repo(Path.cwd())
    try:
        username = os.getlogin().replace('.', '-')
    except Exception:
        username = 'main'
    print(f'username={username}')
    try:
        return f'{username}-{repo.active_branch}-{SERVICE_NAME}'
    except TypeError:
        return f'{username}-{SERVICE_NAME}'


class ServiceStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # This construct should be deployed in a different repo and have its own pipeline so updates can be decoupled
        # from running the service pipeline and without redeploying the service lambdas. For the sake of this template
        # example, it is deployed as part of the service stack
        self.dynamic_configuration = ConfigurationStore(self, 'dynamic_conf'[0:64], ENVIRONMENT, SERVICE_NAME, CONFIGURATION_NAME)
        self.lambdas = ApiConstruct(self, 'Service'[0:64])
