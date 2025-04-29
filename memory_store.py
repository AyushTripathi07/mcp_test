# memory_store.py
import os
import json
from typing import List, Dict

MEMORY_FILE_PATH = "/Users/ayush/Documents/ArcMCP/memory.json"


class KnowledgeGraphManager:
    def __init__(self):
        self.entities = []
        self.relations = []
        self._load()

    def _load(self):
        if not os.path.exists(MEMORY_FILE_PATH):
            self.entities = []
            self.relations = []
            return
        with open(MEMORY_FILE_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            obj = json.loads(line)
            if obj["type"] == "entity":
                self.entities.append(obj)
            elif obj["type"] == "relation":
                self.relations.append(obj)

    def _save(self):
        with open(MEMORY_FILE_PATH, "w", encoding="utf-8") as f:
            for e in self.entities:
                f.write(json.dumps({**e, "type": "entity"}) + "\n")
            for r in self.relations:
                f.write(json.dumps({**r, "type": "relation"}) + "\n")

    def create_entities(self, entities: List[Dict]) -> List[Dict]:
        new = [e for e in entities if not any(x["name"] == e["name"] for x in self.entities)]
        self.entities.extend(new)
        self._save()
        return new

    def create_relations(self, relations: List[Dict]) -> List[Dict]:
        new = [r for r in relations if not any(
            x["from"] == r["from"] and x["to"] == r["to"] and x["relationType"] == r["relationType"]
            for x in self.relations)]
        self.relations.extend(new)
        self._save()
        return new

    def add_observations(self, updates: List[Dict]) -> List[Dict]:
        results = []
        for u in updates:
            entity = next((e for e in self.entities if e["name"] == u["entityName"]), None)
            if entity:
                new_obs = [o for o in u["contents"] if o not in entity["observations"]]
                entity["observations"].extend(new_obs)
                results.append({"entityName": u["entityName"], "addedObservations": new_obs})
        self._save()
        return results

    def delete_entities(self, names: List[str]):
        self.entities = [e for e in self.entities if e["name"] not in names]
        self.relations = [r for r in self.relations if r["from"] not in names and r["to"] not in names]
        self._save()

    def delete_observations(self, deletions: List[Dict]):
        for d in deletions:
            entity = next((e for e in self.entities if e["name"] == d["entityName"]), None)
            if entity:
                entity["observations"] = [o for o in entity["observations"] if o not in d["observations"]]
        self._save()

    def delete_relations(self, rels: List[Dict]):
        self.relations = [r for r in self.relations if not any(
            r["from"] == dr["from"] and r["to"] == dr["to"] and r["relationType"] == dr["relationType"]
            for dr in rels)]
        self._save()

    def read_graph(self) -> Dict:
        return {"entities": self.entities, "relations": self.relations}

    def search_nodes(self, query: str) -> Dict:
        filtered = [e for e in self.entities if query.lower() in e["name"].lower()
                    or query.lower() in e["entityType"].lower()
                    or any(query.lower() in o.lower() for o in e["observations"])]
        names = {e["name"] for e in filtered}
        rels = [r for r in self.relations if r["from"] in names and r["to"] in names]
        return {"entities": filtered, "relations": rels}

    def open_nodes(self, names: List[str]) -> Dict:
        ents = [e for e in self.entities if e["name"] in names]
        rels = [r for r in self.relations if r["from"] in names and r["to"] in names]
        return {"entities": ents, "relations": rels}