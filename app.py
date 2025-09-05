import streamlit as st
import pandas as pd
from io import BytesIO
import streamlit_shadcn_ui as ui
from datetime import datetime

st.set_page_config(
    page_title="Effective Rent / Net Effective Rate",
    page_icon="🏢",
    layout="wide"
)

# Remove form border and padding, style calc button green
st.markdown("""
<style>
[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background: none !important;
}
[data-testid="stForm"] > div {
    border: none !important;
    padding: 0 !important;
}

/* Green calculate button with light/dark mode compatibility */
.stButton > button[kind="primary"] {
    background-color: #22c55e !important;
    border-color: #22c55e !important;
    color: white !important;
}
.stButton > button[kind="primary"]:hover {
    background-color: #16a34a !important;
    border-color: #16a34a !important;
}
.stButton > button[kind="primary"]:focus {
    box-shadow: 0 0 0 0.2rem rgba(34, 197, 94, 0.5) !important;
}

/* Secondary button styling */
.stButton > button[kind="secondary"] {
    background-color: #f1f5f9 !important;
    border-color: #e2e8f0 !important;
    color: #475569 !important;
}
.stButton > button[kind="secondary"]:hover {
    background-color: #e2e8f0 !important;
    border-color: #cbd5e1 !important;
}

/* Dark mode compatibility */
@media (prefers-color-scheme: dark) {
    .stButton > button[kind="primary"] {
        background-color: #22c55e !important;
        border-color: #22c55e !important;
        color: white !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #16a34a !important;
        border-color: #16a34a !important;
    }
    
    .stButton > button[kind="secondary"] {
        background-color: #334155 !important;
        border-color: #475569 !important;
        color: #e2e8f0 !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background-color: #475569 !important;
        border-color: #64748b !important;
    }
}
</style>
""", unsafe_allow_html=True)

def calculate_effective_rent(rsf, start_rent, term_months, annual_escalation, 
                           free_rent_months, ti_allowance, ti_method, discount_rate, 
                           perspective, spread_free_rent):
    
    # Calculate monthly rents with escalations
    monthly_rents = []
    current_rent = start_rent
    
    for month in range(1, term_months + 1):
        if month > 1 and (month - 1) % 12 == 0:
            current_rent = current_rent * (1 + annual_escalation / 100)
        monthly_rents.append(current_rent)
    
    # Apply free rent
    effective_rents = monthly_rents.copy()
    
    if spread_free_rent:
        # Spread the DOLLAR VALUE of free months evenly across term
        n = min(int(free_rent_months), term_months)
        free_value = sum(monthly_rents[:n])  # $/SF total value
        credit_per_month = free_value / term_months  # $/SF/mo
        # Clamp at zero to prevent negative rents
        effective_rents = [max(r - credit_per_month, 0) for r in monthly_rents]
    else:
        # Front-loaded: set first n months to zero
        for i in range(min(int(free_rent_months), term_months)):
            effective_rents[i] = 0
    
    # Calculate TI impact per month
    monthly_rate = discount_rate / 100 / 12
    if ti_method == "Discounted" and monthly_rate > 0:
        ti_per_month = (ti_allowance * monthly_rate) / (1 - (1 + monthly_rate) ** (-term_months))
    else:
        ti_per_month = ti_allowance / term_months
    
    # Apply TI impact based on perspective (CORRECTED SIGNS)
    # Tenant: TI is a credit -> reduces effective rent
    # Landlord: TI is a cost -> increases effective cost
    signed_ti = -ti_per_month if perspective == "Tenant" else +ti_per_month
    net_effective_rents = [r + signed_ti for r in effective_rents]
    
    # Calculate summary metrics
    total_contract_rent = sum(monthly_rents) * rsf
    total_effective_rent = sum(effective_rents) * rsf
    total_free_rent_value = total_contract_rent - total_effective_rent
    total_ti = ti_allowance * rsf
    
    avg_contract_rent = sum(monthly_rents) / term_months
    net_effective_rent_monthly = sum(net_effective_rents) / term_months
    net_effective_rent_annual = net_effective_rent_monthly * 12
    
    # Create schedule dataframe
    schedule_data = {
        'Month': list(range(1, term_months + 1)),
        'Scheduled Rent ($/SF/mo)': [round(rent, 2) for rent in monthly_rents],
        'After Free Rent ($/SF/mo)': [round(rent, 2) for rent in effective_rents],
        'TI ($/SF/mo)': [round(ti_per_month, 2)] * term_months,
        'Effective ($/SF/mo)': [round(rent, 2) for rent in net_effective_rents]
    }
    
    schedule_df = pd.DataFrame(schedule_data)
    
    metrics = {
        'net_effective_rent_monthly': round(net_effective_rent_monthly, 2),
        'net_effective_rent_annual': round(net_effective_rent_annual, 2),
        'avg_contract_rent': round(avg_contract_rent, 2),
        'ti_impact_per_month': round(ti_per_month, 2),
        'total_contract_rent': round(total_contract_rent, 0),
        'total_free_rent_value': round(total_free_rent_value, 0),
        'total_ti': round(total_ti, 0)
    }
    
    return schedule_df, metrics

