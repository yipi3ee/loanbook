import psycopg2
from time import time
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, create_engine, DateTime
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()
class freelancer(Base):
    __tablename__ = 'freelancer'

    freelancer_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    rating = Column(String, nullable=True)

    freelancer_skills = relationship("freelancer_skill", back_populates="freelancer")
    tasks = relationship("task", back_populates="freelancer")


class freelancer_skill(Base):
    __tablename__ = 'freelancer_skill'

    freelancer_skill_id = Column(Integer, primary_key=True)
    freelancer_id = Column(Integer, ForeignKey('freelancer.freelancer_id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skill.skill_id'), nullable=False)
    skill_level = Column(String, nullable=True)

    freelancer = relationship("freelancer", back_populates="freelancer_skills")
    skill = relationship("skill", back_populates="freelancer_skills")


class project(Base):
    __tablename__ = 'project'

    project_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    creation_time = Column(DateTime, nullable=False)
    status = Column(String, nullable=True)

    tasks = relationship("task", back_populates="project")


class skill(Base):
    __tablename__ = 'skill'

    skill_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    field = Column(String, nullable=True)

    freelancer_skills = relationship("freelancer_skill", back_populates="skill")
    task_skills = relationship("task_skill", back_populates="skill")


class task(Base):
    __tablename__ = 'task'

    task_id = Column(Integer, primary_key=True)
    description = Column(String, nullable=True)
    deadline = Column(DateTime, nullable=True)
    project_id = Column(Integer, ForeignKey('project.project_id'), nullable=False)
    freelancer_id = Column(Integer, ForeignKey('freelancer.freelancer_id'), nullable=True)

    project = relationship("project", back_populates="tasks")
    freelancer = relationship("freelancer", back_populates="tasks")
    task_skills = relationship("task_skill", back_populates="task")


class task_skill(Base):
    __tablename__ = 'task_skill'

    task_skill_id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('task.task_id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skill.skill_id'), nullable=False)
    required_level = Column(String, nullable=True)

    task = relationship("task", back_populates="task_skills")
    skill = relationship("skill", back_populates="task_skills")


