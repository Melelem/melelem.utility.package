from ._base import ServiceRequestSession


class DocumentsService(ServiceRequestSession):
    name = 'soffos-service-documents'

    def ingest_document(
        self,
        text: str,
        client_id: str,
        document_id: str,
        name: str,
        meta: dict = None,
        chunk_word_length: int = None,
        sent_overlap: int = 1 
    ):
        """Pre-processes document and stores it to Elasticsearch.

        Args:
            text (str): Document text.
            client_id (str): Client's ID.
            document_id (str): Document's ID. Client must keep track of this ID.
            name (str): Document's name.
            meta (dict, optional): Dictionary with any metadata we wish to tag the document with. Defaults to None.
            chunk_word_length (int, optional): Specify how many words per passage when splitting the document to passages. Defaults to None. Service defaults to 100.
            sent_overlap (int, optional): Specify how many sentences should overlap between adjacent passages. Defaults to 1.

        Returns:
            _type_: json
            success (bool): Whether the task succeeded.
        """
        json = {
            "text": text,
            "client_id": client_id,
            "document_id": document_id,
            "name": name
        }
        if meta:
            json["meta"] = meta
        if chunk_word_length:
            json["chunk_word_length"] = chunk_word_length
        if sent_overlap:
            json["sent_overlap"] = sent_overlap

        return self.request(json=json, path="document/ingest")
