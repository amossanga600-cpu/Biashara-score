import json

def calculate_credit_score(trader_data):
    metrics = trader_data["metrics"]
    
    # 1. Consistency Score (35% Weight) - Mzunguko wa ununuzi kutoka kwa Msambazaji
    purchases = metrics["monthly_supplier_purchases_tzs"]
    avg_purchase = sum(purchases) / len(purchases)
    purchase_consistency_score = min(100, (avg_purchase / 1000000) * 100) * 0.35

    # 2. Supplier Loyalty Score (30% Weight) - Uaminifu wa ulipaji wa invois za zamani
    history = metrics["supplier_repayment_history"]
    loyalty_ratio = history["paid_on_time"] / history["total_credit_invoices"]
    loyalty_score = (loyalty_ratio * 100) * 0.30

    # 3. Digital Cashflow Volume (25% Weight) - Mzunguko wa miamala ya Lipa Namba/Simu
    digital_ratio = metrics["digital_payments_ratio"]
    digital_score = (digital_ratio * 100) * 0.25

    # 4. Business Stability / Age (10% Weight) - Umri wa biashara
    age_months = trader_data["business_age_months"]
    age_score = min(100, (age_months / 24) * 100) * 0.10

    # Jumla ya Credit Score (0 - 100)
    final_score = round(purchase_consistency_score + loyalty_score + digital_score + age_score)

    # Decision Engine (Uamuzi wa Mkopo kwa ajili ya Benki)
    if final_score >= 75:
        risk_level = "LOW"
        approved = True
        max_loan_tzs = round(avg_purchase * 0.8)  # Anaweza kukopa hadi 80% ya ununuzi wake wa wastani
    elif final_score >= 50:
        risk_level = "MEDIUM"
        approved = True
        max_loan_tzs = round(avg_purchase * 0.4)
    else:
        risk_level = "HIGH"
        approved = False
        max_loan_tzs = 0

    return {
        "trader_id": trader_data["trader_id"],
        "business_name": trader_data["business_name"],
        "credit_score": final_score,
        "risk_level": risk_level,
        "loan_status": "APPROVED" if approved else "REJECTED",
        "max_stock_financing_limit_tzs": max_loan_tzs
    }

# Kujaribu Mfumo (Execution Test)
if __name__ == "__main__":
    with open("sample_trader_data.json", "r") as file:
        data = json.load(file)
        result = calculate_credit_score(data)
        
        print("=" * 50)
        print("   AFRICREDIT ALTERNATIVE SCORING RESULTS   ")
        print("=" * 50)
        print(f"Trader Name  : {result['business_name']}")
        print(f"Credit Score : {result['credit_score']} / 100")
        print(f"Risk Level   : {result['risk_level']}")
        print(f"Loan Status  : {result['loan_status']}")
        print(f"Max Loan     : TZS {result['max_stock_financing_limit_tzs']:,}")
        print("=" * 50)
