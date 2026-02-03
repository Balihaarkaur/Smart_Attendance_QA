import streamlit as st
from datetime import date
from attendance import AttendanceTracker


def init_tracker() -> AttendanceTracker:
    if "tracker" not in st.session_state:
        st.session_state.tracker = AttendanceTracker()
    return st.session_state.tracker


def main() -> None:
    st.set_page_config(page_title="Smart Attendance System", layout="wide", page_icon="📋")
    st.title("📋 Smart Attendance System")
    
    tracker = init_tracker()
    
    # Sidebar
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Go to", ["Add Record", "View Summary", "Reports", "Export/Import"])
    
    if page == "Add Record":
        add_record_page(tracker)
    elif page == "View Summary":
        view_summary_page(tracker)
    elif page == "Reports":
        reports_page(tracker)
    elif page == "Export/Import":
        export_import_page(tracker)


def add_record_page(tracker: AttendanceTracker) -> None:
    st.header("➕ Add Attendance Record")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        emp_id = st.number_input("Employee ID", min_value=1, step=1, value=101)
    with col2:
        record_date = st.date_input("Date", value=date.today())
    with col3:
        status = st.selectbox("Status", tracker.VALID_STATUSES)
    
    if st.button("Add Record", type="primary"):
        try:
            tracker.add_record(int(emp_id), record_date.isoformat(), status)
            st.success(f"✅ Record added for Employee {emp_id}")
        except ValueError as e:
            st.error(f"❌ Error: {e}")
    
    # Show recent records
    if tracker.records:
        st.subheader("Recent Records")
        all_records = []
        for emp, dates in sorted(tracker.records.items()):
            for d, s in sorted(dates.items(), reverse=True)[:5]:
                all_records.append({"Employee ID": emp, "Date": d, "Status": s})
        if all_records:
            st.dataframe(all_records[:10], use_container_width=True)


def view_summary_page(tracker: AttendanceTracker) -> None:
    st.header("📊 Attendance Summary")
    
    tab1, tab2 = st.tabs(["Individual Employee", "All Employees"])
    
    with tab1:
        emp_id = st.number_input("Employee ID", min_value=1, step=1, value=101, key="summary_emp")
        
        if st.button("Show Summary"):
            summary = tracker.get_summary(int(emp_id))
            if summary is None:
                st.warning(f"⚠️ No records found for Employee {emp_id}")
            else:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Present", summary["Present"], delta=None)
                with col2:
                    st.metric("Absent", summary["Absent"])
                with col3:
                    st.metric("Leave", summary["Leave"])
                with col4:
                    rate = tracker.get_attendance_rate(int(emp_id))
                    st.metric("Attendance Rate", f"{rate:.1f}%")
                
                # Show detailed records
                records = tracker.get_records(int(emp_id))
                if records:
                    st.subheader("Detailed Records")
                    record_list = [{"Date": d, "Status": s} for d, s in sorted(records.items(), reverse=True)]
                    st.dataframe(record_list, use_container_width=True)
    
    with tab2:
        all_summaries = tracker.get_all_summaries()
        if all_summaries:
            summary_list = []
            for emp_id, summary in sorted(all_summaries.items()):
                rate = tracker.get_attendance_rate(emp_id)
                summary_list.append({
                    "Employee ID": emp_id,
                    "Present": summary["Present"],
                    "Absent": summary["Absent"],
                    "Leave": summary["Leave"],
                    "Attendance Rate (%)": f"{rate:.1f}" if rate else "0.0"
                })
            st.dataframe(summary_list, use_container_width=True)
        else:
            st.info("ℹ️ No attendance records yet.")


def reports_page(tracker: AttendanceTracker) -> None:
    st.header("📈 Reports & Analytics")
    
    if not tracker.records:
        st.info("ℹ️ No data available for reports.")
        return
    
    # Date range filter
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=date(2026, 2, 1))
    with col2:
        end_date = st.date_input("End Date", value=date.today())
    
    if st.button("Generate Report"):
        filtered = tracker.filter_by_date_range(start_date.isoformat(), end_date.isoformat())
        
        if not filtered:
            st.warning("⚠️ No records found in the selected date range.")
        else:
            st.subheader(f"Records from {start_date} to {end_date}")
            
            # Summary statistics
            total_records = sum(len(dates) for dates in filtered.values())
            total_employees = len(filtered)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Employees", total_employees)
            with col2:
                st.metric("Total Records", total_records)
            
            # Detailed records
            record_list = []
            for emp_id, dates in sorted(filtered.items()):
                for d, s in sorted(dates.items()):
                    record_list.append({"Employee ID": emp_id, "Date": d, "Status": s})
            
            st.dataframe(record_list, use_container_width=True)


def export_import_page(tracker: AttendanceTracker) -> None:
    st.header("💾 Export & Import Data")
    
    tab1, tab2 = st.tabs(["Export", "Import"])
    
    with tab1:
        st.subheader("Export Records")
        
        export_format = st.radio("Select Format", ["CSV", "JSON"])
        filename = st.text_input("Filename", value="attendance_data")
        
        if st.button("Export", type="primary"):
            try:
                if export_format == "CSV":
                    filepath = f"{filename}.csv"
                    tracker.export_to_csv(filepath)
                else:
                    filepath = f"{filename}.json"
                    tracker.export_to_json(filepath)
                st.success(f"✅ Data exported to {filepath}")
            except Exception as e:
                st.error(f"❌ Export failed: {e}")
    
    with tab2:
        st.subheader("Import Records")
        
        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
        
        if uploaded_file is not None:
            try:
                # Save uploaded file temporarily
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                count = tracker.import_from_csv(temp_path)
                st.success(f"✅ Imported {count} records successfully")
                
                # Clean up
                import os
                os.remove(temp_path)
            except Exception as e:
                st.error(f"❌ Import failed: {e}")


if __name__ == "__main__":
    main()
