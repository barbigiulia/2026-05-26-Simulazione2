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
------------------------------------------------------------------------------
Vertici (Nodi): I film appartenenti esclusivamente al genere selezionato dall'utente.
Archi : Un arco deve connettere due film diversi se, e solo se, i due film condividono
        almeno un regista (name_id in comune).
Peso : Il valore numerico dell'arco deve corrispondere al numero totale di
       registi in comune tra i due film.

SELECT
    m.id AS m1,
    m2.id AS m2,
    COUNT(DISTINCT dm.name_id) AS peso
FROM
    genre g,
    genre g2,
    movie m,
    movie m2,
    director_mapping dm,
    director_mapping dm2
WHERE g.movie_id = m.id
    AND g2.movie_id = m2.id
    AND m.id = dm.movie_id
    AND m2.id = dm2.movie_id
    AND dm.name_id = dm2.name_id    → stesso registra
    AND m.id < m2.id
    AND g.genre = "Drama"
    AND g2.genre = "Drama"
GROUP BY
    m.id,
    m2.id;
—-----------------------------------------------------------------------------------------------------------------------
Costruire un grafo non orientato e pesato in cui:
Vertici: tutti e soli i film pubblicati nell'anno A.
Archi: due film sono collegati se hanno almeno un attore in comune (role_mapping.category = 'actor').
Peso: il numero di attori in comune.
SELECT
    rm1.movie_id AS movie_v1,
    rm2.movie_id AS movie_v2,
    COUNT(DISTINCT rm1.name_id) AS peso
FROM role_mapping rm1
JOIN role_mapping rm2 ON rm1.name_id = rm2.name_id  -- Stesso attore
JOIN movie m1 ON rm1.movie_id = m1.id
JOIN movie m2 ON rm2.movie_id = m2.id
WHERE m1.year = 2017
  AND m2.year = 2017
  AND rm1.category = 'actor'
  AND rm2.category = 'actor'
  AND rm1.movie_id < rm2.movie_id
GROUP BY rm1.movie_id, rm2.movie_id;


—------------------------------------------------------------------------
Vertici: Tutte e sole le case di produzione (production_company) che hanno prodotto almeno un film del genere G che abbia ricevuto un numero di voti totali maggiore o uguale a V (ratings.total_votes >= V).
Archi: Due case di produzione sono collegate se hanno collaborato con lo stesso regista (director_mapping) per film del genere G.
Peso: Il numero di registi unici che hanno in comune per quel genere.

select m.production_company, m2.production_company, count(distinct dm.name_id) as peso
from movie m , genre g , director_mapping dm ,
     movie m2 , genre g2 , director_mapping dm2
where m.id = g.movie_id
and dm.movie_id = m.id
and dm2.movie_id = m2.id
and m2.id = g2.movie_id
and dm.name_id = dm2.name_id
and m.production_company < m2.production_company
and m.production_company is not null
and g.genre ="Drama"
and m2.production_company is not null
and g2.genre ="Drama"
group by m.production_company, m2.production_company



—------------------------------------------------------------------------

L'utente inserisce una Valutazione Minima R (es. avg_rating = 7.0) e un Paese di Produzione P (es. 'USA'). Costruire un grafo non orientato e pesato in cui:
Vertici: Tutti e soli i registi (names) che hanno diretto almeno un film prodotto nel paese P con una valutazione media maggiore o uguale a R.
Archi: Due registi sono collegati se hanno diretto almeno un film dello stesso genere (genre), a patto che entrambi i film siano stati prodotti nel paese P e abbiano la valutazione minima R.
Peso: Il numero di generi distinti che i due registi hanno in comune.
select dm.name_id as r1, dm2.name_id as d2, count(distinct g.genre) as peso
from director_mapping dm , director_mapping dm2 ,
     movie m , movie m2 ,
     genre g , genre g2 ,
     ratings r , ratings r2
where dm.movie_id = m.id
and m.id = g.movie_id
and m.id = r.movie_id
and dm2.movie_id = m2.id
and m2.id = g2.movie_id
and m2.id = r2.movie_id
and dm.name_id < dm2.name_id
and g.genre = g2.genre
and m.country = "USA"
and m2.country = "USA"
and r.avg_rating >= 7.0
and r2.avg_rating >= 7.0
group by dm.name_id , dm2.name_id;




