import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    all = []
    def __init__ (self, name, breed):
        self.name = name
        self.breed = breed
        Dog.all.append(self)
    @classmethod
    def create_table (cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()
    @classmethod
    def drop_table (self):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO dogs (name, breed) 
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.breed) )
        CONN.commit()
        self.id = CURSOR.lastrowid


    @classmethod
    def create(cls, name, breed):
        new_dog = cls(name, breed)
        new_dog.save()
        return new_dog
    
    @classmethod
    def new_from_db(cls, row):
        dog_instance = cls(row[1], row[2])
        dog_instance.id = row[0]
        return dog_instance
    
    @classmethod
    def get_all (cls):
        sql = """
            SELECT * 
            FROM dogs
        """
        all = CURSOR.execute(sql).fetchall()
        return [cls.new_from_db(dog) for dog in all]
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * 
            FROM dogs
            WHERE name = ?
        """
        dogs = CURSOR.execute(sql, (name,)).fetchall()

        dog_instance = cls.new_from_db(dogs[0])
        return dog_instance

    @classmethod
    def find_by_id(cls, dog_id):
        sql = """
            SELECT * 
            FROM dogs
            WHERE id = ?
        """
        dog = CURSOR.execute(sql, (dog_id,)).fetchone()

        dog_instance = cls.new_from_db(dog)
        return dog_instance
   
    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = """
            SELECT * 
            FROM dogs
            WHERE name = ? AND breed = ?
            """
        dog = CURSOR.execute(sql, (name, breed)).fetchone()

        if dog:
            return dog
        else:
            new_dog = cls.create(name, breed)
            return new_dog
  
    def update (self, new_name):
        self.name = new_name

        sql = """
            UPDATE dogs
            SET name = ?
            WHERE id =  ?

        """
        CURSOR.execute(sql, (new_name, self.id))
        CONN.commit()
                        
            


Dog.create_table()
Dog.drop_table()

