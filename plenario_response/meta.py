class Meta(object):

    def __init__(self, json_payload_dict):
        self.payload = json_payload_dict
        self.params = self.payload.get('params')
        self.links = self.payload.get('links')
        self.counts = self.payload.get('counts')

    def get_page(self):
        return self.params.get('page_size')

    def get_page_size(self):
        return self.params.get('page_size')

    def get_current_page_link(self):
        return self.links.get('current')

    def get_next_page_link(self):
        return self.links.get('current')

    def get_previous_link(self):
        return self.links.get('previous')

    def get_counts(self):
        return self.counts
