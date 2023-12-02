"""Database management"""
import pymongo

class Database:
    """Database containing server settings data"""
    @classmethod
    def start_db(db):
        """Start the database"""
        db.dbclient = pymongo.MongoClient()
        db.database = db.dbclient["db"]
        db.guilds = db.database["guilds"]

    @classmethod
    def clear_db(db):
        """Clear the database"""
        db.guilds.delete_many({})

    @classmethod
    def print_db(db):
        """Print the database"""
        for x in db.guilds.find():
            print(x)

    @classmethod
    def add_server(db, guild_id: int):
        """Add a new server to the database"""
        server = {
            "id": guild_id,
            "channel": 0,
            "mode": 0,
        }
        db.guilds.insert_one(server)

    @classmethod
    def get_server(db, guild_id: int):
        """Get a server's data from the database"""
        query = {"id": guild_id}
        return db.guilds.find_one(query)

    @classmethod
    def update_channel(db, guild_id: int, channel: int):
        """Change logging channel of a server product"""
        query = {"id" : guild_id}
        newvalue = {"$set": {"channel": channel}}
        db.guilds.update_one(query, newvalue)

    @classmethod
    def update_mode(db, guild_id: int, mode: int):
        """Change the level of moderation for a server"""
        query = {"id" : guild_id}
        newvalue = {"$set": {"mode": mode}}
        db.guilds.update_one(query, newvalue)
