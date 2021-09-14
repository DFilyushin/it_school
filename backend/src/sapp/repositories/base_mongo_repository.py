import asyncio
from dataclasses import dataclass
from typing import Optional, List, Iterable, Dict
from sapp.connectors.mongo_connector import MongoDBConnector
from sapp.settings import Settings
from pymongo import ASCENDING


@dataclass
class IndexDef:
    field_name: str
    sort: int = ASCENDING


@dataclass
class BaseMongoRepository:
    connection_manager: MongoDBConnector
    settings: Settings

    def __post_init__(self):
        self.database = self.settings.mongodb_database

    @property
    def collection_name(self) -> str:
        """
        Get default collection name
        :return:
        """
        raise NotImplementedError

    @property
    def collection_indexes(self) -> Iterable[IndexDef]:
        """
        Get indexes list
        :return:
        """
        raise NotImplementedError

    async def create_index(self, field_name: str, sort_id: int) -> None:
        """
        Create index
        :param field_name:
        :param sort_id:
        :return:
        """
        connection = await self.connection_manager.get_connection_async()
        collection = connection[self.database][self.collection_name]
        await collection.create_index([(field_name, sort_id), ], background=True)

    def create_indexes(self) -> None:
        """
        Create indexes async
        :return:
        """
        tasks = []
        for index_item in self.collection_indexes:
            tasks.append(self.create_index(index_item.field_name, index_item.sort))
        asyncio.ensure_future(asyncio.gather(*tasks))

    async def get_data(self, criteria_dict: dict) -> Optional[dict]:
        """
        Get data by criteria

        :param criteria_dict:
        :return: found data as dict
        """
        connection = await self.connection_manager.get_connection_async()
        collection = connection[self.database][self.collection_name]

        data = await collection.find_one(criteria_dict)
        if not data:
            return None

        return data

    async def add_data(self, document: dict) -> str:
        """
        Saving document to database

        :param document: dictionary
        :return:
        """
        connection = await self.connection_manager.get_connection_async()
        result = await connection[self.database][self.collection_name].insert_one(document)

        return result.inserted_id

    async def add_item_to_array(self, criteria_dict: dict, array_field: str, data: dict,
                                array_filter: List[Dict] = None) -> str:
        """
        Add item to array

        :param array_field:
        :param criteria_dict: dictionary
        :param data: dictionary of update field and data
        :param array_filter: Additional filter for using embedded documents
        :return:
        """
        connection = await self.connection_manager.get_connection_async()
        result = await connection[self.database][self.collection_name].update_one(
            filter=criteria_dict,
            update={'$push': {array_field: data}},
            array_filters=array_filter,
            upsert=False
        )
        return result.raw_result

    async def remove_item_from_array(self, criteria_dict: dict, array_field: str, data: dict,
                                     array_filter: List[Dict] = None) -> str:
        connection = await self.connection_manager.get_connection_async()
        result = await connection[self.database][self.collection_name].update_one(
            filter=criteria_dict,
            update={'$pull': {array_field: data}},
            upsert=False
        )
        return result.raw_result['nModified']

    async def update_data(self, criteria_dict: dict, data: dict, array_filter: List[Dict] = None) -> str:
        """
        Update document by criteria

        :param criteria_dict: dictionary
        :param data: dictionary of update field and data
        :param array_filter: Additional filter for using embedded documents
        :return:
        """
        connection = await self.connection_manager.get_connection_async()
        result = await connection[self.database][self.collection_name].update_one(
            filter=criteria_dict,
            update={'$set': data},
            array_filters=array_filter,
            upsert=False
        )
        return result.raw_result

    async def get_list_data(self, criteria_dict: dict) -> List[dict]:
        """
        Get list of data by criteria

        :param criteria_dict: dictionary
        :return: List of document
        """
        connection = await self.connection_manager.get_connection_async()
        cursor = connection[self.database][self.collection_name].find(criteria_dict)

        result = list()
        async for document in cursor:
            result.append(document)
        return result

    async def delete_data(self, criteria_dict: dict) -> bool:
        """
        Delete document by criteria

        :param criteria_dict: dictionary
        :return: Result of operation
        """
        connection = await self.connection_manager.get_connection_async()
        collection = connection[self.database][self.collection_name]
        result = await collection.delete_many(criteria_dict)
        return result.deleted_count > 0

    async def drop_collection(self, collection_name: str):
        """
        Drop collection by collection name
        """
        connection = await self.connection_manager.get_connection_async()
        await connection[self.database].drop_collection(collection_name)
