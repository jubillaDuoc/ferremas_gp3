import logging
from datetime import datetime, timedelta
from modules.postgres import DBConnection
import json

from models.modelsUsers import TABLA_USERS, TABLA_USERS_COLUMNS, VISTA_USERS, VISTA_USERS_COLUMNS, VISTA_USERS_SECURE_COLUMNS
from models.modelsUsers.modelUserRol import UsersRolModel
from models.modelsUsers.modelUserState import UsersStateModel
from modules.system.crypto_data import decrypt_data
from modules.system.get_config import get_mainKey


# Configuración de logging
logger = logging.getLogger(__name__)


class UsersModel:
    def __init__(self):
        self.idUser = None
        self.nombreUser = None
        self.emailUser = None                   # Nota: Username en la plataforma
        self.passwdUser = None
        self.userRol = UsersRolModel()
        self.userState = UsersStateModel()

    # Getters
    def get_id_user(self):
        return self.idUser

    def get_nombre_user(self):
        return self.nombreUser

    def get_email_user(self):
        return self.emailUser

    def get_passwd_user(self):
        return self.passwdUser

    def get_user_rol(self):
        return self.userRol

    def get_user_state(self):
        return self.userState

    # Setters
    def set_id_user(self, id_user):
        self.idUser = id_user

    def set_nombre_user(self, nombre_user):
        self.nombreUser = nombre_user

    def set_email_user(self, email_user):
        self.emailUser = email_user

    def set_passwd_user(self, passwd_user):
        self.passwdUser = passwd_user

    def set_user_rol(self, user_rol):
        if isinstance(user_rol, UsersRolModel):
            self.userRol = user_rol

    def set_user_state(self, user_state):
        if isinstance(user_state, UsersStateModel):
            self.userState = user_state

    # Obtain specific data methods

    def is_active(self):
        return self.userState.get_id_user_state() == 1
    
    def is_admin(self):
        return self.userRol.get_id_user_rol() == 1
    
    def is_sales(self):
        return self.userRol.get_id_user_rol() == 2
    
    def is_packager(self):
        return self.userRol.get_id_user_rol() == 3
    
    def is_countable(self):
        return self.userRol.get_id_user_rol() == 4
    
    def is_client(self):
        return self.userRol.get_id_user_rol() == 5
    
    def to_json(self):
        return {
            "id_user": self.get_id_user(),
            "nombre_user": self.get_nombre_user(),
            "email_user": self.get_email_user(),
            "id_user_rol": self.get_user_rol().get_id_user_rol(),
            "nombre_user_rol": self.get_user_rol().get_nombre_user_rol(),
            "id_user_state": self.get_user_state().get_id_user_state(),
            "nombre_user_state": self.get_user_state().get_nombre_user_state()
        }

    def to_json_pswd(self):
        return {
            "id_user": self.get_id_user(),
            "nombre_user": self.get_nombre_user(),
            "email_user": self.get_email_user(),
            "passwd_user": self.get_passwd_user(),
            "id_user_rol": self.get_user_rol().get_id_user_rol(),
            "nombre_user_rol": self.get_user_rol().get_nombre_user_rol(),
            "id_user_state": self.get_user_state().get_id_user_state(),
            "nombre_user_state": self.get_user_state().get_nombre_user_state()
        }

    # Métodos de obtencion de datos

    def get_user_by_email(self, email_user):
        """
        Retrieves a user from the database based on their email.

        Args:
            email_user (str): The email of the user.

        Returns:
            User: The User object representing the retrieved user, or None if the user is not found.

        Raises:
            Exception: If there is an error retrieving the user from the database.
        """

        logger.debug(f"Getting user by email {email_user}")

        try:
            # Connect to the database
            logger.debug("Connecting to the database to get user by email")
            db_connection = DBConnection()
            logger.debug("Connected to the database to get user by email")

            # Query the database for the user
            where_definition = "email_user = %s"
            where_data = (email_user,)

            # Execute the query
            result = db_connection.select_query(from_table=VISTA_USERS, select_params=VISTA_USERS_COLUMNS, where_condition=where_definition, where_params=where_data)
            if not result:
                return None

            # Process the query result
            data = result[0]
            self.set_id_user(data['id_user'])
            self.set_nombre_user(data['nombre_user'])
            self.set_email_user(data['email_user'])
            self.set_passwd_user(data['passwd_user'])
            self.userRol.set_id_user_rol(data['id_user_rol'])
            self.userRol.set_nombre_user_rol(data['nombre_user_rol'])
            self.userState.set_id_user_state(data['id_user_state'])
            self.userState.set_nombre_user_state(data['nombre_user_state'])

            return self

        except Exception as e:
            logger.error(f"Error retrieving user by email: {e}")
            return None

    def get_user_by_id(self, id_user):
        """
        Retrieves a user from the database based on their ID.

        Args:
            id_user (int): The ID of the user.

        Returns:
            User: The User object representing the retrieved user, or None if the user is not found.

        Raises:
            Exception: If there is an error retrieving the user from the database.
        """
        
        # Validar entrada
        try:
            id_user = int(id_user)
        except:
            return None
        
        try:
            # Connect to the database
            db_connection = DBConnection()

            # Query the database for the user
            where_definition = "id_user = %s"
            where_data = (id_user,)

            # Execute the query
            result = db_connection.select_query(from_table=VISTA_USERS, select_params=VISTA_USERS_COLUMNS, where_condition=where_definition, where_params=where_data)
            if not result:
                return None

            # Process the query result
            data = result[0]
            self.set_id_user(data['id_user'])
            self.set_nombre_user(data['nombre_user'])
            self.set_email_user(data['email_user'])
            self.set_passwd_user(data['passwd_user'])
            self.userRol.set_id_user_rol(data['id_user_rol'])
            self.userRol.set_nombre_user_rol(data['nombre_user_rol'])
            self.userState.set_id_user_state(data['id_user_state'])
            self.userState.set_nombre_user_state(data['nombre_user_state'])

            return self

        except Exception as e:
            logger.error(f"Error retrieving user by ID: {e}")
            return None
    
    def get_all_users(self):
        """
        Retrieves all users from the database.

        Returns:
            list: A list of User objects representing the retrieved users, or an empty list if no users are found.

        Raises:
            Exception: If there is an error retrieving the users from the database.
        """

        try:
            # Connect to the database
            db_connection = DBConnection()
            
            # Define Function
            order_param = "id_user"
            
            # Query the database for the users
            result = db_connection.select_query(from_table=VISTA_USERS, select_params=VISTA_USERS_SECURE_COLUMNS, order_asc=order_param)
            if not result:
                return []

            return result

        except Exception as e:
            logger.error(f"Error retrieving all users: {e}")
            return None
        
    def get_users_by_rol(self, id_user_rol):
        """
        Retrieves all users from the database based on their role.

        Args:
            id_user_rol (int): The ID of the role.

        Returns:
            list: A list of User objects representing the retrieved users, or an empty list if no users are found.

        Raises:
            Exception: If there is an error retrieving the users from the database.
        """

        try:
            # Connect to the database
            db_connection = DBConnection()

            # Query the database for the users
            where_definition = "id_user_rol = %s"
            where_data = (id_user_rol,)
            
            # Execute the query
            result = db_connection.select_query(from_table=VISTA_USERS, select_params=VISTA_USERS_SECURE_COLUMNS, where_condition=where_definition, where_params=where_data)
            if not result:
                return []

            return result

        except Exception as e:
            logger.error(f"Error retrieving users by role: {e}")
            return None

    def get_users_by_state(self, id_user_state):
        """
        Retrieves all users from the database based on their state.

        Args:
            id_user_state (int): The ID of the state.

        Returns:
            list: A list of User objects representing the retrieved users, or an empty list if no users are found.

        Raises:
            Exception: If there is an error retrieving the users from the database.
        """

        try:
            # Connect to the database
            db_connection = DBConnection()
        
            # Query the database for the users
            where_definition = "id_user_state = %s"
            where_data = (id_user_state,)

            # Execute the query
            result = db_connection.select_query(from_table=VISTA_USERS, select_params=VISTA_USERS_SECURE_COLUMNS, where_condition=where_definition, where_params=where_data)
            if not result:
                return []

            return result

        except Exception as e:
            logger.error(f"Error retrieving users by state: {e}")
            return None

    # Métodos de ABM de Usuarios

    def save_user(self):
        """
        Saves the user in the database.

        Returns:
            User: The User object representing the saved user, or None if the user could not be saved.

        Raises:
            Exception: If there is an error saving the user in the database.
        """

        try:
            # Connect to the database
            db_connection = DBConnection()
            
            # Compose function
            insert_values = [
                self.get_nombre_user(),
                self.get_email_user(),
                self.get_passwd_user(),
                self.get_user_rol().get_id_user_rol(),
                self.get_user_state().get_id_user_state()
                ]
            insert_returning = ["id_user"]
            
            # Insert Query
            result = db_connection.insert_query(table=TABLA_USERS, columns=TABLA_USERS_COLUMNS[1:], values=insert_values, returnData=True, returnColumns=insert_returning)
            
            if not result:
                logger.error(f"Error saving user with email {self.get_email_user()}")
                return None

            # Process the query result
            idUser = result[0][0]

            # Check execution
            if not idUser:
                logger.error(f"Error saving user with email {self.get_email_user()}")
                return None

            if not isinstance(self.get_user_by_id(idUser), UsersModel):
                logger.error(f"Error saving user with ID {idUser}")
                return None

            # Set the ID of the saved user
            self.set_id_user(idUser)
            logger.info(f"User with ID {self.get_id_user()} saved successfully")

            return True

        except Exception as e:
            logger.error(f"Error saving user: {e}")
            return None

    def update_user(self):
        """
        Updates the user in the database.

        Returns:
            User: The User object representing the updated user, or None if the user could not be updated.

        Raises:
            Exception: If there is an error updating the user in the database.
        """

        try:
            # Connect to the database
            db_connection = DBConnection()
            
            # Compose function
            set_columns = TABLA_USERS_COLUMNS[1:]
            set_values = [self.get_nombre_user(), self.get_email_user(), self.get_passwd_user(), self.get_user_rol().get_id_user_rol(), self.get_user_state().get_id_user_state()]
            where_definition = "id_user = %s"
            where_data = (self.get_id_user(),)
            
            # Update Query
            result = db_connection.update_query(table=TABLA_USERS, set_columns=set_columns, set_values=set_values, where_condition=where_definition, where_params=where_data)
            
            if not result:
                logger.error(f"Error updating user with ID {self.get_id_user()}")
                return False

            # Check execution
            if not isinstance(self.get_user_by_id(self.get_id_user()), UsersModel):
                logger.error(f"Error updating user with ID {self.get_id_user()}")
                return False

            logger.info(f"User with ID {self.get_id_user()} updated successfully")

            return True

        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return False

    # Check credentials

    def check_user_credentials(self, email_user, passwd_user):
        """
        Checks the credentials of the user.

        Args:
            email_user (str): The email of the user.
            passwd_user (str): The password of the user.

        Returns:
            User: The User object representing the user, or None if the credentials are invalid.

        Raises:
            Exception: If there is an error checking the credentials of the user.
        """

        logger.debug("Checking user credentials")

        # Validación de entrada
        logger.debug("Validating input data for user credentials")
        if not isinstance(email_user, str) or not isinstance(passwd_user, str):
            return None
        logger.debug("Input data for user credentials validated successfully")

        # Obtener usuario por email
        logger.debug(f"Getting user by email {email_user}")
        user = self.get_user_by_email(email_user)
        if not isinstance(user, UsersModel):
            logger.error(f"User with email {email_user} not found")
            return None
        
        # Desencriptar contraseñas
        passwd_user = decrypt_data(passwd_user, get_mainKey())
        passwd_user_db = decrypt_data(user.get_passwd_user(), get_mainKey())

        # Validar contraseña
        if passwd_user != passwd_user_db and passwd_user is not None and passwd_user_db is not None:
            logger.error(f"Invalid password for user with email {email_user}")
            return None

        logger.info(f"User with email {email_user} authenticated successfully")

        return user.get_id_user()