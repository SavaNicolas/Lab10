from database.DB_connect import DBConnect
from model.arco import Arco
from model.country import Country


class DAO():
    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
         FROM country c"""
        cursor.execute(query)

        for row in cursor:
            result.append(Country(**row))
            # equivalente a fare (ArtObject(object_id= row["object_id"])
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllCountries_anno(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT c.StateAbb, c.CCode, c.StateNme
        FROM country c, contiguity c1
        WHERE c.CCode = c1.state1no and c1.year<= %s
        UNION
        SELECT c.StateAbb, c.CCode, c.StateNme
        FROM country c, contiguity2006 c2
        WHERE c.CCode = c2.state1no and c2.year<= %s
        """
        cursor.execute(query,(anno,anno))

        for row in cursor:
            result.append(Country(**row))
            #equivalente a fare (ArtObject(object_id= row["object_id"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(idMapCountry,anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        #least e greatest servono per dire: tra id1 e id2, id1 è sempre il più piccolo, per evitare che ci siano coppie che esistono già nell'ordine inverso
        query = """SELECT DISTINCT LEAST(c1.state1no, c1.state2no) AS state1no, 
                GREATEST(c1.state1no, c1.state2no) AS state2no
                FROM contiguity c1
                WHERE c1.conttype = 1 and c1.year<= %s

                UNION

                SELECT DISTINCT LEAST(c2.state1no, c2.state2no) AS state1no, 
                GREATEST(c2.state1no, c2.state2no) AS state2no
                FROM contiguity2006 c2
                WHERE c2.conttype = 1 and c2.year<= %s"""
        cursor.execute(query,(anno,anno))

        for row in cursor:
            result.append(Arco(idMapCountry[row["state1no"]], idMapCountry[row["state2no"]]))
            # o1 e o2 sono id e noi vogliamo l'oggetto
        cursor.close()
        conn.close()
        return result #mi torna una lista di archi


