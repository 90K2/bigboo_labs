

def es_paginator(es, index_name, query):
    """
    Iterate over all search result and yield each record

    :param es: <elasticsearch.client.Elasticsearch>
    :param index_name: <str> logstash index name
    :param query: <dict> elasticsearch dsl query (https://elasticsearch-dsl.readthedocs.io/en/latest/)
    :return: yield dict record
    """

    search_result = es.search(index=index_name, body=query)

    if search_result["hits"]["hits"]:
        paginator = 0

        while paginator < search_result["hits"]["total"]:
            search_result = es.search(index=index_name, body=query, from_=paginator)
            match = search_result["hits"]["hits"]
            paginator += 10
            for record in match:
                yield record
