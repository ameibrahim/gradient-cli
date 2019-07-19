from gradient.api_sdk.repositories import ListResources
from .. import serializers


class ParseModelDictMixin(object):
    def _parse_object(self, model_dict, **kwargs):
        """
        :param dict model_dict:
        :rtype Model
        """
        model = serializers.Model().get_instance(model_dict)
        return model


class ListModels(ParseModelDictMixin, ListResources):
    def get_request_url(self, **kwargs):
        return "/mlModels/getModelList/"

    def _parse_objects(self, data, **kwargs):
        experiments = []
        for model_dict in data["modelList"]:
            experiment = self._parse_object(model_dict)
            experiments.append(experiment)

        return experiments

    def _get_request_params(self, kwargs):
        return {"limit": -1}

    def _get_request_json(self, kwargs):
        filters = {}
        if kwargs.get("experiment_id"):
            filters["experimentId"] = kwargs.get("experiment_id")
        if kwargs.get("project_id"):
            filters["projectId"] = kwargs.get("project_id")

        if not filters:
            return None

        json_ = {"filter": {"where": {"and": [filters]}}}
        return json_