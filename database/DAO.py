from database.DB_connect import DBConnect
from model.attore import Attore


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def getRatings():
        conn = DBConnect.get_connection()

        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct r.avg_rating 
                    from ratings r
                    order by r.avg_rating desc
            """
        cursor.execute(query)
        for row in cursor:
            results.append(row["avg_rating"])
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodes(r1,r2):
        conn = DBConnect.get_connection()

        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct n.*
                    from names n , role_mapping rm , movie m , ratings r 
                    where n.id = rm.name_id 
                    and rm.movie_id = m.id 
                    and m.id = r.movie_id 
                    and r.avg_rating >= %s and r.avg_rating<= %s
                    and n.date_of_birth is not null
                """
        cursor.execute(query,(r1,r2))
        for row in cursor:
            results.append(Attore(**row))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getArchi(r1,r2):
        conn = DBConnect.get_connection()

        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct rm.name_id as a1, rm1.name_id as a2, rm.movie_id as movie,
                m.worlwide_gross_income as peso
                from role_mapping rm, role_mapping rm1, movie m, ratings r
                where rm.movie_id = rm1.movie_id
                and rm.movie_id = m.id
                and m.id = r.movie_id
                and r.avg_rating between %s and %s
                and rm.name_id != rm1.name_id
                and rm.name_id < rm1.name_id
                and m.worlwide_gross_income is not null
                and m.worlwide_gross_income like '$%%'
                """
        cursor.execute(query,(r1,r2))
        for row in cursor:
            results.append((row["a1"], row["a2"], row["movie"], row["peso"]))
        cursor.close()
        conn.close()
        return results




