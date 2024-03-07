# %%
from selenium import webdriver
import pandas as pd
import os
import unicodedata
from pathlib import Path
from datetime import datetime
import traceback

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from time import sleep

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# %%
def get_timestamp():
    # Get current timestamp in the format yyyymmdd_hhmmss
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def normalize_string_for_filename(input_str):
    # Normalize the string to remove special characters
    normalized_str = unicodedata.normalize('NFKD', input_str)
    # Remove non-ASCII characters
    normalized_str = normalized_str.encode('ASCII', 'ignore').decode('utf-8')
    # Replace spaces with underscores
    normalized_str = normalized_str.replace(' ', '_')
    # Replace slashes with underscores
    normalized_str = normalized_str.replace('/', '_')
    return normalized_str

def scrape_data(indice_ano):
    try:
        #Check if the saving files directory already exists, if not, it creates the directory
        output_directory = Path(r'C:\Users\stree\OneDrive\Desktop\Scrape SSP\Output_file')
        output_logs = Path(r'C:\Users\stree\OneDrive\Desktop\Scrape SSP\Scripts\Logs')

        if not os.path.exists(output_directory):
            os.makedirs(output_directory, exist_ok=True)
            print(f'Dir created: {output_directory}')
        else:
            print(f'Dir already exists! {output_directory}')
        
        #Busca de elementos e coleta de dados
        url = 'https://www.ssp.sp.gov.br/estatistica/dados-mensais'
        
        options = Options()
        options.headless = True  # Enable headless mode, does the extraction without a window opened
        #options.add_argument("--headless") 
        driver = Firefox(options=options)
        driver.get(url)

        sleep(1.2)


        # Wait for the dynamic content to load (you may need to adjust the wait time)
        driver.implicitly_wait(5)

        # Get the updated HTML content
        html_content = driver.page_source

        conjunto_listas_menu = driver.find_elements(By.XPATH, '//div[@class="row mb-4"]')

        # [1] indice para ir para as 4 listas
        # 4 listas (ano, regioes, municipios, delegacias) e 1 botao (exportar)
        elementos_dropdown = conjunto_listas_menu[1].find_elements(By.XPATH, 'div[@class="col"]/select')

        # Year = Select(elementos_dropdown[0])
        # Regiao = Select(elementos_dropdown[1])
        # Municipio = Select(elementos_dropdown[2])
        # Delegacia = Select(elementos_dropdown[3])
        
        # Assuming there is at least one dropdown
        if elementos_dropdown:
            # Create an empty DataFrame with the desired column names
            column_headers = [column.text for column in driver.find_elements(By.XPATH, "//div[@id='collapse0']//table[@class='table table-striped table-hover']/thead/tr/th")]
            final_dataframe = pd.DataFrame(columns=column_headers + ['Year', 'Regiao', 'Municipio', 'Delegacia'])
            
            Year = Select(elementos_dropdown[0])
            Year.select_by_index(indice_ano)
            sleep(2.0)

            for index_2 in range( len( Select( elementos_dropdown[1] ).options )):
                if index_2 == 12: #index_2 != 0:
                    Regiao = Select(elementos_dropdown[1])
                    Regiao.select_by_index(index_2)
                    sleep(2.0)

                    for index_3 in range(len(Select(elementos_dropdown[2]).options)):
                        if index_3 == 16: #index_3 != 0:
                            Municipio = Select(elementos_dropdown[2])
                            Municipio.select_by_index(index_3)
                            sleep(2.0)
                        
                            for index_4 in range(len(Select(elementos_dropdown[3]).options)):
                                if index_4 == 1: #index_4 != 0:
                                    Delegacia = Select(elementos_dropdown[3])
                                    Delegacia.select_by_index(index_4)
                                    sleep(2.0)
                                    
                                    try:
                                        # Extracting rows
                                        rows_elements = driver.find_elements(By.XPATH, "//div[@id='collapse0']//table[@class='table table-striped table-hover']/tbody/tr")  # Linhas
                                        rows_data = []  # Lista
                                        for row in rows_elements:
                                            row_data = [i.text for i in row.find_elements(By.TAG_NAME, 'th') + row.find_elements(By.TAG_NAME, 'td')]
                                            rows_data.append(row_data)
                            
                                        # DataFrame
                                        new_data = pd.DataFrame(rows_data, columns=column_headers)
                                    
                                        # New Columns
                                        new_data['Year'] = Year.first_selected_option.text
                                        new_data['Regiao'] = Regiao.first_selected_option.text
                                        new_data['Municipio'] = Municipio.first_selected_option.text
                                        new_data['Delegacia'] = Delegacia.first_selected_option.text
                                        
                                        # Append the new data to final_dataframe
                                        # final_dataframe = pd.concat([final_dataframe, new_data], ignore_index=True) #not necessary atm
                                        
                                        # This part of the code deals with characters that can stop the proccess (special character such as: ? / \)
                                        normalized_delegacia_name = normalize_string_for_filename(Delegacia.first_selected_option.text)


                                        new_data.to_csv(
                                            f'{output_directory}/{Year.first_selected_option.text}_{Regiao.first_selected_option.text}_{Municipio.first_selected_option.text}_{normalized_delegacia_name}.csv', 
                                            sep=';', 
                                            index=False, 
                                            encoding='utf-8', 
                                            header=True
                                        )

                                        

                                    except Exception as ee:
                                        # Log the exception details to a file
                                        with open( os.path.join(output_logs, 'error_log_internal_routine.txt'), 'a') as log_file:
                                            log_file.write(f'{get_timestamp()} | Error at index {indice_ano, index_2, index_3, index_4}: {str(ee)}\n')
    except Exception as e:
        # Log the exception details to a file
        with open( os.path.join(output_logs, 'error_log.txt'), 'a') as log_file: 
            log_file.write(f'{get_timestamp()} | Error at index {indice_ano, index_2, index_3, index_4}: {str(e)}\n')

