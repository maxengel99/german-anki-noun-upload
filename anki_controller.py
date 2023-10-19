import json
import urllib.request

class AnkiController:
    """Handles interaction with anki"""

    def generate_payload(self, action, params):
        return {
            "action": action,
            "version": 6,
            "params": params
        }

    def invoke(self, action, params):
        payload = self.generate_payload(action, params)
        return json.load(
            urllib.request.urlopen(
                'http://localhost:8765',
                json.dumps(payload).encode('utf-8')))
        return response
