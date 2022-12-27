from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import logging
from folder_collector import FolderCollector

class ProjectCollector(FolderCollector):

  def __init__(self,show_deleted):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('cloudresourcemanager', 'v3', credentials=credentials)
    self.instance=service.projects()
    self.instance_type ="projects"
    logging.getLogger().setLevel(logging.INFO)
    self.show_deleted=show_deleted



