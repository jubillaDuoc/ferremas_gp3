# # Importar módulos
import psycopg2
import logging
import json

from modules.system.get_config import get_config

class DBConnection:
    """
    Represents a connection to a PostgreSQL database.

    Attributes:
        host (str): The hostname of the database server.
        port (int): The port number of the database server.
        database (str): The name of the database.
        user (str): The username for authentication.
        password (str): The password for authentication.
        connection: The connection object to the database.
        cursor: The cursor object for executing SQL queries.
    """

    def __init__(self):
        """
        Initializes a new instance of the DBConnection class.
        """
        # Obtener la configuración de la base de datos
        config = get_config()
        if config is not None:
            db_config = config['dbpostgresql']
            self.host = db_config['host']
            self.port = db_config['port']
            self.database = db_config['database']
            self.user = db_config['username']
            self.password = db_config['password']
            self.connection = None
            self.cursor = None
        else:
            self.logger.error("Error al obtener la configuración de la base de datos.")
            raise Exception("Error al obtener la configuración de la base de datos.")
        
        # Configurar el logger para esta clase
        self.logger = logging.getLogger(__name__)
        # __name__ dará el nombre del módulo actual, en este caso 'modules.DBConnection'

    def connect(self):
        """
        Connects to the PostgreSQL database.
        """
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            self.logger.debug("Conexión exitosa a la base de datos.")
        except (Exception, psycopg2.Error) as error:
            self.logger.error("Error al conectar a la base de datos: %s", error)
    
    def disconnect(self):
        """
        Disconnects from the PostgreSQL database.

        This method closes the cursor and the database connection.
        """
        if self.connection:
            self.cursor.close()
            self.connection.close()
            self.logger.debug("Conexión cerrada.")
    
    def execute_query(self, query, params=None, to_json=False):
        """
        Executes a query on the PostgreSQL database.
        
        Args:
            query (str): The SQL query to execute.
            params (tuple): The parameters to pass to the query.
            
        Returns:
            The result of the query as a JSON string.
        """
        
        if not isinstance(to_json, bool):
            self.logger.error("El parámetro 'to_json' debe ser un booleano.")
            return False
        
        try:
            if to_json:
                self.connect()
                query = f"SELECT json_agg(t) FROM ({query}) t"
                self.cursor.execute(query)
                # Get data from the query as a list of tuples
                result = self.cursor.fetchall()
                self.connection.commit()
                self.disconnect()
                # Get list of tuple
                result = result[0][0]
                return result
            else:
                self.connect()
                self.logger.debug(f"Consulta: {query} | {params}")
                self.cursor.execute(query, params)
                result = self.cursor.fetchall()
                self.connection.commit()
                self.disconnect()
                return result
        except (Exception, psycopg2.Error) as error:
            self.disconnect()
            self.logger.error("Error al ejecutar la consulta: %s", error)
            return False

    def execute_commit_query(self, query, params=None):
            """
            Executes a query and commits the changes to the database.

            Args:
                query (str): The SQL query to execute.
                params (tuple, optional): The parameters to pass to the query (default: None).

            Returns:
                bool: True if the query was executed successfully and changes were committed, False otherwise.
            """
            try:
                self.connect()
                self.logger.debug(f"Consulta: {query} | {params}")
                self.cursor.execute(query, params)
                dataRetrived = False
                try:
                    result = self.cursor.fetchall()
                    dataRetrived = True
                except:
                    result = True
                self.connection.commit()
                self.disconnect()
                self.logger.info("Consulta ejecutada con éxito.")
                
                return result
            except (Exception, psycopg2.Error) as error:
                self.disconnect()
                self.logger.error("Error al ejecutar la consulta commit: %s", error)
                return False
    
    def select_query(self, *, select_params="*", from_table, where_condition=None, order_desc=None, order_asc=None, limit=None, group_by=None, having=None, where_params=None, to_json=True):
        """
        Sends a SELECT query to the database.

        Args:
            select_params (str, optional): The columns to select (default: "*").
            from_table (str): The table to select from.
            where_params (str, optional): The WHERE clause parameters (default: None).
            order_by (str, optional): The ORDER BY clause (default: None).
            limit (int, optional): The LIMIT clause (default: None).
            group_by (str, optional): The GROUP BY clause (default: None).
            having (str, optional): The HAVING clause (default: None).
            to_json (bool, optional): Whether to return the result as a JSON string (default: True).

        Returns:
            The result of the query as a JSON string.
        """
        
        # Validate the parameters
        if not from_table:
            self.logger.error("No se ha especificado la tabla de la consulta.")
            return False
        if select_params != "*" and not select_params:
            self.logger.error("No se han especificado los parámetros de selección.")
            return False
        if select_params != "*":
            try:
                select_params = ", ".join(select_params)
            except:
                self.logger.error("Error al convertir los parámetros de selección en una cadena.")
                return False
        if where_condition and not isinstance(where_condition, str):
            self.logger.error("Los parámetros de la cláusula WHERE deben ser una cadena.")
            return False
        if where_params and not isinstance(where_params, tuple):
            self.logger.error("Los parámetros de la cláusula WHERE deben ser una tupla.")
            return False
        if order_desc and not isinstance(order_desc, str):
            self.logger.error("Los parámetros de la cláusula ORDER DESC deben ser una cadena.")
            return False
        if order_asc and not isinstance(order_asc, str):
            self.logger.error("Los parámetros de la cláusula ORDER ASC deben ser una cadena.")
            return False
        if limit and not isinstance(limit, int):
            self.logger.error("El parámetro de la cláusula LIMIT debe ser un entero.")
            return False
        if group_by and not isinstance(group_by, str):
            self.logger.error("Los parámetros de la cláusula GROUP BY deben ser una cadena.")
            return False
        if having and not isinstance(having, str):
            self.logger.error("Los parámetros de la cláusula HAVING deben ser una cadena.")
            return False
        if not isinstance(to_json, bool):
            self.logger.error("El parámetro 'to_json' debe ser un booleano.")
            return False
        
        if order_asc and order_desc:
            self.logger.error("No se pueden especificar ambas cláusulas ORDER ASC y ORDER DESC.")
            return False
        
        # Build where sentence
        if where_condition and where_params:
            where_params = tuple(f"'{param}'" for param in where_params)
            where_condition = where_condition % where_params
        else:
            where_condition = None
        
        try:
            # Build the query
            query = f"SELECT {select_params} FROM {from_table}"
            if where_condition:
                query += f" WHERE {where_condition}"
            if group_by:
                query += f" GROUP BY {group_by}"
            if having:
                query += f" HAVING {having}"
            if order_asc:
                query += f" ORDER BY {order_asc} ASC"
            if order_desc:
                query += f" ORDER BY {order_desc} DESC"
            if limit:
                query += f" LIMIT {limit}"
            
            self.logger.debug(f"Query: {query}")
            
            # Execute the query and return the result as a JSON string or a list of tuples
            if to_json:
                self.connect()
                query = f"SELECT json_agg(t) FROM ({query}) t"
                self.cursor.execute(query)
                # Get data from the query as a list of tuples
                result = self.cursor.fetchall()
                self.disconnect()
                # Get list of tuple
                result = result[0][0]
                return result
            else:
                self.connect()
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                self.disconnect()
                return result
        except (Exception, psycopg2.Error) as error:
            self.logger.error("Error al ejecutar la consulta: %s", error)
            self.disconnect()
            return False
    
    def insert_query(self, *, table, columns, values, returnData=False, returnColumns=None):
        """
        Sends an INSERT query to the database.

        Args:
            table (str): The table to insert into.
            columns (list): The columns to insert into.
            values (list): The values to insert.
            returnData (bool, optional): Whether to return the inserted data (default: False).
            returnColumns (list, optional): The columns to return (default: None).

        Returns:
            The inserted data as a JSON string.
        """
        
        # Validate the parameters
        if not table:
            self.logger.error("No se ha especificado la tabla de la consulta.")
            return False
        if not columns:
            self.logger.error("No se han especificado las columnas de la consulta.")
            return False
        if not values:
            self.logger.error("No se han especificado los valores de la consulta.")
            return False
        if not isinstance(columns, list):
            self.logger.error("Las columnas deben ser una lista.")
            return False
        if not isinstance(values, list):
            self.logger.error("Los valores deben ser una lista.")
            return False
        if returnColumns and not isinstance(returnColumns, list):
            self.logger.error("Las columnas de retorno deben ser una lista.")
            return False
        if not isinstance(returnData, bool):
            self.logger.error("El parámetro 'returnData' debe ser un booleano.")
            return False
        
        try:
            # Build the query
            columns = ", ".join(columns)
            values = ", ".join([f"'{value}'" for value in values])
            query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
            if returnData:
                if returnColumns:
                    returnColumns = ", ".join(returnColumns)
                    query += f" RETURNING {returnColumns}"
            
            self.logger.debug(f"Query: {query}")
            
            # Execute the query and return the inserted data as a JSON string
            self.connect()
            self.cursor.execute(query)
            if returnData:
                result = self.cursor.fetchall()
            else:
                result = True

            self.connection.commit()
            self.disconnect()
            return result
        except (Exception, psycopg2.Error) as error:
            self.logger.error("Error al ejecutar la consulta: %s", error)
            self.disconnect()
            return False
        
    def update_query(self, *, table, set_columns, set_values, where_condition=None, where_params=None, returnData=False, returnColumns=None):
        """
        Sends an UPDATE query to the database.

        Args:
            table (str): The table to update.
            set_columns (list): The columns to update.
            set_values (list): The values to set.
            where_condition (str): The WHERE clause.
            where_params (list, optional): The parameters for the WHERE clause (default: None).
            returnData (bool, optional): Whether to return the updated data (default: False).
            returnColumns (list, optional): The columns to return (default: None).

        Returns:
            The updated data as a JSON string.
        """
        
        # Validate the parameters
        if not table:
            self.logger.error("No se ha especificado la tabla de la consulta.")
            return False
        if not set_columns:
            self.logger.error("No se han especificado las columnas de la consulta.")
            return False
        if not set_values:
            self.logger.error("No se han especificado los valores de la consulta.")
            return False
        if where_condition and not isinstance(where_condition, str):
            self.logger.error("Los parámetros de la cláusula WHERE deben ser una cadena.")
            return False
        if where_params and not isinstance(where_params, tuple):
            self.logger.error("Los parámetros de la cláusula WHERE deben ser una tupla.")
            return False
        if not isinstance(set_columns, list):
            self.logger.error("Las columnas deben ser una lista.")
            return False
        if not isinstance(set_values, list):
            self.logger.error(f"Los valores deben ser una lista. {set_values}")
            return False
        if returnColumns and not isinstance(returnColumns, list):
            self.logger.error("Las columnas de retorno deben ser una lista.")
            return False
        if not isinstance(returnData, bool):
            self.logger.error("El parámetro 'returnData' debe ser un booleano.")
            return False
        
        # Build where sentence
        if where_condition and where_params:
            where_params = tuple(f"'{param}'" for param in where_params)
            where_condition = where_condition % where_params
        else:
            where_condition = None
        
        try:
            # Build the query
            set_values = [f"'{value}'" for value in set_values]
            set_values = ", ".join([f"{column} = {value}" for column, value in zip(set_columns, set_values)])
            query = f"UPDATE {table} SET {set_values} WHERE {where_condition}"
            if returnData:
                if returnColumns:
                    returnColumns = ", ".join(returnColumns)
                    query += f" RETURNING {returnColumns}"
            
            self.logger.debug(f"Query: {query}")
            
            # Execute the query and return the updated data as a JSON string
            self.connect()
            self.cursor.execute(query)
            if returnData:
                result = self.cursor.fetchall()
            else:
                result = True
                
            self.connection.commit()
            self.disconnect()
            return result
        except (Exception, psycopg2.Error) as error:
            self.logger.error("Error al ejecutar la consulta: %s", error)
            self.disconnect()
            return False
        