class Model:
    def __init__(self):
        self.engine = create_engine('postgresql://postgres:1234@localhost:5432/freelancer-task-and-project-management-system')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

        self.conn = psycopg2.connect(
            dbname='freelancer-task-and-project-management-system',
            user='postgres',
            password='1234',
            host='localhost',
            port=5432
        )

    def fetch(self, table, limit=None):
        c = self.conn.cursor()
        c.execute(f'SELECT * FROM {table} LIMIT {limit}' if limit else f'SELECT * FROM {table}')
        return c.fetchall()

    def insert_into(self, table, columns, values):
        session = self.Session()
        try:
            table_class = globals()[table]
            record = table_class(**dict(zip(columns, values)))
            session.add(record)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()

    def update(self, table, column, new_value, id):
        session = self.Session()
        try:
            table_class = globals()[table]
            record = session.query(table_class).get(id)
            if record:
                for column_, new_value_ in zip(column, new_value):
                    setattr(record, column_, new_value_)
                    session.commit()
            else:
                print(f"Record with ID {id} not found in {table}.")
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()

    def delete(self, table, id):
        session = self.Session()
        try:
            table_class = globals()[table]
            record = session.query(table_class).get(id)
            if record:
                session.delete(record)
                session.commit()
            else:
                print(f"Record with ID {id} not found in {table}.")
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()

    def get_table_metadata(self, table):
        c = self.conn.cursor()
        query = f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = %s
        """
        c.execute(query, (table,))
        return c.fetchall()

    def generate_random_data(self, table, num_rows):
        metadata = self.get_table_metadata(table)
        c = self.conn.cursor()

        # Retrieve the primary key column (if exists)
        id_column = None
        for col in metadata:
            if "id" in col[0].lower():
                id_column = col[0]
                break

        # Get max ID for sequential generation
        max_id = 0
        if id_column:
            c.execute(f"SELECT COALESCE(MAX({id_column}), 0) FROM {table}")
            max_id = c.fetchone()[0]

        # Iterate to generate the required number of rows
        for i in range(int(num_rows)):
            sql_columns = []
            sql_values = []

            for col in metadata:
                col_name, data_type, is_nullable = col
                sql_columns.append(col_name)

                # Handle sequential IDs
                if col_name == id_column:
                    max_id += 1
                    sql_values.append(str(max_id))

                # Integer and Numeric Columns
                elif data_type in ('integer', 'bigint', 'numeric', 'smallint'):
                    # Check if this is a foreign key column
                    foreign_key_query = f"""
                        SELECT ccu.table_name, ccu.column_name
                        FROM information_schema.constraint_column_usage AS ccu
                        JOIN information_schema.table_constraints AS tc
                        ON ccu.constraint_name = tc.constraint_name
                        WHERE tc.constraint_type = 'FOREIGN KEY'
                        AND ccu.column_name = %s
                    """
                    c.execute(foreign_key_query, (col_name,))
                    fk_info = c.fetchone()

                    if fk_info:
                        fk_table, fk_column = fk_info
                        c.execute(f"SELECT {fk_column} FROM {fk_table} ORDER BY RANDOM() LIMIT 1")
                        fk_value = c.fetchone()
                        sql_values.append(str(fk_value[0]) if fk_value else "NULL")
                    else:
                        sql_values.append(f"FLOOR(RANDOM() * 10000)::int")

                # Text and Character Columns
                elif data_type in ('text', 'varchar', 'char', 'character varying'):
                    sql_values.append(f"'Random_' || FLOOR(RANDOM() * 10000)::text")

                # Boolean Columns
                elif data_type == 'boolean':
                    sql_values.append(f"(RANDOM() > 0.5)::boolean")

                # Timestamp Columns
                elif data_type.startswith('timestamp'):
                    sql_values.append(f"NOW() - INTERVAL '1 day' * FLOOR(RANDOM() * 100)")

                # Date Columns
                elif data_type == 'date':
                    sql_values.append(f"CURRENT_DATE - INTERVAL '1 day' * FLOOR(RANDOM() * 365)::int")

                # Default for Other Types
                else:
                    if is_nullable == 'YES':
                        sql_values.append("NULL")
                    else:
                        sql_values.append("''")

            # Generate the SQL query for this row
            query = f"""
                INSERT INTO {table} ({', '.join(sql_columns)}) 
                VALUES ({', '.join(sql_values)});
            """
            try:
                c.execute(query)
            except Exception as e:
                print(f"Error inserting row {i + 1}: {e}")

        self.conn.commit()

    def __del__(self):
        self.conn.close()
    
    def custom_query_1(self, min_freelancer_id, max_freelancer_id):
        start_time = time.time()
        c = self.conn.cursor()
        query = f"""
            SELECT f.freelancer_id, COUNT(ts.task_id) AS task_count
            FROM freelancer_skill f
            JOIN task t ON f.freelancer_id = t.freelancer_id
            JOIN task_skill ts ON t.task_id = ts.task_id
            WHERE f.freelancer_id BETWEEN %s AND %s
            GROUP BY f.freelancer_id;
        """
        c.execute(query, (min_freelancer_id, max_freelancer_id))
        records = c.fetchall()
        elapsed_time = (time.time() - start_time) * 1000  # milliseconds
        return records, elapsed_time

    def custom_query_2(self, min_task_id, max_task_id):
        start_time = time.time()
        c = self.conn.cursor()
        query = f"""
            SELECT t.task_id, COUNT(ts.skill_id) AS required_skills
            FROM task t
            JOIN task_skill ts ON t.task_id = ts.task_id
            WHERE t.task_id BETWEEN %s AND %s
            GROUP BY t.task_id;
        """
        c.execute(query, (min_task_id, max_task_id))
        records = c.fetchall()
        elapsed_time = (time.time() - start_time) * 1000  # milliseconds
        return records, elapsed_time

    def custom_query_3(self, min_project_id, max_project_id):
        start_time = time.time()
        c = self.conn.cursor()
        query = f"""
            SELECT p.project_id, COUNT(t.task_id) AS total_tasks
            FROM project p
            JOIN task t ON p.project_id = t.project_id
            WHERE p.project_id BETWEEN %s AND %s
            GROUP BY p.project_id;
        """
        c.execute(query, (min_project_id, max_project_id))
        records = c.fetchall()
        elapsed_time = (time.time() - start_time) * 1000  # milliseconds
        return records, elapsed_time
