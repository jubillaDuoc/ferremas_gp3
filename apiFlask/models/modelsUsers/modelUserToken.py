import logging
from datetime import datetime, timedelta
from modules.postgres import DBConnection
import json

from models.modelsUsers import TABLA_USERS_TOKEN, TABLA_USERS_TOKEN_COLUMNS
from models.modelsUsers.modelUser import UsersModel
from modules.system.generate_token import generate_token
from modules.system.crypto_data import decrypt_data, encrypt_data
from modules.system.get_config import get_mainKey

# Configuración de logging
logger = logging.getLogger(__name__)


class UsersTokenModel():
    def __init__(self):
        self.user = UsersModel()

    # Getters

    def get_user(self):
        return self.user

    # Setters

    def set_user(self, user):
        if isinstance(user, UsersModel):
            self.user = user

    # Methods

    def create_user_token(self, id_user):
        """
        Creates a new user token in the database.

        Args:
            id_user (int): The ID of the user.

        Returns:
            UserToken: The UserToken object representing the new user token, or False if the user token could not be created.

        Raises:
            Exception: If there is an error creating the user token in the database.
        """

        # Validación de entrada
        if not isinstance(id_user, int):
            return False
        if not isinstance(UsersModel().get_user_by_id(id_user), UsersModel):
            return False

        try:
            # Set User on Token Object
            self.set_user(UsersModel().get_user_by_id(id_user))

            # Get parameters to create token
            userId = self.get_user().get_id_user()
            userRole = self.get_user().get_user_rol().get_nombre_user_rol()
            userState = self.get_user().get_user_state().get_nombre_user_state()
            userPasswd = self.get_user().get_passwd_user()

            check_token, token = generate_token()
            if not check_token:
                return False
            check_token, token = generate_token(seed=encrypt_data(token, get_mainKey()))
            if not check_token:
                return False

            created_at = datetime.now()
            valid_from = created_at
            valid_to = valid_from + timedelta(minutes=10)
            
            # Compose Function
            insert_values = [
                token,
                created_at,
                valid_from,
                valid_to,
                userId
            ]
            insert_returning = "token_session"
            
            # Insert Query
            db_connection = DBConnection()
            logger.debug(f"Creating new user token for user with ID {userId}")
            result = db_connection.insert_query(table=TABLA_USERS_TOKEN, columns=TABLA_USERS_TOKEN_COLUMNS, values=insert_values, returnData=True, returnColumns=[insert_returning])
            if not result:
                return False

            # Process the query result
            tokenSession = result[0][0]
            if tokenSession != token:
                logger.error(f"Error creating new user token for user with ID {userId}")
                return False

            logger.info(f"User token created successfully for user with ID {userId}")

            data_for_real_token = {
                'token': token,
                'role': userRole,
                'state': userState,
                'passwd': userPasswd
            }

            encrypt_real_token = encrypt_data(data_for_real_token, get_mainKey())
            if not encrypt_real_token:
                logger.error(f"Error creating new user token for user with ID {userId}")
                return False

            logger.info(f"User token created successfully for user with ID {userId}")
            return encrypt_real_token

        except Exception as e:
            logger.error(f"Error creating new user token: {e}")
            return False

    def check_user_token(self, token):
        """
        Checks the validity of the user token.

        Args:
            token (str): The token to be checked.

        Returns:
            bool: True if the token is valid, False otherwise.

        Raises:
            Exception: If there is an error checking the user token.
        """

        # Validación de entrada
        if not isinstance(token, str):
            return False

        try:
            # Decrypt token
            token = decrypt_data(token, get_mainKey())
            if not token:
                return False

            token_request = json.loads(token)

            token = token_request['token']
            userRole = token_request['role']
            userState = token_request['state']
            userPasswd = token_request['passwd']

            actual_date = datetime.now()

            # Connect to the database
            db_connection = DBConnection()

            # Query the database for the users
            where_definition = "token_session = %s"
            where_data = (token,)
            
            # Execute the query
            result = db_connection.select_query(from_table=TABLA_USERS_TOKEN, select_params=TABLA_USERS_TOKEN_COLUMNS, where_condition=where_definition, where_params=where_data)
            if not result:
                return False

            data = result[0]
            if not data:
                return False
            
            token_valid_to = data['valid_to_session']
            
            # Convert token_valid_to to a date
            token_valid_to = datetime.strptime(token_valid_to, '%Y-%m-%dT%H:%M:%S.%f')
            
            logger.debug(f"Checking user token")
            
            if actual_date >= token_valid_to:
                logger.error(f"User token expired")
                return False

            # Validar rol, estado y contraseña
            user = UsersModel().get_user_by_id(data['id_user'])
            if not isinstance(user, UsersModel):
                return False

            if user.get_user_rol().get_nombre_user_rol() != userRole:
                return False
            if user.get_user_state().get_nombre_user_state() != userState:
                return False
            if user.check_user_credentials(user.get_email_user(), userPasswd) is None:
                return False

            logger.info(f"User token checked successfully")
            return True

        except Exception as e:
            logger.error(f"Error checking user token: {e}")
            return False

    def refresh_user_token(self, token):
        """
        Refreshes the user token.

        Args:
            token (str): The user token to be refreshed.

        Returns:
            bool: True if the token was refreshed successfully, False otherwise.
        """

        # Validación de entrada
        if not isinstance(token, str):
            return False

        try:
            # Validar Token
            if not self.check_user_token(token):
                return False

            # Decrypt token
            token = decrypt_data(token, get_mainKey())
            if not token:
                return False

            token_request = json.loads(token)

            token_only = token_request['token']
            actual_date = datetime.now()
            valid_to = actual_date + timedelta(minutes=10)

            db_connection = DBConnection()
            
            set_columns = ["valid_to_session"]
            set_values = [valid_to]
            where_definition = "token_session = %s"
            where_data = (token_only,)
            
            # Update Query
            logger.debug(f"Refreshing user token")
            result = db_connection.update_query(table=TABLA_USERS_TOKEN, set_columns=set_columns, set_values=set_values, where_condition=where_definition, where_params=where_data)
            
            if not result:
                return False

            logger.info(f"User token refreshed successfully")
            return True

        except Exception as e:
            logger.error(f"Error refreshing user token: {e}")
            return False
    
    def check_admin_token(self, token):
        """
        Checks the validity of the admin token.

        Args:
            token (str): The token to be checked.

        Returns:
            bool: True if the token is valid, False otherwise.

        Raises:
            Exception: If there is an error checking the admin token.
        """

        # Validación de entrada
        if not isinstance(token, str):
            return False

        try:
            # Decrypt token
            token = decrypt_data(token, get_mainKey())
            if not token:
                return False

            token_request = json.loads(token)

            token = token_request['token']
            userRole = token_request['role']
            userState = token_request['state']
            userPasswd = token_request['passwd']

            actual_date = datetime.now()

            # Connect to the database
            db_connection = DBConnection()

            # Query the database for the users
            where_definition = "token_session = %s"
            where_data = (token,)
            
            # Execute the query
            result = db_connection.select_query(from_table=TABLA_USERS_TOKEN, select_params=TABLA_USERS_TOKEN_COLUMNS, where_condition=where_definition, where_params=where_data)
            if not result:
                return False

            data = result[0]
            if not data:
                return False
            
            token_valid_to = data['valid_to_session']
            
            # Convert token_valid_to to a date
            token_valid_to = datetime.strptime(token_valid_to, '%Y-%m-%dT%H:%M:%S.%f')
            
            logger.debug(f"Checking admin token")
            
            if actual_date >= token_valid_to:
                logger.error(f"Admin token expired")
                return False

            # Validar rol, estado y contraseña
            user = UsersModel().get_user_by_id(data['id_user'])
            if not isinstance(user, UsersModel):
                return False

            if user.get_user_rol().get_nombre_user_rol() != userRole:
                return False
            if user.get_user_state().get_nombre_user_state() != userState:
                return False
            if user.check_user_credentials(user.get_email_user(), userPasswd) is None:
                return False
            
            if not user.is_admin():
                return False

            logger.info(f"Admin token checked successfully")
            return True

        except Exception as e:
            logger.error(f"Error checking admin token: {e}")
            return False
    
    def refresh_admin_token(self, token):
        """
        Refreshes the admin token.

        Args:
            token (str): The admin token to be refreshed.

        Returns:
            bool: True if the token was refreshed successfully, False otherwise.
        """

        # Validación de entrada
        if not isinstance(token, str):
            return False

        try:
            # Validar Token
            if not self.check_admin_token(token):
                return False

            # Decrypt token
            token = decrypt_data(token, get_mainKey())
            if not token:
                return False

            token_request = json.loads(token)

            token_only = token_request['token']
            actual_date = datetime.now()
            valid_to = actual_date + timedelta(minutes=10)

            db_connection = DBConnection()
            
            set_columns = ["valid_to_session"]
            set_values = [valid_to]
            where_definition = "token_session = %s"
            where_data = (token_only,)
            
            # Update Query
            logger.debug(f"Refreshing admin token")
            result = db_connection.update_query(table=TABLA_USERS_TOKEN, set_columns=set_columns, set_values=set_values, where_condition=where_definition, where_params=where_data)
            
            if not result:
                return False

            logger.info(f"Admin token refreshed successfully")
            return True

        except Exception as e:
            logger.error(f"Error refreshing admin token: {e}")
            return False