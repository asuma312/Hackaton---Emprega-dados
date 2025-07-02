import pandas as pd


class SheetsCleaner:


    def __read_csv__(self, csv_path:str, header_row:int = 0, separator:str = ';', skiprows:int = 0)->pd.DataFrame:
        """Dataframe
        Reads a CSV file and returns a DataFrame.
        """
        try:
            df = pd.read_csv(csv_path, header=header_row, sep=separator, skiprows=skiprows, encoding='utf-8-sig')
            return df
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            raise


    def clean_receita_csv(self,csv_name:str='receita.csv')->pd.DataFrame:
        df = self.__read_csv__(csv_name)
        alucar_columns = [
            'Nome (Alucar)',
            'Data',
            'Mes',
            'Ano',
            'Valor\nReceita'
        ]
        df_receita_alucar = df[alucar_columns]

        df_receita_alucar = self.clean_alucar_sheet(df_receita_alucar)

        consigcar_columns = [
            'Faturamento\nConsigCar',
            'Valor',
            'Data'
        ]
        df_receita_consigcar = df[consigcar_columns]
        df_receita_consigcar = self.clean_consigcar_sheet(df_receita_consigcar)


        df_receita_alucar['empresa'] = 'Alucar'
        df_receita_consigcar['empresa'] = 'ConsigCar'

        full_df = pd.concat([df_receita_alucar, df_receita_consigcar], ignore_index=True)

        return full_df

    def clean_alucar_receita_data(self, row:pd.Series) -> pd.Series:
        row['valor_receita'] = float(row['valor_receita'].split(" ")[-1].replace(".", "").replace(",", "."))
        return row

    def clean_alucar_sheet(self,df_alucar:pd.DataFrame)->pd.DataFrame:
        alucar_renamed_columns = {
            'Nome (Alucar)': 'nome_cliente',
            'Data': 'data',
            'Mes': 'mes',
            'Ano': 'ano',
            'Valor\nReceita': 'valor_receita'
        }

        df_alucar.rename(columns=alucar_renamed_columns, inplace=True)
        df_alucar.dropna(subset=['nome_cliente'], inplace=True)
        df_alucar.dropna(subset=['mes'], inplace=True)
        df_alucar = df_alucar[df_alucar['nome_cliente'] != 'Estimativa']
        df_alucar['data'] = pd.to_datetime(df_alucar['data'], errors='coerce', format='%d/%m/%Y')
        df_alucar.drop(['mes', 'ano'], inplace=True, axis=1)
        df_alucar:pd.DataFrame = df_alucar.apply(self.clean_alucar_receita_data, axis=1)
        df_alucar = df_alucar.sort_values(by=['data'], ascending=True)
        return df_alucar

    def clean_consigcar_receita_data(self, row:pd.Series) -> pd.Series:
        row['valor_receita'] = float(row['valor_receita'].split(" ")[-1].replace(".", "").replace(",", "."))
        return row

    def clean_consigcar_sheet(self,df_consigcar:pd.DataFrame)->pd.DataFrame:
        consigcar_renamed_columns = {
            'Faturamento\nConsigCar': 'nome_cliente',
            'Valor': 'valor_receita',
            'Data':'data'
        }
        df_consigcar.rename(columns=consigcar_renamed_columns, inplace=True)
        df_consigcar.dropna(subset=['valor_receita'], inplace=True)
        df_consigcar.dropna(subset=['data'], inplace=True)

        df_consigcar['data'] = pd.to_datetime(df_consigcar['data'], errors='coerce', format='%d/%m/%Y')
        df_consigcar['data'] = df_consigcar['data'].dt.to_period('M').dt.to_timestamp()

        df_consigcar = df_consigcar.apply(self.clean_consigcar_receita_data, axis=1)
        df_consigcar = df_consigcar.sort_values(by=['data'], ascending=True)
        return df_consigcar

    def clean_despesas_data(self, row: pd.Series) -> pd.Series:
        row['janeiro'] = float(row['janeiro'].split(" ")[-1].replace(".", "").replace(",", "."))
        row['fevereiro'] = float(row['fevereiro'].split(" ")[-1].replace(".", "").replace(",", "."))
        row['março'] = float(row['março'].split(" ")[-1].replace(".", "").replace(",", "."))
        row['abril'] = float(row['abril'].split(" ")[-1].replace(".", "").replace(",", "."))
        row['maio'] = float(row['maio'].split(" ")[-1].replace(".", "").replace(",", "."))
        row['junho'] = float(row['junho'].split(" ")[-1].replace(".", "").replace(",", "."))
        row['julho'] = float(row['julho'].split(" ")[-1].replace(".", "").replace(",", "."))
        row['agosto'] = float(row['agosto'].split(" ")[-1].replace(".", "").replace(",", "."))
        row['setembro'] = float(row['setembro'].split(" ")[-1].replace(".", "").replace(",", "."))
        row['outubro'] = float(row['outubro'].split(" ")[-1].replace(".", "").replace(",", "."))
        row['novembro'] = float(row['novembro'].split(" ")[-1].replace(".", "").replace(",", "."))
        row['dezembro'] = float(row['dezembro'].split(" ")[-1].replace(".", "").replace(",", "."))
        return row

    def clean_despesas_csv(self, csv_name:str='despesas.csv'):
        df = self.__read_csv__(csv_name)
        index_separation = list(df[df['DESPESAS'] == 'DESPESAS'].index)[-1]
        df_alucar = df.iloc[:index_separation]
        df_alucar.dropna(subset=['DESPESAS'], inplace=True)
        df_alucar = df_alucar.apply(self.clean_despesas_data, axis=1)


        df_consigcar = df.iloc[index_separation:]
        df_consigcar.dropna(subset=['DESPESAS'], inplace=True)
        df_consigcar = df_consigcar[df_consigcar['DESPESAS'] != 'DESPESAS']
        df_consigcar = df_consigcar.apply(self.clean_despesas_data, axis=1)

        df_consigcar['empresa'] = 'ConsigCar'
        df_alucar['empresa'] = 'Alucar'

        df_despesas = pd.concat([df_alucar, df_consigcar], ignore_index=True)
        return df_despesas

    def clean_plr_csv(self, csv_name:str = 'PLR.csv'):
        df = self.__read_csv__(csv_name,skiprows=2)
        alucar_columns = {
            'Ano':'ano',
            'Mês':'mes',
            'Meta\n1':'meta 1',
            'Meta\n2': 'meta 2',
            'Realizado': 'realizado'
        }
        df_alucar = df[list(alucar_columns.keys())]
        df_alucar = df_alucar.rename(alucar_columns, axis=1)
        df_alucar.dropna(subset=['mes'], inplace=True)

        #TODO ver isso dps
        df_alucar['data'] = '01/' + df_alucar['mes'].astype(str).str.split(".").str[0] + '/' + '2025'
        df_alucar['data'] = pd.to_datetime(df_alucar['data'], errors='coerce', format='%d/%m/%Y')
        df_alucar['data'] = df_alucar['data'].dt.to_period('M').dt.to_timestamp()
        df_alucar.drop(['realizado', 'ano', 'mes'], axis=1, inplace=True)

        consigcar_columns = {
            'Ano.1':'ano',
            'Mês.1':'mes',
            'Meta\n1.1':'meta 1',
            'Meta\n2.1': 'meta 2',
            'Realizado.1': 'realizado'
        }
        df_consigcar = df[list(consigcar_columns.keys())]
        df_consigcar = df_consigcar.rename(consigcar_columns, axis=1)
        df_consigcar.dropna(subset=['mes'], inplace=True)

        df_consigcar['data'] = '01/' + df_consigcar['mes'].astype(str).str.split(".").str[0] + '/' + '2025'
        df_consigcar['data'] = pd.to_datetime(df_consigcar['data'], errors='coerce', format='%d/%m/%Y')
        df_consigcar['data'] = df_consigcar['data'].dt.to_period('M').dt.to_timestamp()
        df_consigcar.drop(['realizado', 'ano', 'mes'], axis=1, inplace=True)


        df = self.__read_csv__(csv_name, skiprows=1)
        meta_columns = {
            'Meta Anual': 'meta anual',
            'Salário Extra': 'salario extra'
        }
        df_metas = df[list(meta_columns.keys())]
        df_metas = df_metas.rename(meta_columns, axis=1)
        df_metas.dropna(subset=['salario extra'], inplace=True)


        df_alucar['empresa'] = 'Alucar'
        df_consigcar['empresa'] = 'ConsigCar'
        df_plr = pd.concat([df_alucar, df_consigcar], ignore_index=True)


        return df_plr, df_metas


if __name__ == "__main__":
    cleaner = SheetsCleaner()
    cleaner.clean_plr_csv()
