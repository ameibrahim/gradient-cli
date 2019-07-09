from .common import ListResources, GetResource
from .. import serializers


class ParseExperimentDictMixin(object):
    def _parse_object(self, experiment_dict, **kwargs):
        if self._is_single_node_experiment(experiment_dict):
            experiment = serializers.SingleNodeExperimentSchema().get_instance(experiment_dict)
        else:
            experiment = serializers.MultiNodeExperimentSchema().get_instance(experiment_dict)

        return experiment

    @staticmethod
    def _is_single_node_experiment(experiment_dict):
        return "parameter_server_machine_type" not in experiment_dict


class ListExperiments(ParseExperimentDictMixin, ListResources):
    def get_request_url(self, **kwargs):
        return "/experiments/"

    def _parse_objects(self, data, **kwargs):
        experiments_dicts = self._get_experiments_dicts_from_json_data(data, kwargs)
        experiments = []
        for experiment_dict in experiments_dicts:
            experiment_dict.update(experiment_dict["templateHistory"]["params"])
            experiment = self._parse_object(experiment_dict)
            experiments.append(experiment)

        return experiments

    @staticmethod
    def _get_experiments_dicts_from_json_data(data, kwargs):
        filtered = bool(kwargs.get("project_id"))
        if not filtered:  # If filtering by project ID response data has different format...
            return data["data"]

        experiments = []
        for project_experiments in data["data"]:
            for experiment in project_experiments["data"]:
                experiments.append(experiment)

        return experiments

    def _get_request_params(self, kwargs):
        params = {"limit": -1}  # so the API sends back full list without pagination

        project_id = kwargs.get("project_id")
        if project_id:
            for i, experiment_id in enumerate(project_id):
                key = "projectHandle[{}]".format(i)
                params[key] = experiment_id

        return params


class GetExperiment(ParseExperimentDictMixin, GetResource):
    def _parse_object(self, experiment_dict, **kwargs):
        experiment_dict = experiment_dict["data"]
        experiment_dict.update(experiment_dict["templateHistory"]["params"])
        return super(GetExperiment, self)._parse_object(experiment_dict, **kwargs)

    def get_request_url(self, **kwargs):
        experiment_id = kwargs["experiment_id"]
        url = "/experiments/{}/".format(experiment_id)
        return url


class ListExperimentLogs(ListResources):
    def __init__(self, api):
        super(ListExperimentLogs, self).__init__(api)

    def get_request_url(self, **kwargs):
        return "/jobs/logs"

    def list(self, experiment_id, line, limit, **kwargs):
        instances = super(ListExperimentLogs, self).list(experiment_id=experiment_id,
                                                         line=line, limit=limit)
        instances = list(instances)  # because here the _parse_objects returns a generator
        return instances

    def yield_logs(self, experiment_id, line=0, limit=10000):

        gen = self._get_logs_generator(experiment_id, line, limit)
        return gen

    def _get_logs_generator(self, experiment_id, line, limit):
        last_line_number = line

        while True:
            logs = self.list(experiment_id, last_line_number, limit)

            for log in logs:
                # stop generator - "PSEOF" indicates there are no more logs
                if log.message == "PSEOF":
                    raise StopIteration()

                last_line_number += 1
                yield log

    def _parse_objects(self, log_rows, **kwargs):
        serializer = serializers.LogRowSchema()
        log_rows = (serializer.get_instance(row) for row in log_rows)
        return log_rows

    def _get_request_params(self, kwargs):
        params = {
            "experimentId": kwargs["experiment_id"],
            "line": kwargs["line"],
            "limit": kwargs["limit"],
        }
        return params