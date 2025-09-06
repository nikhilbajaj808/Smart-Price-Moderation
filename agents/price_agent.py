import pandas as pd
import math
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / 'data' / 'marketplace.csv'

class PriceAgent:
    def __init__(self, data_path=None):
        path = data_path or DATA_PATH
        try:
            self.df = pd.read_csv(path)
        except Exception:
            # fallback to empty df
            self.df = pd.DataFrame(columns=['category','brand','condition','age_months','asking_price'])

    def baseline_median(self, category, brand=None):
        df = self.df[self.df['category'].str.lower()==category.lower()]
        if brand:
            bdf = df[df['brand'].str.lower()==brand.lower()]
            if len(bdf)>=3:
                return float(bdf['asking_price'].median())
        if len(df)>0:
            return float(df['asking_price'].median())
        # default fallback baseline
        return 10000.0

    def suggest_price(self, product):
        # product: dict with keys category, brand, condition, age_months, asking_price (optional)
        category = product.get('category','misc') or 'misc'
        brand = product.get('brand',None)
        condition = product.get('condition','Good').lower()
        age = int(product.get('age_months') or 0)
        asking = product.get('asking_price', None)

        baseline = self.baseline_median(category, brand)
        # age depreciation: category-based simple heuristics
        # mobile depreciates faster than furniture
        if category.lower() in ['mobile','laptop','electronics']:
            monthly_depr = 0.03
        elif category.lower() in ['furniture']:
            monthly_depr = 0.01
        else:
            monthly_depr = 0.02

        age_factor = max(0.0, 1 - monthly_depr * age)
        # condition factor
        if 'like' in condition:
            cond_factor = 1.10
        elif 'fair' in condition:
            cond_factor = 0.85
        else:
            cond_factor = 1.00

        estimated = baseline * age_factor * cond_factor
        # if asking provided, we blend
        if asking:
            try:
                asking = float(asking)
                estimated = (estimated + asking) / 2.0
            except Exception:
                pass

        # range +/- 12%
        low = math.floor(estimated * 0.88)
        high = math.ceil(estimated * 1.12)
        return {
            "suggested_min": int(low),
            "suggested_max": int(high),
            "currency": "INR",
            "method": "baseline_from_dataset + age_depreciation + condition_factor (+ asking blend)",
            "reasoning": f"baseline={baseline:.0f}, age_months={age}, age_factor={age_factor:.3f}, condition_factor={cond_factor:.2f}"
        }

if __name__ == '__main__':
    pa = PriceAgent()
    print(pa.suggest_price({'category':'mobile','brand':'Apple','condition':'Good','age_months':24,'asking_price':20000}))
