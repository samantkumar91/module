from project_collector import ProjectCollector
from folder_collector import FolderCollector


class ProjectDiscovery:

    def __init__(self, show_deleted):
        self.project_retreiver = ProjectCollector(show_deleted)
        self.folder_retreiver = FolderCollector(show_deleted)

    def lister(self, parent):
        project_list = self.project_retreiver.getObjectsListPage(parent, None)

        folder_list = self.folder_retreiver.getObjectsListPage(parent, None)

        for folder in folder_list:
            project_list.extend(self.lister(folder.get("name")))
        return project_list
