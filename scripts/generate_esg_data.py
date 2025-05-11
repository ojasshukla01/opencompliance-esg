
import pandas as pd
import uuid
import random
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker and set seed
fake = Faker()
Faker.seed(42)
random.seed(42)

# Predefined sectors and countries
sectors = ['Energy', 'Technology', 'Finance', 'Manufacturing', 'Retail', 'Healthcare']
countries = ['Australia', 'India', 'United States', 'Germany', 'Brazil', 'Japan']

def generate_esg_data(num_records=500, output_path='data/esg_sample.csv'):
    data = []
    for _ in range(num_records):
        record = {
            "org_id": str(uuid.uuid4()),
            "org_name": fake.company(),
            "sector": random.choice(sectors),
            "country": random.choice(countries),
            "emissions_score": round(random.uniform(0, 100), 2),
            "labor_compliance_score": round(random.uniform(0, 100), 2),
            "governance_index": round(random.uniform(0, 100), 2),
            "esg_flagged": random.choice([True, False]),
            "report_date": (datetime.today() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        }
        data.append(record)

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"✅ Generated {num_records} ESG records at '{output_path}'")

if __name__ == "__main__":
    generate_esg_data()
