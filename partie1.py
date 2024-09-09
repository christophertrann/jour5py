import requests

def get_companies_with_name(company_name):
    try:
        base_url = "https://api.recherche-entreprises.api.gouv.fr/v1/search"
        
        params = {
            "q": company_name,
            "page_size": 10 
        }

        response = requests.get(base_url, params=params)
        
        if response.status_code != 200:
            return []

        data = response.json()
        
        if 'results' not in data:
            return []

        companies = []
        for company in data['results']:
            company_info = {
                "siren": company.get("siren"),
                "nom_entreprise": company.get("nom_entreprise"),
                "date_creation": company.get("date_creation")
            }
            companies.append(company_info)
        
        return companies
    
    except Exception as e:
        print(f"Erreur : {e}")
        return []

#ex2
    
import requests

def get_all_companies_with_name(company_name):
    try:
        base_url = "https://api.recherche-entreprises.api.gouv.fr/v1/search"
        
        params = {
            "q": company_name,
            "page_size": 100,
            "page": 1  
        }

        companies = []
        
        while True:
            response = requests.get(base_url, params=params)
            if response.status_code != 200:
                return []
            
            data = response.json()
            
            if 'results' not in data:
                return []
            
            for company in data['results']:
                company_info = {
                    "siren": company.get("siren"),
                    "nom_entreprise": company.get("nom_entreprise"),
                    "date_creation": company.get("date_creation")
                }
                companies.append(company_info)
            
            if len(data['results']) < params['page_size']:
                break
            
            params['page'] += 1

        return companies

    except Exception as e:
        print(f"Erreur : {e}")
        return []

#ex3
    
import requests
import csv
import os

def get_all_companies_with_name(company_name):
    try:
        
        base_url = "https://api.recherche-entreprises.api.gouv.fr/v1/search"
        
        params = {
            "q": company_name,
            "page_size": 100,  
            "page": 1  
        }

        companies = []
        
        while True:
            
            response = requests.get(base_url, params=params)
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            
            if 'results' not in data:
                return []
            
            for company in data['results']:
                company_info = {
                    "siren": company.get("siren"),
                    "nom_entreprise": company.get("nom_entreprise"),
                    "date_creation": company.get("date_creation")
                }
                companies.append(company_info)
            
            if len(data['results']) < params['page_size']:
                break
            
            params['page'] += 1

        return companies

    except Exception as e:
        
        print(f"Erreur : {e}")
        return []

def get_and_store_companies(company_name, file_path):
    try:
     
        companies = get_all_companies_with_name(company_name)

        if not companies:
            return
        
        existing_sirens = set()
        if os.path.exists(file_path):
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    existing_sirens.add(row['siren'])
        
        new_companies = [c for c in companies if c['siren'] not in existing_sirens]
        
        if not new_companies:
            return
        new_companies.sort(key=lambda x: x['siren'])

        file_exists = os.path.exists(file_path)

        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            fieldnames = ['siren', 'nom_entreprise', 'date_creation']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            for company in new_companies:
                writer.writerow(company)

    except Exception as e:
        print(f"Erreur lors du traitement : {e}")
        return

