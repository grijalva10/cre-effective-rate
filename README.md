# CRE Effective Rate Calculator

A lightweight **Streamlit app** for analyzing **Net Effective Rent (NER)** in commercial real estate lease deals.
Brokers can input rent, term, escalations, free rent, and TI allowance to instantly calculate effective rates, view charts, and export results.

---

## ✨ Features

* Input lease parameters:

  * RSF (Rentable Square Feet)
  * Start Rent (\$/SF/mo)
  * Term (months)
  * Annual escalations (%)
  * Free rent (months, front-loaded or spread)
  * TI allowance (\$/SF), amortized straight-line or discounted
  * Perspective: Tenant or Landlord

* Outputs:

  * Net Effective Rent (\$/SF/mo and \$/SF/yr)
  * Average contract rent (before TI)
  * TI impact per SF per month
  * Total contract rent, total free rent value, and TI total
  * Monthly rent schedule

* Visuals & Exports:

  * Line chart of effective rent over term
  * Download CSV/XLSX schedule

---

## 📂 Project Structure

```
cre-effective-rate/
├── app.py              # Streamlit app
├── requirements.txt    # Python dependencies
├── .gitignore
└── prd.md              # Product requirements doc
```

---

## ⚙️ Setup & Installation

Clone the repo:

```bash
git clone https://github.com/YOUR-ORG/cre-effective-rate.git
cd cre-effective-rate
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate environment:

* Mac/Linux:

  ```bash
  source .venv/bin/activate
  ```
* Windows (PowerShell):

  ```bash
  .venv\Scripts\Activate.ps1
  ```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 Run the App

```bash
streamlit run app.py
```

The app will open in your browser at [http://localhost:8501](http://localhost:8501).

---

## 📊 Example Output

* **Summary:** Net Effective Rent, Avg Contract Rent, TI Impact, Totals
* **Table:** Month-by-month rent schedule
* **Graph:** Effective \$/SF/mo line chart
* **Exports:** CSV/XLSX

---

## 🛠 Tech Stack

* **Python 3.12+**
* **Streamlit** for UI
* **pandas** for data handling
* **xlsxwriter / openpyxl** for Excel export

---

## 🧪 Example Usage

**Test A (Tenant, front-loaded):**
- RSF=10,000; Start=2.50; Term=60; Esc=3%; Free=3; TI=$30/SF; TI=Straight-line; Perspective=Tenant
- Expected: Effective < Avg Contract (since TI credit & free months lower it)

**Test B (Tenant, spread):**
- Same as A, with "Spread Free Rent" = true
- Expected: First months no longer zero; smooth line chart; NER similar to A

**Test C (Landlord):**
- Same inputs as A, Perspective=Landlord
- Expected: Effective > Avg Contract (TI increases cost)

## 📌 Roadmap

* [ ] PDF export with charts and summary
* [ ] NPV/DCF analysis option  
* [ ] Next.js port for better performance
* [ ] Multi-tenant lease analysis

---

## 📄 License

MIT License © 2025 Lee & Associates – Newport Beach
