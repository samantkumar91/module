from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import logging


class FolderCollector:

    def __init__(self, show_deleted):
        credentials = GoogleCredentials.get_application_default()
        service = discovery.build('cloudresourcemanager', 'v3', credentials=credentials)
        self.instance = service.folders()
        self.instance_type = "folders"
        logging.getLogger().setLevel(logging.INFO)
        self.show_deleted = show_deleted

    def getObjectsListPage(self, parent_folder, next_page_token):
        logging.getLogger().setLevel(logging.INFO)
        request = self.instance.list(parent=parent_folder, showDeleted=self.show_deleted, pageToken=next_page_token)
        response = {}
        try:
            response = request.execute()
        except Exception as ex:
            template = "An exception in {0} of type {1} occurred. Arguments:\n{2!r}"
            message = template.format(self.__class__.__name__, type(ex).__name__, ex.args)
            logging.warning(message)

        folder_list = response.get(self.instance_type, [])
        next_page_token = self.getNextPageToken(response)
        if next_page_token is not None and folder_list:
            folder_list.extend(self.getObjectsListPage(parent_folder, next_page_token))
        return folder_list

    def getNextPageToken(self, response):
        try:
            next_page_token = response.get("nextPageToken")
        except KeyError:
            next_page_token = None
        return next_page_token
