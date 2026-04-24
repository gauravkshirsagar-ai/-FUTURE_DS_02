# ============================================
# Future Interns - Task 2
# Customer Retention & Churn Analysis
# ============================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# --- 1. Load Data ---
df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df.dropna(inplace=True)

print("Data Loaded!")
print(f"Shape: {df.shape}")
print(f"Null Values:\n{df.isnull().sum()}")

# --- 2. KPI Summary ---
total_customers  = len(df)
churned          = df[df['Churn'] == 'Yes'].shape[0]
retained         = df[df['Churn'] == 'No'].shape[0]
churn_rate       = (churned / total_customers) * 100
avg_tenure       = df['tenure'].mean()
avg_monthly      = df['MonthlyCharges'].mean()

print("\n===== KPI SUMMARY =====")
print(f"Total Customers  : {total_customers}")
print(f"Churned          : {churned}")
print(f"Retained         : {retained}")
print(f"Churn Rate       : {churn_rate:.2f}%")
print(f"Avg Tenure       : {avg_tenure:.1f} months")
print(f"Avg Monthly Charge: ${avg_monthly:.2f}")

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 5)

# --- 3. Overall Churn Distribution ---
plt.figure()
churn_counts = df['Churn'].value_counts()
colors = ['#2ecc71', '#e74c3c']
plt.pie(churn_counts, labels=['Retained', 'Churned'],
        autopct='%1.1f%%', colors=colors,
        startangle=90, textprops={'fontsize': 13})
plt.title('Overall Customer Churn Distribution', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('churn_distribution.png', dpi=150)
plt.show()
print("Chart 1 Saved!")

# --- 4. Churn by Contract Type ---
plt.figure()
contract_churn = df.groupby(['Contract', 'Churn']).size().unstack()
contract_churn.plot(kind='bar', color=['#2ecc71', '#e74c3c'],
                    edgecolor='white')
plt.title('Churn by Contract Type', fontsize=14, fontweight='bold')
plt.xlabel('Contract Type')
plt.ylabel('Number of Customers')
plt.xticks(rotation=0)
plt.legend(['Retained', 'Churned'])
plt.tight_layout()
plt.savefig('churn_by_contract.png', dpi=150)
plt.show()
print("Chart 2 Saved!")

# --- 5. Churn by Tenure Group ---
df['Tenure_Group'] = pd.cut(df['tenure'],
                             bins=[0, 12, 24, 36, 48, 60, 72],
                             labels=['0-12m', '13-24m', '25-36m',
                                     '37-48m', '49-60m', '61-72m'])
tenure_churn = df[df['Churn'] == 'Yes'].groupby('Tenure_Group').size()

plt.figure()
sns.barplot(x=tenure_churn.index.astype(str),
            y=tenure_churn.values, palette='Reds_r')
plt.title('Churn by Customer Tenure', fontsize=14, fontweight='bold')
plt.xlabel('Tenure Group')
plt.ylabel('Number of Churned Customers')
plt.tight_layout()
plt.savefig('churn_by_tenure.png', dpi=150)
plt.show()
print("Chart 3 Saved!")

# --- 6. Monthly Charges vs Churn ---
plt.figure()
sns.boxplot(data=df, x='Churn', y='MonthlyCharges',
            palette={'No': '#2ecc71', 'Yes': '#e74c3c'})
plt.title('Monthly Charges vs Churn', fontsize=14, fontweight='bold')
plt.xlabel('Churn')
plt.ylabel('Monthly Charges ($)')
plt.tight_layout()
plt.savefig('monthly_charges_churn.png', dpi=150)
plt.show()
print("Chart 4 Saved!")

# --- 7. Churn by Payment Method ---
pay_churn = df[df['Churn'] == 'Yes'].groupby('PaymentMethod').size()\
              .sort_values(ascending=False).reset_index()
pay_churn.columns = ['PaymentMethod', 'Churned']

plt.figure()
sns.barplot(data=pay_churn, x='Churned', y='PaymentMethod', palette='OrRd_r')
plt.title('Churn by Payment Method', fontsize=14, fontweight='bold')
plt.xlabel('Number of Churned Customers')
plt.ylabel('Payment Method')
plt.tight_layout()
plt.savefig('churn_by_payment.png', dpi=150)
plt.show()
print("Chart 5 Saved!")

print("\nAnalysis Complete! All 5 charts saved.")
print("Next: Import CSV in Power BI for dashboard!")
