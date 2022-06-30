"""
Copyright (c)2022 - Soffos.ai - All rights reserved
Created at: 2022-05-28
Purpose: Base classes for services
"""

import logging

# pylint: disable=unused-import,no-name-in-module
from pydantic import BaseModel as DataModel
from pydantic import Field as DataField
from pydantic import ValidationError as DataValidationError


class Service:
    """
    Base super class for every Soffos microservice.

    Notes
    -----

    For Celery services, remember to change "name" property to something that is
    adequate for celery. 
    """

    name: str = 'ServiceName'

    class Data:
        pass

    def __init__(self):
        """
        Initializes the microservice
        """
        logging.info('Initializing service: %s.', self.__class__.__name__)
        self.initialize()
        logging.info('Successfully initialized service: %s.', self.__class__.__name__)

    def initialize(self):
        """
        Initializes service, by loading whatever it needs to load into memory.

        Note
        ----

        This is called when the service is loaded. It is expected to be called
        only once during microservice life-cycle.
        """
        pass

    def validate(self, **kwargs):
        return self.Data(**kwargs)

    def run(self, data: Data):
        raise NotImplementedError()

    def serve(self, **kwargs):
        data = self.validate(**kwargs)
        return self.run(data)
