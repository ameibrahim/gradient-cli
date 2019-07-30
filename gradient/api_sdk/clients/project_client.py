from gradient.config import config
from .base_client import BaseClient
from .. import models, repositories


class ProjectsClient(BaseClient):
    HOST_URL = config.CONFIG_HOST

    def create(self, name, repository_name=None, repository_url=None):
        """Create new project

        *EXAMPLE*::

            gradient projects create --name new-project

        *EXAMPLE RETURN*::

            Project created with ID: <your-project-id>

        :param str name: Name of new project [required]
        :param str repository_name: Name of the repository
        :param str repository_url: URL to the repository

        :returns: project ID
        :rtype: str
        """

        project = models.Project(
            name=name,
            repository_name=repository_name,
            repository_url=repository_url,
        )

        handle = repositories.CreateProject(self.client).create(project)
        return handle

    def list(self):
        """Get list of your projects

        *EXAMPLE*::

            gradient projects list

        *EXAMPLE RETURN*::

            +-----------+------------------+------------+----------------------------+
            | ID        | Name             | Repository | Created                    |
            +-----------+------------------+------------+----------------------------+
            | project-id| <name-of-project>| None       | 2019-06-28 10:38:57.874000 |
            | project-id| <name-of-project>| None       | 2019-07-17 13:17:34.493000 |
            | project-id| <name-of-project>| None       | 2019-07-17 13:21:12.770000 |
            | project-id| <name-of-project>| None       | 2019-07-29 09:26:49.105000 |
            +-----------+------------------+------------+----------------------------+


        :returns: list of projects
        :rtype: list[models.Project]
        """
        projects = repositories.ListProjects(self.client).list()
        return projects