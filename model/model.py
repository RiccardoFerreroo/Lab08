from database.consumo_DAO import ConsumoDAO
from database.impianto_DAO import ImpiantoDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()

    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        lista_dati_medie = ConsumoDAO.get_media_consumi(mese)
        return lista_dati_medie




    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = float('inf')
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
       # id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {i}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """

        if giorno == 8:
            if costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = list(sequenza_parziale)
            return # ritorna alla parte prima del pop()
        #prova ogni impianto per il giorno corrente


        for impianto, consumi in consumi_settimana.items():
            costo =  consumi[giorno-1]

            #se cambio impianto costo = +5
            if ultimo_impianto is not None and impianto != ultimo_impianto:
                costo += 5
            # se già peggio del migliore taglia ( se costa di più )
            if costo_corrente + costo >= self.__costo_ottimo:
                continue
            sequenza_parziale.append(impianto)
            self.__ricorsione(sequenza_parziale, giorno+1,
                              impianto,
                              costo_corrente+costo,
                              consumi_settimana
                              )
            sequenza_parziale.pop()








        # TODO

    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """
        lista_consumi_settimana = ConsumoDAO.get_consumi_settimana(mese)
        return lista_consumi_settimana

        # TODO

