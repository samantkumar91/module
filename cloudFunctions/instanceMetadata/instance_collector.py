from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import logging
from folder_collector import FolderCollector


class InstanceCollector(FolderCollector):

  def __init__(self):
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    self.instance=service.instances()
    self.instance_type ="items"
    logging.getLogger().setLevel(logging.INFO)

  def getObjectsListPage(self, project_name,next_page_token):
    logging.getLogger().setLevel(logging.INFO)
    request = self.instance.aggregatedList(project=project_name,pageToken=next_page_token)
    try:
      response = request.execute()
    except Exception as ex:
      template = "An exception in {0} of type {1} occurred. Arguments:\n{2!r}"
      message = template.format(self.__class__.__name__,type(ex).__name__, ex.args)
      logging.warning(message)
      return ""
    zone_list= response.get(self.instance_type, [])
    next_page_token = self.getNextPageToken(response)
    if next_page_token is not None and zone_list:
      zone_list.extend(self.getObjectsListPage(project_name,next_page_token))
    return zone_list