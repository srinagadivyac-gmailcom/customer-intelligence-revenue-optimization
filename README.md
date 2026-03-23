# 🛍️ ShopPulse — Customer Intelligence & Revenue Optimization

> End-to-end customer analytics project analyzing e-commerce transaction data to uncover customer segments, revenue drivers, return patterns, and business insights using Python and MySQL.

---

## 📌 Overview

This project analyzes ShopPulse e-commerce data to identify high-value customers, optimize revenue strategies, and reduce return rates. The analysis covers customer segmentation, category performance, monthly trends, and Pareto-based revenue insights.

---

## 🛠️ Tech Stack

| Tool | Usage |
|------|-------|
| Python (Pandas) | Data cleaning, EDA, feature engineering |
| Matplotlib | Dashboard visualizations |
| MySQL + SQLAlchemy | Database integration & SQL queries |
| python-dotenv | Secure credential management |

---

## ✨ Key Features

- 🧹 **Data Cleaning** — Cancelled order removal, null handling, IQR outlier treatment
- ⚙️ **Feature Engineering** — Customer metrics (AOV, return rate, total spend), segmentation
- 👥 **Customer Segmentation** — Premium / Regular / Low-Value based on spending
- 📊 **EDA** — Category revenue, return rates, monthly trends, repeat customer analysis
- 🗄️ **MySQL Integration** — Transactions loaded to DB, top customer SQL query
- 💡 **Business Insights** — Pareto principle, premium behavior, fashion return analysis
- 📈 **Visual Dashboard** — 5-chart analytics dashboard saved as PNG

---

## 📊 Dashboard Visualizations

1. Customer Segment Distribution (Bar Chart)
2. Monthly Sales Trend (Line Chart)
3. Category-wise Revenue (Bar Chart)
4. Order Status Distribution (Pie Chart)
5. Return Rate by Category (Bar Chart)

---

## 💡 Key Insights

- Top 20% customers contribute **45.42%** of total revenue (Pareto Principle)
- **52.58%** customers are repeat buyers
- Beauty is the highest revenue-generating category
- Accessories & Fashion have highest return rates (~15%)
- Premium customers average **3.13 orders** per person

---

## 📁 Project Structure

```
shoppulse-customer-intelligence/
│
├── shoppulse_analysis.py                     # Main analysis script
├── Customer_Intelligence_Revenue_Optimization.csv  # Dataset (add locally)
├── shoppulse_customer_analytics.png          # Dashboard output
├── .env.example                              # Environment variable template
├── .gitignore                                # Excludes .env and sensitive files
├── requirements.txt                          # Dependencies
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/srinagadivyac-gmailcom/shoppulse-customer-intelligence
cd shoppulse-customer-intelligence
```

### 2. Install Dependencies
```bash
pip install pandas matplotlib sqlalchemy mysql-connector-python python-dotenv
```

### 3. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env with your MySQL credentials
```

### 4. Add Dataset
Place `Customer_Intelligence_Revenue_Optimization.csv` in the project root folder.

### 5. Run the Analysis
```bash
python shoppulse_analysis.py
```

---

## 🔒 Security Notes

- Database credentials stored in `.env` file (never committed to GitHub)
- `.gitignore` excludes `.env` and sensitive files
- Use `.env.example` as setup template

---

## 👩‍💻 Author

**Srinaga Divya Chunchula**  
Data Analyst | Python | SQL | Power BI  
📧 srinagadivyac@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/sri-naga-divya-chunchula-955b56288)  
🐙 [GitHub](https://github.com/srinagadivyac-gmailcom)
