from elasticsearch import Elasticsearch
import datetime
import uuid


class ElasticsearchUtils:
    def __init__(self, host="http://localhost:9200", username="", password="", base_index_name="log_messages"):
        self.es = Elasticsearch(hosts=[host], http_auth=(username, password))
        self.base_index_name = base_index_name
        self._ensure_index_template()

    def _ensure_index_template(self):
        template_name = f"{self.base_index_name}_template"
        if not self.es.indices.exists_index_template(name=template_name):
            self.es.indices.put_index_template(
                name=template_name,
                body={
                    "index_patterns": [f"{self.base_index_name}-*"],
                    "template": {
                        "mappings": {
                            "properties": {
                                "message": {"type": "text"},
                                "username": {"type": "keyword"},
                                "msg_id": {"type": "keyword"},
                                "timestamp": {"type": "date"},
                            }
                        },
                        "settings": {
                            "number_of_shards": 1,
                            "number_of_replicas": 1,
                        },
                    },
                    "priority": 1,
                },
            )
            print(f"Index template '{template_name}' created successfully.")
        else:
            print(f"Index template '{template_name}' already exists.")

    def _get_date_based_index_name(self):
        date_suffix = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        return f"{self.base_index_name}-{date_suffix}"

    def log_message(self, message, username, msg_id):
        msg_id = str(uuid.uuid4())
        timestamp = datetime.datetime.utcnow().isoformat()

        doc = {
            "message": message,
            "username": username,
            "msg_id": msg_id,
            "timestamp": timestamp,
        }

        index_name = self._get_date_based_index_name()
        print(doc)
        response = self.es.index(index=index_name, document=doc)
        print(response)
        return response

    def search_logs(self, query=None, index_pattern=None):
        if query is None:
            query = {"query": {"match_all": {}}}

        if index_pattern is None:
            index_pattern = f"{self.base_index_name}-*"

        response = self.es.search(index=index_pattern, body=query)
        return response.get("hits", {}).get("hits", [])

