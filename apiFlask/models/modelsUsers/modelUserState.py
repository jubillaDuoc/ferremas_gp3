import logging
from datetime import datetime, timedelta
from modules.postgres import DBConnection
import json

from models.modelsUsers import TABLA_USERS_STATE, TABLA_USERS_STATE_COLUMNS

# Configuración de logging
logger = logging.getLogger(__name__)


class UsersStateModel():
    def __init__(self):
        self.idUserState = None
        self.nombreUserState = None

    # Getters
    def get_id_user_state(self):
        return self.idUserState

    def get_nombre_user_state(self):
        return self.nombreUserState

    # Setters
    def set_id_user_state(self, id_user_state):
        self.idUserState = id_user_state

    def set_nombre_user_state(self, nombre_user_state):
        self.nombreUserState = nombre_user_state

    # Obtain methods

    def to_json(self):
        return {
            "id_user_state": self.get_id_user_state(),
            "nombre_user_state": self.get_nombre_user_state()
        }

    # Métodos
    
    def get_all_user_states(self):
        """
        Retrieves all user states from the database.

        Returns:
            list: A list of UserState objects representing all user states in the database.

        Raises:
            Exception: If there is an error retrieving the user states from the database.
        """

        try:
            # Connect to the database
            db_connection = DBConnection()

            # Query the database for all user states
            result = db_connection.select_query(from_table=TABLA_USERS_STATE)
            if not result:
                return []

            return result
        except Exception as e:
            logger.error(f"Error retrieving all user states: {e}")
            return
    
    def get_user_state_by_id(self, id_user_state):
        """
        Retrieves a user state from the database based on its ID.

        Args:
            id_user_state (int): The ID of the user state.

        Returns:
            UserState: The UserState object representing the retrieved user state, or None if the user state is not found.

        Raises:
            Exception: If there is an error retrieving the user state from the database.
        """

        try:
            # Connect to the database
            db_connection = DBConnection()

            # Query the database for the user role
            where_definition = "id_user_state = %s"
            where_data = (id_user_state,)
            result = db_connection.select_query(from_table=TABLA_USERS_STATE, select_params=TABLA_USERS_STATE_COLUMNS, where_condition=where_definition, where_params=where_data)
            if not result:
                return None

            # Process the query result
            data = result[0]
            self.set_id_user_state(data['id_user_state'])
            self.set_nombre_user_state(data['nombre_user_state'])

            return self
        except Exception as e:
            logger.error(f"Error retrieving user state by ID: {e}")
            return None

    def get_user_state_by_name(self, nombre_user_state):
        """
        Retrieves a user state from the database based on its name.

        Args:
            nombre_user_state (str): The name of the user state.

        Returns:
            UserState: The UserState object representing the retrieved user state, or None if the user state is not found.

        Raises:
            Exception: If there is an error retrieving the user state from the database.
        """

        try:
            # Connect to the database
            db_connection = DBConnection()

            # Query the database for the user role
            where_definition = "nombre_user_state = %s"
            where_data = (nombre_user_state,)
            result = db_connection.select_query(from_table=TABLA_USERS_STATE, select_params=TABLA_USERS_STATE_COLUMNS, where_condition=where_definition, where_params=where_data)
            if not result:
                return None

            # Process the query result
            data = result[0]
            self.set_id_user_state(data['id_user_state'])
            self.set_nombre_user_state(data['nombre_user_state'])

            return self
        except Exception as e:
            logger.error(f"Error retrieving user state by name: {e}")
            return None