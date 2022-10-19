"""
Copyright (c)2022 - Soffos.ai - All rights reserved
Created at: 2022-05-28
Purpose: Base classes for services
"""

import logging

# pylint: disable=no-name-in-module
from pydantic import BaseModel as Model
from pydantic import Field, ValidationError, validator


class Service:
    """
    Base super class for every Soffos microservice.
    """

    # NOTE: Singelton pattern. Only create and initialize one instance per child class.
    #   Class variables are created per child class that inherits this base class. Therefore, a
    #   single instance will be allowed for each class that inherits this base class.
    _instance = None
    _was_initialized = False

    class Data:
        pass

    def __new__(cls):
        # Singelton pattern. Only create one instance.
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initializes the microservice
        """
        # Singelton pattern. Only initialize instance once.
        if self._was_initialized:
            return
        self._was_initialized = True

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

    def validate(self, **data):
        return self.Data(**data)

    def run(self, data: Data):
        raise NotImplementedError()

    def serve(self, **data):
        validated_data = self.validate(**data)
        return self.run(validated_data)
