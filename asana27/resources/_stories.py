# This file is automatically generated by generate.py using api.json

class _Stories:
    def __init__(self, client=None):
        self.client = client

    def find_by_task(self, task_id, params={}, **options):
        """Returns the stories on a task."""
        path = '/tasks/%s/stories' % (task_id)
        return self.client.get_collection(path, params, **options)

    def create_on_task(self, task_id, params={}, **options):
        """Creates a story on the task."""
        path = '/tasks/%s/stories' % (task_id)
        return self.client.post(path, params, **options)

    def find_by_id(self, story_id, params={}, **options):
        """Returns the story."""
        path = '/stories/%s' % (story_id)
        return self.client.get(path, params, **options)
