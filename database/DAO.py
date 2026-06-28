from database.DB_connect import DBConnect
from model.attore import Attore


class DAO():
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
                from ratings r, names n , role_mapping rm , movie m 
                where n.id = rm.name_id 
                and rm.movie_id = m.id 
                and m.id =r.movie_id 
                and r.avg_rating between %s and %s
                and n.date_of_birth is not null
                """
        cursor.execute(query,(r1,r2))
        for row in cursor:
            results.append(Attore(**row))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getIncassi(r1, r2):
        conn = DBConnect.get_connection()

        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select n.id , rm.movie_id , m.worlwide_gross_income as incasso
                    from ratings r, names n , role_mapping rm , movie m 
                    where n.id = rm.name_id 
                    and rm.movie_id = m.id 
                    and m.id =r.movie_id 
                    and r.avg_rating between %s and %s
                    and n.date_of_birth is not null
                    """
        cursor.execute(query, (r1, r2))
        for row in cursor:
            results.append((row["id"], row["movie_id"], row["incasso"]))
        cursor.close()
        conn.close()
        return results
