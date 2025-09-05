## 1. Overview

The **Effective Rent Calculator** is a lightweight tool for commercial real estate brokers to quickly calculate **Net Effective Rent (NER)** and visualize lease economics.
The MVP is a **Streamlit web app** that supports input of basic lease parameters, produces an effective rate analysis, generates a rent schedule, and exports results with a graph.

This PRD covers the initial prototype (Option A — Streamlit) and lays the foundation for a future production-grade Next.js tool.

---

## 2. Goals

* Provide a **fast, accurate calculator** for brokers to analyze deals.
* Reduce manual Excel work for effective rent analysis.
* Support **exports (CSV, XLSX)** and **graphical output** to share with clients.
* Deliver an MVP within a single week (Python + Streamlit).
* Allow easy porting of calculation logic to Next.js/Makerkit in the future.

---

## 3. Non-Goals

* No full-featured lease modeling (NPV, IRR, DCF).
* No integration with CoStar, AIR, or CRM (MVP only).
* No multi-user authentication or cloud deployment (prototype first).

---

## 4. Users

**Primary:**

* Lee & Associates brokers (Jeff, Brian, Alejandro).

**Secondary:**

* Clients reviewing lease economics.
* Analysts supporting the Value-Add Property Group.

---

## 5. Inputs

The app will prompt users for the following parameters:

* **RSF (Rentable Square Feet)**
* **Start Rent (\$/SF/mo)**
* **Lease Term (months)**
* **Annual Escalation (%)**
* **Free Rent (months)**
* **TI Allowance (\$/SF)**
* **TI Amortization Method:** Straight-line | Discounted
* **Discount Rate (annual %)** (only if discounted)
* **Perspective:** Tenant | Landlord
* **Free Rent Treatment:** Front-loaded | Spread evenly

---

## 6. Outputs

* **Summary Metrics**

  * Net Effective Rent (\$/SF/mo and \$/SF/yr)
  * Average Contract Rent (before TI)
  * TI impact (\$/SF/mo)
  * Total Contract Rent (\$)
  * Total Free Rent Value (\$)
  * Total TI (\$)

* **Rent Schedule Table**
  \| Month | Scheduled Rent (\$/SF/mo) | After Free Rent | TI \$/SF/mo | Effective \$/SF/mo |

* **Graph**

  * Line chart of Effective Rent (\$/SF/mo) across the lease term.

* **Exports**

  * CSV download of schedule
  * XLSX download of schedule

---

## 7. User Flow

1. User opens the Streamlit app.
2. Enters lease assumptions into the form.
3. Clicks **"Run Analysis"**.
4. Summary metrics and chart are displayed.
5. User optionally downloads results as CSV/XLSX.

---

## 8. Technical Requirements

* **Language:** Python 3.12+
* **Framework:** Streamlit
* **Dependencies:** pandas, xlsxwriter, openpyxl
* **Charting:** Streamlit’s built-in line chart (altair or plotly optional later).
* **Exports:** pandas `.to_csv` and `.to_excel`.
* **File Structure:**

  ```
  cre-effective-rate/
  ├── .venv/
  ├── app.py
  ├── requirements.txt
  ├── .gitignore
  └── prd.md
  ```

---

## 9. Future Enhancements

* Add **PDF export with chart + summary**.
* Support **NPV/discounted cash flow** option.
* Multi-tenant support inside **Makerkit CRM**.
* Deploy as `/tools/effective-rate` inside Lee & Associates’ internal app.
* Enable **branding (Lee & Associates logo)** in reports.

---

## 10. Success Metrics

* Prototype runs locally with correct outputs within 1 week.
* Brokers can use it live in client meetings (graph + download).
* Results match Excel manual calculations within ±1%.
* Team adoption: at least 3 brokers use tool within first month.

---
