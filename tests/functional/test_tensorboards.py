import mock
from click.testing import CliRunner

import gradient.api_sdk.clients.http_client
from gradient.cli import cli
from tests import MockResponse, example_responses


class TestTensorboardsCreate(object):
    URL = "https://api.paperspace.io/tensorboards/v1/"
    COMMAND = [
        "tensorboards",
        "create",
        "--experiment", "some_experiment_id",
        "--experiment", "some_other_experiment_id",
    ]
    EXPECTED_REQUEST_JSON = {"experiments": ["some_experiment_id", "some_other_experiment_id"]}
    EXPECTED_RESPONSE_JSON = example_responses.TENSORBOARD_CREATE_RESPONSE_JSON
    EXPECTED_STDOUT = """Created new tensorboard with id: some_id\n"""

    COMMAND_WITH_API_KEY_CHANGED = [
        "tensorboards",
        "create",
        "--experiment", "some_experiment_id",
        "--experiment", "some_other_experiment_id",
        "--apiKey", "some_key",
    ]
    COMMAND_WITH_ALL_OPTIONS = [
        "tensorboards",
        "create",
        "--experiment", "some_experiment_id",
        "--experiment", "some_other_experiment_id",
        "--image", "some_image",
        "--username", "some_username",
        "--password", "some_password",
        "--instanceType", "some_instance_type",
        "--instanceSize", "some_instance_size",
        "--instancesCount", 2,
        "--apiKey", "some_key",
    ]

    EXPECTED_REQUEST_JSON_WITH_ALL_OPTIONS = {
        "experiments": [
            "some_experiment_id",
            "some_other_experiment_id",
        ],
        "image": "some_image",
        "username": "some_username",
        "password": "some_password",
        "instance": {
            "type": "some_instance_type",
            "size": "some_instance_size",
            "count": 2,
        }
    }
    COMMAND_WITH_OPTIONS_FILE_USED = ["tensorboards", "create", "--optionsFile", ]  # path added in test

    EXPECTED_HEADERS = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"title": "Invalid credentials provided"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to create resource: Invalid credentials provided\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_valid_request_when_command_was_executed_with_required_options(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             data=None,
                                             files=None,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_request_with_changed_api_key_when_api_key_option_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_CHANGED)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON,
                                             data=None,
                                             files=None,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_send_valid_request_when_command_was_executed_with_all_options(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_ALL_OPTIONS)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON_WITH_ALL_OPTIONS,
                                             data=None,
                                             files=None,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.post")
    def test_should_read_options_from_yaml_file(self, post_patched, tensorboards_create_config_path):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE_USED[:] + [tensorboards_create_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=self.EXPECTED_REQUEST_JSON_WITH_ALL_OPTIONS,
                                             data=None,
                                             files=None,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"


class TestTensorboardsDetail(object):
    URL = "https://api.paperspace.io/tensorboards/v1/some_id/"
    COMMAND = [
        "tensorboards",
        "details",
        "--id", "some_id",
    ]
    EXPECTED_RESPONSE_JSON = example_responses.TENSORBOARD_CREATE_RESPONSE_JSON
    EXPECTED_STDOUT = """+----------------+----------------------------------+
| ID             | some_id                          |
+----------------+----------------------------------+
| Image          | tensorflow/tensorflow:latest-py3 |
| URL            | None                             |
| State          | 1                                |
| Instance type  | cpu                              |
| Instance size  | large                            |
| Instance count | 2                                |
+----------------+----------------------------------+
"""

    COMMAND_WITH_API_KEY_CHANGED = [
        "tensorboards",
        "details",
        "--id", "some_id",
        "--apiKey", "some_key",
    ]
    COMMAND_WITH_OPTIONS_FILE_USED = ["tensorboards", "details", "--optionsFile", ]  # path added in test

    EXPECTED_HEADERS = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"title": "Invalid credentials provided"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to create resource: Invalid credentials provided\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_request_when_command_was_executed_with_required_options(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=None,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_request_with_changed_api_key_when_api_key_option_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_CHANGED)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=None,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(self, post_patched, tensorboards_details_config_path):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE_USED[:] + [tensorboards_details_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=None,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"


class TestTensorboardsDetail(object):
    URL = "https://api.paperspace.io/tensorboards/v1/"
    COMMAND = ["tensorboards", "list"]
    EXPECTED_RESPONSE_JSON = example_responses.TENSORBOARD_CREATE_RESPONSE_JSON
    EXPECTED_STDOUT = """+----------------+----------------------------------+
| ID             | some_id                          |
+----------------+----------------------------------+
| Image          | tensorflow/tensorflow:latest-py3 |
| URL            | None                             |
| State          | 1                                |
| Instance type  | cpu                              |
| Instance size  | large                            |
| Instance count | 2                                |
+----------------+----------------------------------+
"""

    COMMAND_WITH_API_KEY_CHANGED = ["tensorboards", "list", "--apiKey", "some_key"]
    COMMAND_WITH_OPTIONS_FILE_USED = ["tensorboards", "list", "--optionsFile", ]  # path added in test

    EXPECTED_HEADERS = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY = gradient.api_sdk.clients.http_client.default_headers.copy()
    EXPECTED_HEADERS_WITH_CHANGED_API_KEY["X-API-Key"] = "some_key"

    RESPONSE_JSON_WITH_WRONG_API_TOKEN = {"title": "Invalid credentials provided"}
    EXPECTED_STDOUT_WITH_WRONG_API_TOKEN = "Failed to create resource: Invalid credentials provided\n"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_valid_request_when_command_was_executed_with_required_options(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS,
                                             json=None,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_send_request_with_changed_api_key_when_api_key_option_was_used(self, post_patched):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)

        runner = CliRunner()
        result = runner.invoke(cli.cli, self.COMMAND_WITH_API_KEY_CHANGED)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=None,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"

    @mock.patch("gradient.api_sdk.clients.http_client.requests.get")
    def test_should_read_options_from_yaml_file(self, post_patched, tensorboards_details_config_path):
        post_patched.return_value = MockResponse(self.EXPECTED_RESPONSE_JSON)
        command = self.COMMAND_WITH_OPTIONS_FILE_USED[:] + [tensorboards_details_config_path]

        runner = CliRunner()
        result = runner.invoke(cli.cli, command)

        assert result.output == self.EXPECTED_STDOUT, result.exc_info
        post_patched.assert_called_once_with(self.URL,
                                             headers=self.EXPECTED_HEADERS_WITH_CHANGED_API_KEY,
                                             json=None,
                                             params=None)
        assert self.EXPECTED_HEADERS["X-API-Key"] != "some_key"