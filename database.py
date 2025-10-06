import aiomysql
import asyncio
import json
from typing import Dict, List, Optional
import config
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.pool = None
        self.connection_params = self._parse_database_url()
    
    def _parse_database_url(self):
        url = config.DATABASE_URL
        if not url:
            raise ValueError("DATABASE_URL not found in config")
                
        url = url.replace('mysql://', '')
        auth_host, database = url.split('/')
        auth, host_port = auth_host.split('@')
        user, password = auth.split(':')
        
        import urllib.parse
        password = urllib.parse.unquote(password)
        
        if ':' in host_port:
            host, port = host_port.split(':')
            port = int(port)
        else:
            host = host_port
            port = 3306
        
        return {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'db': database,
            'autocommit': True,
            'charset': 'utf8mb4'
        }
    
    async def connect(self):
        try:
            self.connection_params['connect_timeout'] = 10
            self.connection_params['minsize'] = 1
            self.connection_params['maxsize'] = 5
            
            self.pool = await aiomysql.create_pool(**self.connection_params)
            await self.create_tables()
            logger.info("MySQL connection pool created")
        except Exception as e:
            logger.error(f"Failed to connect to MySQL: {e}")
            raise
    
    async def create_tables(self):
        create_servers_table = """
        CREATE TABLE IF NOT EXISTS servers (
            guild_id BIGINT PRIMARY KEY,
            activated BOOLEAN DEFAULT FALSE,
            cmd_channel_id BIGINT,
            locked BOOLEAN DEFAULT FALSE,  
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        create_packages_table = """
        CREATE TABLE IF NOT EXISTS installed_packages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            guild_id BIGINT NOT NULL,
            package_name VARCHAR(255) NOT NULL,
            installed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY unique_guild_package (guild_id, package_name),
            INDEX idx_guild_id (guild_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        import warnings
        import aiomysql
        
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=aiomysql.Warning)
                    await cursor.execute(create_servers_table)
                    await cursor.execute(create_packages_table)
                    
                try:
                    await cursor.execute("""
                        ALTER TABLE installed_packages 
                        ADD CONSTRAINT fk_guild_id 
                        FOREIGN KEY (guild_id) REFERENCES servers(guild_id) ON DELETE CASCADE
                    """)
                except:
                    pass
                    
                logger.info("Database tables created/verified")
    
    async def close(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            logger.info("MySQL connection pool closed")
    
    async def is_server_activated(self, guild_id: int) -> bool:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "SELECT activated FROM servers WHERE guild_id = %s",
                    (guild_id,)
                )
                result = await cursor.fetchone()
                return result[0] if result else False
    
    async def activate_server(self, guild_id: int, cmd_channel_id: int):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("""
                    INSERT INTO servers (guild_id, activated, cmd_channel_id, locked)
                    VALUES (%s, TRUE, %s, FALSE)
                    ON DUPLICATE KEY UPDATE
                    activated = TRUE, cmd_channel_id = %s, updated_at = CURRENT_TIMESTAMP
                """, (guild_id, cmd_channel_id, cmd_channel_id))
                logger.info(f"Server {guild_id} activated")
    
    async def is_server_locked(self, guild_id: int) -> bool:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "SELECT locked FROM servers WHERE guild_id = %s",
                    (guild_id,)
                )
                result = await cursor.fetchone()
                return result[0] if result else False
    
    async def lock_server(self, guild_id: int):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("""
                    UPDATE servers SET locked = TRUE, updated_at = CURRENT_TIMESTAMP
                    WHERE guild_id = %s
                """, (guild_id,))
                logger.info(f"Server {guild_id} locked")
    
    async def get_cmd_channel_id(self, guild_id: int) -> Optional[int]:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "SELECT cmd_channel_id FROM servers WHERE guild_id = %s",
                    (guild_id,)
                )
                result = await cursor.fetchone()
                return result[0] if result else None
    
    async def install_package(self, guild_id: int, package_name: str) -> bool:
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("""
                        INSERT INTO installed_packages (guild_id, package_name)
                        VALUES (%s, %s)
                    """, (guild_id, package_name))
                    logger.info(f"Package {package_name} installed on server {guild_id}")
                    return True
        except aiomysql.IntegrityError:
            logger.warning(f"Package {package_name} already installed on server {guild_id}")
            return False
    
    async def is_package_installed(self, guild_id: int, package_name: str) -> bool:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("""
                    SELECT 1 FROM installed_packages 
                    WHERE guild_id = %s AND package_name = %s
                """, (guild_id, package_name))
                result = await cursor.fetchone()
                return result is not None
    
    async def get_installed_packages(self, guild_id: int) -> List[str]:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("""
                    SELECT package_name FROM installed_packages 
                    WHERE guild_id = %s ORDER BY installed_at
                """, (guild_id,))
                results = await cursor.fetchall()
                return [row[0] for row in results]
    
    async def get_package_count(self, guild_id: int) -> int:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("""
                    SELECT COUNT(*) FROM installed_packages WHERE guild_id = %s
                """, (guild_id,))
                result = await cursor.fetchone()
                return result[0] if result else 0
    
    async def remove_package(self, guild_id: int, package_name: str) -> bool:
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("""
                        DELETE FROM installed_packages 
                        WHERE guild_id = %s AND package_name = %s
                    """, (guild_id, package_name))
                    
                    if cursor.rowcount > 0:
                        logger.info(f"Package {package_name} removed from server {guild_id}")
                        return True
                    else:
                        logger.warning(f"Package {package_name} was not installed on server {guild_id}")
                        return False
        except Exception as e:
            logger.error(f"Failed to remove package {package_name} from server {guild_id}: {e}")
            return False
    
    async def get_all_installed_packages(self) -> List[str]:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("""
                    SELECT DISTINCT package_name FROM installed_packages
                """)
                results = await cursor.fetchall()
                return [row[0] for row in results]

db_manager = DatabaseManager()
