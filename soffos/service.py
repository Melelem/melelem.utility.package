"""
Copyright (c)2022 - Soffos.ai - All rights reserved
Created at: 2022-05-28
Purpose: Base classes for services
"""
import logging
import typing as t
from abc import abstractmethod

ServiceResponse = t.Optional[t.Tuple[t.Dict[str, t.Any], ...]]
ServiceRequestData = t.List[t.Dict[str, t.Any]]

class Service:
    """
    Base super class for every Soffos microservice.
    """

    def __init__(self):
        """
        Initializes the microservice
        """
        logging.info('Initializing service. %s', self.__class__.__name__)
        self.initialize()
        logging.info('Service %s successfully initialized',
                     self.__class__.__name__)

    def initialize(self):
        """
        Initializes service, by loading whatever it needs to load into memory.

        Note
        ----

        This is called when the service is loaded. It is expected to be called
        only once during microservice life-cycle.
        """
        pass

    def validate(self, request_data: ServiceRequestData):
        """
        Abstract method. Validates the provided request.

        Parameters
        -----------

        - request_data: Request data being validated

        Note
        ----

        If provided request is invalid, this should raise an exception.
        """
        pass

    @abstractmethod
    def run(self, request_data: ServiceRequestData) -> ServiceResponse:
        """
        Serves the request.

        Parameters
        ----------

        - request_data: Request data to be used for servicing the request.
        """
