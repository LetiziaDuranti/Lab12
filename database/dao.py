from database.DB_connect import DBConnect

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO

    @staticmethod
    def readAllRifugi():
        conn = DBConnect.get_connection()
        result = []

        query = "SELECT id, nome, localita, altitudine, capienza, aperto FROM rifugio"
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def readConnessioniByYear(year):
        conn = DBConnect.get_connection()
        result = []

        query = """
            SELECT id_rifugio1, id_rifugio2, distanza, difficolta, anno 
            FROM connessione 
            WHERE anno <= %s
        """
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (year,))
        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result