def main():
    # Page header with title and download interface
    header_col1, header_col2 = st.columns([2, 1])
    
    with header_col1:
        st.title("Effective Rent / Net Effective Rate (NER)")
    
    with header_col2:
        # Download interface will be populated when results are available
        download_placeholder = st.empty()
    
    # Sidebar for all inputs
    with st.sidebar:
        st.header("Lease Parameters")
        with st.form("lease_form", clear_on_submit=False):
            # Basic lease terms
            st.subheader("Basic Terms")
            rsf = st.number_input("RSF (Rentable Square Feet)", min_value=1.0, value=10000.0, step=100.0, format="%.0f", key="rsf", help="Total rentable square footage of the space")
            start_rent = st.number_input("Start Rent ($/SF/mo)", min_value=0.01, value=2.50, step=0.01, format="%.2f", key="start_rent", help="Initial monthly rent per square foot")
            term_months = st.number_input("Term (months)", min_value=1, value=60, step=1, key="term_months", help="Total lease term in months")
            annual_escalation = st.number_input("Annual Escalation (%)", min_value=0.0, value=3.0, step=0.1, format="%.1f", key="annual_escalation", help="Annual rent increase percentage")
            
            st.divider()
            
            # Free rent options
            st.subheader("Free Rent")
            free_rent_months = st.number_input("Free Rent (months)", min_value=0, value=3, step=1, key="free_rent_months", help="Number of months with no rent")
            spread_free_rent = st.checkbox("Spread Free Rent Evenly", value=False, key="spread_free_rent", help="Convert the value of front-loaded free months into an equal monthly credit across the full term")
            
            st.divider()
            
            # TI allowance
            st.subheader("TI Allowance")
            ti_allowance = st.number_input("TI Allowance ($/SF)", min_value=0.0, value=25.0, step=1.0, format="%.2f", key="ti_allowance", help="Tenant improvement allowance per square foot")
            ti_method = st.selectbox("TI Amortization Method", ["Straight-line", "Discounted"], key="ti_method", help="How to spread TI cost over lease term")
            discount_rate = st.number_input("Discount Rate (%)", min_value=0.0, value=7.0, step=0.1, format="%.1f", key="discount_rate", help="Annual discount rate for present value calculation") if st.session_state.get("ti_method") == "Discounted" else 0.0
            
            st.divider()
            
            # Analysis options
            st.subheader("Analysis Options")
            perspective = st.selectbox("Perspective", ["Tenant", "Landlord"], key="perspective", help="Tenant: TI reduces effective rent • Landlord: TI increases effective cost")
            
            submitted = st.form_submit_button("Calculate Effective Rent", use_container_width=True, type="primary")
        
        if st.button("Clear Results", help="Reset to empty state", key="clear_btn", use_container_width=True, type="secondary"):
            for k in ("schedule_df", "metrics"):
                st.session_state.pop(k, None)
            st.rerun()
    
    if submitted:
        # Calculate effective rent
        schedule_df, metrics = calculate_effective_rent(
            rsf, start_rent, term_months, annual_escalation, 
            free_rent_months, ti_allowance, ti_method, discount_rate, 
            perspective, spread_free_rent
        )
        
        st.session_state.schedule_df = schedule_df
        st.session_state.metrics = metrics
    
    # Show empty state or results
    if "schedule_df" in st.session_state and "metrics" in st.session_state:
        schedule_df = st.session_state.schedule_df
        metrics = st.session_state.metrics
        
        # Populate progressive download interface in header
        with download_placeholder.container():
            # Add spacing to align with title baseline
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Prepare download data
            csv = schedule_df.to_csv(index=False)
            
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                schedule_df.to_excel(writer, sheet_name='Rent Schedule', index=False)
                
                summary_data = pd.DataFrame([
                    ['Net Effective Rent ($/SF/mo)', f"{metrics['net_effective_rent_monthly']:,.2f}"],
                    ['Net Effective Rent ($/SF/yr)', f"{metrics['net_effective_rent_annual']:,.2f}"],
                    ['Avg Contract Rent ($/SF/mo)', f"{metrics['avg_contract_rent']:,.2f}"],
                    ['TI Impact ($/SF/mo)', f"{metrics['ti_impact_per_month']:,.2f}"],
                    ['Total Contract Rent ($)', f"{metrics['total_contract_rent']:,.0f}"],
                    ['Total Free Rent Value ($)', f"{metrics['total_free_rent_value']:,.0f}"],
                    ['Total TI ($)', f"{metrics['total_ti']:,.0f}"]
                ], columns=['Metric', 'Value'])
                
                summary_data.to_excel(writer, sheet_name='Summary', index=False)
            
            xlsx_data = buffer.getvalue()
            
            # Generate timestamped filenames
            stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
            base = f"rent_analysis_{int(rsf)}sf_{stamp}"
            
            # Download interface aligned with title
            download_col1, download_col2 = st.columns([1, 1])
            
            with download_col1:
                format_choice = st.selectbox(
                    "Format",
                    options=["CSV", "XLSX"],
                    index=0,
                    key="format_select",
                    label_visibility="collapsed"
                )
            
            with download_col2:
                if format_choice == "XLSX":
                    st.download_button(
                        label="Download", 
                        data=xlsx_data,
                        file_name=f"{base}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                        type="primary"
                    )
                else:  # CSV (default)
                    st.download_button(
                        label="Download",
                        data=csv,
                        file_name=f"{base}.csv",
                        mime="text/csv",
                        use_container_width=True,
                        type="primary"
                    )
        
        # Primary metrics in a 3-column layout
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ui.metric_card(
                title="Net Effective Rent",
                content=f"${metrics['net_effective_rent_monthly']:,.2f}/SF/mo",
                description=f"${metrics['net_effective_rent_annual']:,.2f}/SF/yr",
                key="net_effective_rent_metric"
            )
            
        with col2:
            contract_vs_effective = metrics['avg_contract_rent'] - metrics['net_effective_rent_monthly']
            ui.metric_card(
                title="Avg Contract Rent",
                content=f"${metrics['avg_contract_rent']:,.2f}/SF/mo",
                description=f"{contract_vs_effective:+.2f} $/SF/mo vs NER",
                key="avg_contract_rent_metric"
            )
            
        with col3:
            ui.metric_card(
                title="TI Impact",
                content=f"${metrics['ti_impact_per_month']:,.2f}/SF/mo",
                description=f"${metrics['total_ti']:,.0f} total",
                key="ti_impact_metric"
            )
        
        st.markdown("")
        
        # Total values in a 3-column layout
        st.subheader(f"Total Values ({rsf:,} RSF)")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ui.metric_card(
                title="Total Contract Rent",
                content=f"${metrics['total_contract_rent']:,.0f}",
                description="Total scheduled rent over lease term",
                key="total_contract_rent_metric"
            )
            
        with col2:
            den = metrics['total_contract_rent']
            free_rent_percent = (metrics['total_free_rent_value'] / den * 100) if den else 0.0
            ui.metric_card(
                title="Free Rent Savings",
                content=f"${metrics['total_free_rent_value']:,.0f}",
                description=f"{free_rent_percent:.1f}% of contract",
                key="free_rent_savings_metric"
            )
            
        with col3:
            ti_per_sf_total = metrics['total_ti'] / rsf
            ui.metric_card(
                title="Total TI Allowance",
                content=f"${metrics['total_ti']:,.0f}",
                description=f"${ti_per_sf_total:.2f}/SF",
                key="total_ti_allowance_metric"
            )
        
        st.markdown("---")
        
        # Analysis section with tabs
        st.header("Rent Analysis")
        
        # Create tabs for different views
        tab1, tab2 = st.tabs(["Chart", "Schedule"])
        
        with tab1:
            # Chart with better styling
            chart_data = pd.DataFrame({
                'Month': schedule_df['Month'],
                'Scheduled Rent': schedule_df['Scheduled Rent ($/SF/mo)'],
                'After Free Rent': schedule_df['After Free Rent ($/SF/mo)'],
                'Effective Rent': schedule_df['Effective ($/SF/mo)']
            })
            
            st.markdown("#### NER over Term ($/SF/mo)")
            st.line_chart(chart_data.set_index('Month'), height=400)
            
            # Chart insights
            st.markdown("### Key Insights")
            col1, col2, col3 = st.columns(3)
            with col1:
                ui.metric_card(
                    title="Highest Monthly Rent", 
                    content=f"${schedule_df['Scheduled Rent ($/SF/mo)'].max():,.2f}/SF",
                    key="highest_rent_metric"
                )
            with col2:
                ui.metric_card(
                    title="Free Rent Periods", 
                    content=f"{(schedule_df['After Free Rent ($/SF/mo)'] == 0).sum()} months",
                    key="free_rent_periods_metric"
                )
            with col3:
                avg_effective = schedule_df['Effective ($/SF/mo)'].mean()
                ui.metric_card(
                    title="Avg Effective Rent", 
                    content=f"${avg_effective:,.2f}/SF/mo",
                    key="avg_effective_rent_metric"
                )
        
        with tab2:
            # Detailed monthly schedule table
            st.markdown("### Monthly Payment Schedule")
            st.dataframe(schedule_df, width='stretch', hide_index=True, height=400)
            
            # Additional table insights
            st.markdown("### Schedule Summary")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Months", len(schedule_df))
                st.metric("Escalation Months", len([r for i, r in enumerate(schedule_df['Scheduled Rent ($/SF/mo)']) if i > 0 and r > schedule_df['Scheduled Rent ($/SF/mo)'].iloc[i-1]]))
            with col2:
                st.metric("Free Rent Months", (schedule_df['After Free Rent ($/SF/mo)'] == 0).sum())
                st.metric("Average Monthly Rent", f"${schedule_df['Scheduled Rent ($/SF/mo)'].mean():.2f}/SF")
        
    else:
        # Show empty state when no results
        st.markdown("")
        st.markdown("")
        st.markdown("")
        
        col1, col2, col3 = st.columns([2, 3, 2])
        with col2:
            st.markdown("""
                <div style="text-align: center; color: #6b7280; padding: 3rem 0;">
                    <h3 style="color: #374151; margin-bottom: 1rem;">Enter lease parameters</h3>
                    <p style="margin-bottom: 2rem;">Fill the sidebar and click Calculate.</p>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

# ACCEPTANCE TESTS
# Test A (Tenant, front-loaded):
#   RSF=10,000; Start=2.50; Term=60; Esc=3%; Free=3; TI=$30/SF; TI=Straight-line; Perspective=Tenant
#   Expect: Effective < Avg Contract (since TI credit & free months lower it).
#
# Test B (Tenant, spread):
#   Same as A, with "Spread Free Rent" = true
#   Expect: First months no longer zero; line chart smooth; total free rent value unchanged; NER approx similar to A.
#
# Test C (Landlord):
#   Same inputs as A, Perspective=Landlord
#   Expect: Effective > Avg Contract (TI increases cost).
#
# Sanity: Changing Free Rent from 0 to 3 lowers Tenant NER; Increasing TI lowers Tenant NER, raises Landlord cost.