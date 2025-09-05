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

## 📌 Roadmap

* [ ] Add PDF export with chart + summary
* [ ] Deploy as `/tools/effective-rate` inside Makerkit CRM
* [ ] Add NPV/DCF option
* [ ] Add branding (Lee & Associates logo on reports)

---

## 📄 License

MIT License © 2025 Lee & Associates – Newport Beach
