from database.DB_connect import ConnessioneDB
from model.consumo_DTO import Consumo

"""
    CONSUMO DAO
    Gestisce le operazioni di accesso alla tabella consumo.
"""

class ConsumoDAO:
    @staticmethod
    def get_consumi(id_impianto) -> list[Consumo] | None:
        """
        Restituisce tutti i consumi di un impianto
        :return: lista di tutti i Consumi di un certo impianto
        """
        cnx = ConnessioneDB.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT * FROM consumo WHERE id_impianto = %s"""
        try:
            cursor.execute(query, (id_impianto,))
            for row in cursor:
                consumo = Consumo(
                    data=row["data"],
                    kwh=row["kwh"],
                    id_impianto=row["id_impianto"],
                )
                result.append(consumo)
        except Exception as e:
            print(f"Errore durante la query get_consumi: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result
    @staticmethod
    def get_media_consumi( mese):

        cnx = ConnessioneDB.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT i.nome, avg(c.kwh)as media
			        FROM impianto i, consumo c 
			        WHERE id_impianto = id and MONTH(c.data)=%s
			        GROUP BY i.nome;
                    """

        try:
            cursor.execute(query, (mese,))
            for row in cursor:
                dati_medie = (row["nome"], row["media"])
                result.append(dati_medie)


        except Exception as e:
            print(f"Errore durante la query get_media_consumi: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def get_consumi_settimana(mese):

        cnx = ConnessioneDB.get_connection()
        result = []

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """ SELECT i.nome, kwh as prezzo_giorno
			        FROM impianto i, consumo c 
			        WHERE id_impianto = id 
			        GROUP BY i.nome, c.data 
			        having MONTH(c.data)=%s and DAY(c.data)<8;
                        """

        try:
            consumi_settimana ={}
            cursor.execute(query, (mese,))
            for row in cursor:
                impianto = row["nome"]
                prezzo_giorno = row["prezzo_giorno"]

                if impianto not in consumi_settimana:
                    consumi_settimana[impianto] = []
                consumi_settimana[impianto].append(prezzo_giorno)

            result.append(consumi_settimana)


        except Exception as e:
            print(f"Errore durante la query get_media_consumi: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

