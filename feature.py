class FeatureStatus:
    def __init__(self, feature, html_file_name, status):
        self.feature = feature
        self.html_file_name = html_file_name
        self.status = status
        
    def update_status(self, new_status):
        self.status = new_status