import attr


@attr.s
class _Experiment(object):
    name = attr.ib(type=str, default=None)
    ports = attr.ib(type=str, default=None)
    workspace = attr.ib(type=str, default=None)
    workspace_archive = attr.ib(type=str, default=None)
    workspace_url = attr.ib(type=str, default=None)
    ignore_files = attr.ib(type=list, default=list)
    working_directory = attr.ib(type=str, default=None)
    artifact_directory = attr.ib(type=str, default=None)
    cluster_id = attr.ib(type=int, default=None)
    experiment_env = attr.ib(type=dict, default=dict)
    project_id = attr.ib(type=str, default=None)
    model_type = attr.ib(type=str, default=None)
    model_path = attr.ib(type=str, default=None)
    id = attr.ib(type=str, default=None)
    state = attr.ib(type=int, default=None)


@attr.s
class SingleNodeExperiment(_Experiment):
    container = attr.ib(type=str, default=None)
    machine_type = attr.ib(type=str, default=None)
    command = attr.ib(type=str, default=None)
    container_user = attr.ib(type=str, default=None)
    registry_username = attr.ib(type=str, default=None)
    registry_password = attr.ib(type=str, default=None)
    experiment_type_id = attr.ib(type=int, default=1)

    @experiment_type_id.validator
    def experiment_type_id_validator(self, attribute, value):
        if value is not 1:
            raise ValueError("Single node experiment's type must equal 1")


@attr.s
class MultiNodeExperiment(_Experiment):
    experiment_type_id = attr.ib(type=int, default=None)
    worker_container = attr.ib(type=str, default=None)
    worker_machine_type = attr.ib(type=str, default=None)
    worker_command = attr.ib(type=str, default=None)
    worker_count = attr.ib(type=str, default=None)
    parameter_server_container = attr.ib(type=str, default=None)
    parameter_server_machine_type = attr.ib(type=str, default=None)
    parameter_server_command = attr.ib(type=str, default=None)
    parameter_server_count = attr.ib(type=int, default=None)
    worker_container_user = attr.ib(type=str, default=None)
    worker_registry_username = attr.ib(type=str, default=None)
    worker_registry_password = attr.ib(type=str, default=None)
    parameter_server_container_user = attr.ib(type=str, default=None)
    parameter_server_registry_container_user = attr.ib(type=str, default=None)
    parameter_server_registry_password = attr.ib(type=str, default=None)