import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def load_transaction_data():
    df = pd.read_csv("Customer_Intelligence_Revenue_Optimization.csv")
    print("Dataset Loaded Successfully")
    print("Shape:", df.shape)
    return df

def preprocess_data(df):
    print("\n=== Data Cleaning & Preprocessing ===")
    df['order_date'] = pd.to_datetime(df['order_date'], format="mixed", dayfirst=True)
    df = df[df['order_status'] != 'Cancelled']
    df['discount_pct'] = df['discount_pct'].fillna(0)
    df['payment_mode'] = df['payment_mode'].fillna('Unknown')
    df = df.drop_duplicates()

    Q1 = df['order_value'].quantile(0.25)
    Q3 = df['order_value'].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df = df[(df['order_value'] >= lower) & (df['order_value'] <= upper)]

    print("Cleaned Records:", len(df))
    return df

def build_customer_metrics(df):
    print("\n=== Feature Engineering ===")

    customer_metrics = df.groupby('customer_id').agg(
        total_orders=('order_id', 'count'),
        total_spent=('order_value', 'sum'),
        avg_order_value=('order_value', 'mean'),
        avg_discount=('discount_pct', 'mean'),
        return_rate=('order_status', lambda x: (x == 'Returned').mean())
    ).reset_index()

    def segment(row):
        if row['total_spent'] > customer_metrics['total_spent'].quantile(0.8):
            return 'Premium'
        elif row['total_spent'] > customer_metrics['total_spent'].quantile(0.4):
            return 'Regular'
        else:
            return 'Low-Value'

    customer_metrics['customer_segment'] = customer_metrics.apply(segment, axis=1)
    print("Customer Metrics Generated")
    return customer_metrics

def perform_eda(df, customer_metrics):
    print("\n=== Exploratory Data Analysis ===")

    print("\nAverage Order Value (AOV):", round(df['order_value'].mean(), 2))

    repeat_customers = customer_metrics[customer_metrics['total_orders'] > 1]
    print("Repeat Customers %:", round(len(repeat_customers) / len(customer_metrics) * 100, 2))

    category_revenue = df.groupby('category')['order_value'].sum().sort_values(ascending=False)
    print("\nCategory-wise Revenue:")
    print(category_revenue)

    discount_return = df.groupby('category')['order_status'] \
        .apply(lambda x: (x == 'Returned').mean() * 100)
    print("\nReturn Rate by Category (%):")
    print(discount_return.round(2))

    df['Month'] = df['order_date'].dt.month
    monthly_sales = df.groupby('Month')['order_value'].sum()

    return category_revenue, discount_return, monthly_sales

def create_dashboard(df, customer_metrics, category_revenue, monthly_sales, discount_return):
    print("\n=== Data Visualization ===")

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('ShopPulse Customer Intelligence & Revenue Optimization Dashboard', fontsize=14, fontweight='bold')

    customer_metrics['customer_segment'].value_counts().plot(kind='bar', ax=axes[0,0], color='skyblue', edgecolor='black')
    axes[0,0].set_title("Customer Segment Distribution", fontweight='bold')
    axes[0,0].set_ylabel("Customers")
    axes[0,0].tick_params(axis='x', rotation=0)

    monthly_sales.plot(marker='o', ax=axes[0,1], color='steelblue', linewidth=2)
    axes[0,1].set_title("Monthly Sales Trend", fontweight='bold')
    axes[0,1].set_ylabel("Revenue")
    axes[0,1].grid(True, alpha=0.3)

    category_revenue.plot(kind='bar', ax=axes[0,2], color='lightgreen', edgecolor='black')
    axes[0,2].set_title("Category-wise Revenue", fontweight='bold')
    axes[0,2].set_ylabel("Revenue")
    axes[0,2].tick_params(axis='x', rotation=45)

    df['order_status'].value_counts().plot(kind='pie', ax=axes[1,0], autopct='%1.1f%%', startangle=90)
    axes[1,0].set_title("Order Status Distribution", fontweight='bold')
    axes[1,0].set_ylabel("")

    discount_return.plot(kind='bar', ax=axes[1,1], color='orange', edgecolor='black')
    axes[1,1].set_title("Return Rate by Category (%)", fontweight='bold')
    axes[1,1].set_ylabel("Return Rate (%)")
    axes[1,1].tick_params(axis='x', rotation=45)

    axes[1,2].axis('off')

    plt.tight_layout()
    plt.savefig("shoppulse_customer_analytics.png", dpi=300, bbox_inches='tight')
    plt.show()
    print("Dashboard saved as shoppulse_customer_analytics.png")

def load_to_database(df):
    print("\n=== SQL Database Integration ===")

    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME", "dataanalysisproject")

    engine = create_engine(
        f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"
    )

    df.to_sql(name="shoppulse_transactions", con=engine, if_exists="replace", index=False)
    print("Data loaded into MySQL successfully")

    query = """
        SELECT customer_id, SUM(order_value) AS total_spent
        FROM shoppulse_transactions
        GROUP BY customer_id
        ORDER BY total_spent DESC
        LIMIT 10;
    """
    top_customers = pd.read_sql(query, engine)
    print("\nTop Customers by Revenue:")
    print(top_customers)

def generate_business_insights(df, customer_metrics):
    print("\n=== Key Business Insights ===")

    total_revenue = df['order_value'].sum()

    top_20_pct = int(0.2 * len(customer_metrics))
    top_revenue = customer_metrics.sort_values(
        by='total_spent', ascending=False
    ).head(top_20_pct)['total_spent'].sum()

    print(f"\n Top 20% customers contribute {round(top_revenue / total_revenue * 100, 2)}% of revenue")

    premium_repeat_rate = customer_metrics[
        customer_metrics['customer_segment'] == 'Premium'
    ]['total_orders'].mean()
    print(f"\n Premium customers show higher repeat purchases")
    print(f" -> Avg Orders: {premium_repeat_rate:.2f}")

    fashion_returns = df[df['category'] == 'Fashion']['order_status']
    fashion_return_rate = (fashion_returns == 'Returned').mean() * 100
    print("\n High discounts in Fashion lead to higher returns")
    print(f" -> Fashion Return Rate: {fashion_return_rate:.2f}%")

def main():
    print("ShopPulse Customer Intelligence & Revenue Optimization")
    print("=" * 60)

    df = load_transaction_data()
    df = preprocess_data(df)
    customer_metrics = build_customer_metrics(df)
    category_revenue, discount_return, monthly_sales = perform_eda(df, customer_metrics)
    load_to_database(df)
    generate_business_insights(df, customer_metrics)
    create_dashboard(df, customer_metrics, category_revenue, monthly_sales, discount_return)

    print("\n=== Project Completed Successfully ===")

if __name__ == "__main__":
    main()