—--------------------------------------------------------------------------
L'utente seleziona una Lingua L (es. 'English') e un Anno Minimo Y (es. 2015). Costruire un grafo non orientato e pesato in cui:
Vertici: Tutti e soli gli attori (names con role_mapping.category = 'actor') che hanno recitato in almeno un film pubblicato a partire dall'anno Y (compreso) la cui lingua principale è L (movie.languages = L).
Archi: Due attori sono collegati se hanno recitato insieme nello stesso film, a patto che il film sia stato pubblicato dall'anno Y in poi e abbia come lingua principale L.
Peso: Il numero di film che i due attori hanno girato insieme soddisfacendo i criteri sopra indicati.

select rm.name_id, rm2.name_id, count(distinct rm.movie_id) as peso
from role_mapping rm , role_mapping rm2 , movie m
where rm.movie_id = m.id
and rm2.movie_id = m.id          -- Entrambi recitano nello STESSO film 'm'
and rm.category = "actor"        -- Assicuriamoci che entrambi siano attori
and rm2.category = "actor"
and rm.name_id < rm2.name_id     -- Rimosso != perché < basta ed evita duplicati
and m.year >= 2017
and m.languages like "%English%"; -- Trova 'English' da solo o in mezzo ad altre lingue
group by rm.name_id , rm2.name_id; -- Rimosso DISTINCT iniziale



—---------------------------------------------------------------
Vertici: I registi (names) che hanno diretto almeno un film nel paese P.

Archi: Due registi sono collegati se hanno diretto insieme lo stesso film prodotto nel paese P.

Peso: Il numero di film che hanno co-diretto insieme in quel paese.

select dm1.name_id as r1, dm2.name_id as r2, count(distinct m.id) as peso
from director_mapping dm1, director_mapping dm2, movie m
where dm1.movie_id = m.id
and dm2.movie_id = m.id          -- Registi dello STESSO film
and dm1.name_id < dm2.name_id    -- Evita specchiati e auto-relazioni
and m.country = "India"
group by dm1.name_id, dm2.name_id;



—--------------------------------------------------------------
Vertici: Tutti i generi (genre) presenti nel database per l'anno A.

Archi: Due generi sono collegati se esiste almeno un attore (role_mapping.category = 'actor') che ha recitato in entrambi i generi nell'anno A (anche in film diversi).

Peso: Il numero di attori unici in comune tra i due generi per quell'anno.

select g1.genre as genere_1, g2.genre as genere_2, count(distinct rm1.name_id) as peso
from genre g1, genre g2,
     role_mapping rm1, role_mapping rm2,
     movie m1, movie m2
where g1.movie_id = m1.id
and g2.movie_id = m2.id
and rm1.movie_id = m1.id
and rm2.movie_id = m2.id
and rm1.name_id = rm2.name_id    -- Lo STESSO attore
and rm1.category = "actor"
and rm2.category = "actor"
and g1.genre < g2.genre          -- Evita specchiati (es. Drama-Action e Action-Drama)
and m1.year = 2017
and m2.year = 2017
group by g1.genre, g2.genre;


***Nota logica: Qui usiamo due tabelle movie distinte (m1 e m2) perché l'attore può aver fatto un film Drama a gennaio e un film Action
                    a dicembre. Non devono per forza essere lo stesso film.


—-------------------------------------------------------------


L'utente inserisce un Numero Minimo di Voti V (es. 5000). Costruire un grafo non orientato in cui:

    Vertici: Le case di produzione (movie.production_company) che hanno prodotto almeno un film che ha ottenuto un numero di voti maggiore o uguale a V.

    Archi: Due case di produzione sono collegate se hanno lavorato con lo stesso attore in film che hanno superato i V voti.

    Peso: Il numero di attori unici che hanno lavorato per entrambe le compagnie (in film di successo).

select m1.production_company as comp_1, m2.production_company as comp_2, count(distinct rm1.name_id) as peso
from movie m1, movie m2,
     role_mapping rm1, role_mapping rm2,
     ratings r1, ratings r2
where rm1.movie_id = m1.id
and rm2.movie_id = m2.id
and r1.movie_id = m1.id
and r2.movie_id = m2.id
and rm1.name_id = rm2.name_id    -- Lo STESSO attore
and rm1.category = "actor"
and rm2.category = "actor"
and m1.production_company < m2.production_company
and m1.production_company is not null
and m2.production_company is not null
and r1.total_votes >= 5000
and r2.total_votes >= 5000
group by m1.production_company, m2.production_company;


