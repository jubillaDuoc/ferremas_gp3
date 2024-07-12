import logging
from datetime import datetime, timedelta
from modules.postgres import DBConnection
import json

from models.modelsUsers import TABLA_USERS_ROLE, TABLA_USERS_ROLE_COLUMNS

# Configuración de logging
logger = logging.getLogger(__name__)


class UsersRolModel():
    def __init__(self):
        self.idUserRol = None
        self.nombreUserRol = None

    # Getters
    def get_id_user_rol(self):
        return self.idUserRol

    def get_nombre_user_rol(self):
        return self.nombreUserRol

    # Setters
    def set_id_user_rol(self, id_user_rol):
        # Validar entrada
        if not isinstance(id_user_rol, int):
            raise ValueError("El ID del rol de usuario debe ser un número entero.")
        self.idUserRol = id_user_rol
        

    def set_nombre_user_rol(self, nombre_user_rol):
        self.nombreUserRol = nombre_user_rol

    # Obtain methods

    def to_json(self):
        return {
            "id_user_rol": self.get_id_user_rol(),
            "nombre_user_rol": self.get_nombre_user_rol()
        }

    # Métodos

    def get_user_rol_by_id(self, id_user_rol):
        """
        Retrieves a user role from the database based on its ID.

        Args:
            id_user_rol (int): The ID of the user role.

        Returns:
            UserRol: The UserRol object representing the retrieved user role, or None if the user role is not found.

        Raises:
            Exception: If there is an error retrieving the user role from the database.
        """

        try:
            # Connect to the database
            db_connection = DBConnection()

            # Query the database for the user role
            where_definition = "id_user_rol = %s"
            where_data = (id_user_rol,)
            result = db_connection.select_query(from_table=TABLA_USERS_ROLE, select_params=TABLA_USERS_ROLE_COLUMNS, where_condition=where_definition, where_params=where_data)
            if not result:
                return None

            # Process the query result
            data = result[0]
            self.set_id_user_rol(data['id_user_rol'])
            self.set_nombre_user_rol(data['nombre_user_rol'])

            return self

        except Exception as e:
            logger.error(f"Error retrieving user role by ID: {e}")
            return None

    def get_user_rol_by_name(self, nombre_user_rol):
        """
        Retrieves a user role from the database based on its name.

        Args:
            nombre_user_rol (str): The name of the user role.

        Returns:
            UserRol: The UserRol object representing the retrieved user role, or None if the user role is not found.

        Raises:
            Exception: If there is an error retrieving the user role from the database.
        """

        try:
            # Connect to the database
            db_connection = DBConnection()

            # Query the database for the user role
            where_definition = "nombre_user_rol = %s"
            where_data = (nombre_user_rol,)
            result = db_connection.select_query(from_table=TABLA_USERS_ROLE, select_params=TABLA_USERS_ROLE_COLUMNS, where_condition=where_definition, where_params=where_data)
            if not result:
                return None

            # Process the query result
            data = result[0]
            self.set_id_user_rol(data['id_user_rol'])
            self.set_nombre_user_rol(data['nombre_user_rol'])

            return self

        except Exception as e:
            logger.error(f"Error retrieving user role by name: {e}")
            return None
    
    def get_all_user_roles(self):
        """
        Retrieves all user roles from the database.

        Returns:
            list: A list of UserRol objects representing the retrieved user roles, or an empty list if no user roles are found.

        Raises:
            Exception: If there is an error retrieving the user roles from the database.
        """

        try:
            # Connect to the database
            db_connection = DBConnection()

            # Query the database for the user roles
            result = db_connection.select_query(from_table=TABLA_USERS_ROLE)
            if not result:
                return []

            return result

        except Exception as e:
            logger.error(f"Error retrieving all user roles: {e}")
            return []