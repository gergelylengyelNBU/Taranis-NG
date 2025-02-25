from marshmallow import post_load
from sqlalchemy import orm, or_, func
import uuid
from datetime import datetime

from managers.db_manager import db
from managers.log_manager import log_debug_trace
from schema.collectors_node import CollectorsNodeSchema, CollectorsNodePresentationSchema

class NewCollectorsNodeSchema(CollectorsNodeSchema):

    @post_load
    def make_collectors_node(self, data, **kwargs):
        return CollectorsNode(name=data['name'], description=data['description'], api_url=data['api_url'], api_key=data['api_key'])


class CollectorsNode(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String())

    api_url = db.Column(db.String(), nullable=False)
    api_key = db.Column(db.String(), nullable=False)

    created = db.Column(db.DateTime, default=datetime.now)
    last_seen = db.Column(db.DateTime, default=datetime.now)

    collectors = db.relationship('Collector', back_populates="node", cascade="all")

    def __init__(self, name, description, api_url, api_key):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.api_url = api_url
        self.api_key = api_key
        self.tag = ""

    @orm.reconstructor
    def reconstruct(self):
        self.tag = "mdi-server-network"

    @classmethod
    def exists_by_api_key(cls, api_key):
        return db.session.query(db.exists().where(CollectorsNode.api_key == api_key)).scalar()

    @classmethod
    def get_by_api_key(cls, api_key):
        return cls.query.filter_by(api_key=api_key).first()

    @classmethod
    def get_all(cls):
        return cls.query.order_by(db.asc(CollectorsNode.name)).all()

    @classmethod
    def get(cls, search):
        query = cls.query

        if search is not None:
            search_string = '%' + search.lower() + '%'
            query = query.filter(or_(
                func.lower(CollectorsNode.name).like(search_string),
                func.lower(CollectorsNode.description).like(search_string)))

        return query.order_by(db.asc(CollectorsNode.name)).all(), query.count()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_all_json(cls, search):
        nodes, count = cls.get(search)
        node_schema = CollectorsNodePresentationSchema(many=True)
        items = node_schema.dump(nodes)

        for i in range(len(items)):
            # calculate collector status
            #   green (last ping in time) < 60s
            #   orange (last ping late) < 300s
            #   red (no ping in a long time) > 300s
            try:
                time_inactive = (datetime.now() - max(nodes[i].created, nodes[i].last_seen))
                items[i]["status"] = "green" if time_inactive.seconds < 60 else "orange" if time_inactive.seconds < 300 else "red"
            except Exception as ex:
                log_debug_trace("Cannot update collector status.")
                # if never collected before
                items[i]["status"] = "red"

        return {'total_count': count, 'items': items}

    @classmethod
    def add_new(cls, node_data, collectors):
        new_node_schema = NewCollectorsNodeSchema()
        node = new_node_schema.load(node_data)
        node.collectors = collectors
        db.session.add(node)
        db.session.commit()
        return node

    @classmethod
    def update(cls, node_id, node_data, collectors):
        new_node_schema = NewCollectorsNodeSchema()
        updated_node = new_node_schema.load(node_data)
        node = cls.query.get(node_id)
        node.name = updated_node.name
        node.description = updated_node.description
        node.api_url = updated_node.api_url
        node.api_key = updated_node.api_key
        for collector in collectors:
            found = False
            for existing_collector in node.collectors:
                if collector.type == existing_collector.type:
                    found = True
                    break

            if found is False:
                node.collectors.append(collector)

        db.session.commit()

    @classmethod
    def delete(cls, node_id):
        node = cls.query.get(node_id)
        for collector in node.collectors:
            if len(collector.sources) > 0:
                raise Exception("Collectors has mapped sources")

        db.session.delete(node)
        db.session.commit()

    def updateLastSeen(self):
        self.last_seen = datetime.now()
        db.session.add(self)
        db.session.commit()
