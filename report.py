import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
import io
import random
from PIL import Image, ImageTk
import mysql.connector
import hashlib
import time

class User:
    def __init__(self, id, username, email=None, role=None):
        self.id = id
        self.username = username
        self.email = email
        self.role = role

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="9321675524@j",  # Replace with your MySQL password
                database="employee_management"
            )
            print("Database connection successful")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to database: {err}")
            print(f"Error: {err}")
    
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")
    
    def execute_query(self, query, params=None, fetch=True):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
                
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                self.connection.commit()
                affected_rows = cursor.rowcount
                cursor.close()
                return affected_rows
        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
            messagebox.showerror("Database Error", f"Error executing query: {err}")
            return None

class ReportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employees Report Generator")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f2f5")
        
        # Initialize database connection
        self.db = DatabaseConnection()
        
        self.current_user = None
        
        # Create frames
        self.login_frame = tk.Frame(self.root, bg="#f0f2f5")
        self.main_frame = tk.Frame(self.root, bg="#f0f2f5")
        self.report_frame = tk.Frame(self.root, bg="#f0f2f5")
        
        # Initialize UI
        self.setup_login_ui()
        self.show_login()
        
    def setup_login_ui(self):
        # Create a stylish login form
        login_container = tk.Frame(self.login_frame, bg="white", padx=40, pady=40)
        login_container.pack(pady=100)
        
        # App logo/title
        title_label = tk.Label(login_container, text="Employee Report Generator", 
                              font=("Helvetica", 24, "bold"), bg="white", fg="#1877f2")
        title_label.pack(pady=(0, 30))
        
        # Username
        username_frame = tk.Frame(login_container, bg="white")
        username_frame.pack(fill="x", pady=10)
        
        username_label = tk.Label(username_frame, text="Username:", 
                                 font=("Helvetica", 12), bg="white", anchor="w")
        username_label.pack(fill="x")
        
        self.username_entry = tk.Entry(username_frame, font=("Helvetica", 12), 
                                     bd=1, relief=tk.SOLID)
        self.username_entry.pack(fill="x", pady=(5, 0))
        
        # Password
        password_frame = tk.Frame(login_container, bg="white")
        password_frame.pack(fill="x", pady=10)
        
        password_label = tk.Label(password_frame, text="Password:", 
                                 font=("Helvetica", 12), bg="white", anchor="w")
        password_label.pack(fill="x")
        
        self.password_entry = tk.Entry(password_frame, font=("Helvetica", 12), 
                                     bd=1, relief=tk.SOLID, show="*")
        self.password_entry.pack(fill="x", pady=(5, 0))
        
        # Login button
        login_button = tk.Button(login_container, text="Login", font=("Helvetica", 12, "bold"),
                               bg="#1877f2", fg="white", padx=20, pady=10,
                               command=self.login)
        login_button.pack(pady=20)
        
        # Register link
        register_frame = tk.Frame(login_container, bg="white")
        register_frame.pack(pady=10)
        
        register_label = tk.Label(register_frame, text="Don't have an account?", 
                                 font=("Helvetica", 10), bg="white")
        register_label.pack(side=tk.LEFT)
        
        register_link = tk.Label(register_frame, text="Register", 
                               font=("Helvetica", 10, "bold"), bg="white", fg="#1877f2",
                               cursor="hand2")
        register_link.pack(side=tk.LEFT, padx=(5, 0))
        register_link.bind("<Button-1>", lambda e: self.show_register())
        
    def setup_main_ui(self):
        # Top navigation bar
        nav_bar = tk.Frame(self.main_frame, bg="#1877f2", height=60)
        nav_bar.pack(fill="x")
        
        # App title
        title_label = tk.Label(nav_bar, text="Employee Report Generator", 
                              font=("Helvetica", 16, "bold"), bg="#1877f2", fg="white")
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # User info and logout
        user_frame = tk.Frame(nav_bar, bg="#1877f2")
        user_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        user_label = tk.Label(user_frame, 
                             text=f"Logged in as: {self.current_user.username}", 
                             font=("Helvetica", 12), bg="#1877f2", fg="white")
        user_label.pack(side=tk.LEFT, padx=(0, 20))
        
        logout_button = tk.Button(user_frame, text="Logout", 
                                font=("Helvetica", 10), bg="white", fg="#1877f2",
                                command=self.logout)
        logout_button.pack(side=tk.LEFT)
        
        # Main content area
        content_frame = tk.Frame(self.main_frame, bg="#f0f2f5", padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # Report selection section
        report_section = tk.LabelFrame(content_frame, text="Generate Reports", 
                                     font=("Helvetica", 14, "bold"), bg="white", padx=20, pady=20)
        report_section.pack(fill="x", pady=20)
        
        # Report type buttons
        reports_frame = tk.Frame(report_section, bg="white")
        reports_frame.pack(fill="x", pady=10)
        
        # Create report type buttons with icons (using emoji as placeholders)
        report_types = [
            {"name": "Attendance Report", "icon": "📋", "command": lambda: self.open_report_form("attendance")},
            {"name": "Turnover Report", "icon": "📊", "command": lambda: self.open_report_form("turnover")},
            {"name": "Progress Report", "icon": "📈", "command": lambda: self.open_report_form("progress")},
            {"name": "Financial Report", "icon": "💰", "command": lambda: self.open_report_form("financial")},
            {"name": "Custom Report", "icon": "🔍", "command": lambda: self.open_report_form("custom")}
        ]
        
        for i, report in enumerate(report_types):
            report_button = tk.Frame(reports_frame, bg="white", padx=10, pady=10, 
                                   bd=1, relief=tk.SOLID, cursor="hand2")
            report_button.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
            report_button.bind("<Button-1>", lambda e, cmd=report["command"]: cmd())
            
            icon_label = tk.Label(report_button, text=report["icon"], 
                                font=("Helvetica", 24), bg="white")
            icon_label.pack(pady=(10, 5))
            
            name_label = tk.Label(report_button, text=report["name"], 
                                font=("Helvetica", 12), bg="white")
            name_label.pack(pady=(0, 10))
        
        # Configure grid weights
        for i in range(3):
            reports_frame.columnconfigure(i, weight=1)
        
        # Recent reports section
        recent_section = tk.LabelFrame(content_frame, text="Recent Reports", 
                                     font=("Helvetica", 14, "bold"), bg="white", padx=20, pady=20)
        recent_section.pack(fill="both", expand=True, pady=20)
        
        # Sample recent reports
        columns = ("report_id", "report_type", "created_date", "created_by")
        self.recent_tree = ttk.Treeview(recent_section, columns=columns, show="headings")
        
        # Define headings
        self.recent_tree.heading("report_id", text="ID")
        self.recent_tree.heading("report_type", text="Report Type")
        self.recent_tree.heading("created_date", text="Created Date")
        self.recent_tree.heading("created_by", text="Created By")
        # self.recent_tree.heading("actions", text="Actions")
        
        # Define columns
        self.recent_tree.column("report_id", width=50)
        self.recent_tree.column("report_type", width=150)
        self.recent_tree.column("created_date", width=150)
        self.recent_tree.column("created_by", width=150)
        
        query = "SELECT id, report_type, created_date, created_by FROM reports ORDER BY id;"
        reports = self.db.execute_query(query)
        

# Clear existing data in Treeview (if needed)
        for row in self.recent_tree.get_children():
            self.recent_tree.delete(row)

# Insert fetched data into Treeview
        for report in reports:
            self.recent_tree.insert("", tk.END, values=(report["id"], report["report_type"], report["created_date"], report["created_by"]))

        self.recent_tree.pack(fill="both", expand=True)

        
    def setup_report_form(self, report_type):
        # Clear previous content
        for widget in self.report_frame.winfo_children():
            widget.destroy()
        
        # Top navigation bar
        nav_bar = tk.Frame(self.report_frame, bg="#1877f2", height=60)
        nav_bar.pack(fill="x")
        
        # Back button
        back_button = tk.Button(nav_bar, text="← Back", 
                              font=("Helvetica", 12), bg="#1877f2", fg="white",
                              bd=0, command=self.back_to_main)
        back_button.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Report title
        title_label = tk.Label(nav_bar, 
                              text=f"{report_type.title()} Report", 
                              font=("Helvetica", 16, "bold"), bg="#1877f2", fg="white")
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Main content area
        content_frame = tk.Frame(self.report_frame, bg="#f0f2f5")
        content_frame.pack(fill="both", expand=True)
        
        # Create a notebook for multi-step form
        notebook = ttk.Notebook(content_frame)
        notebook.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Step 1: Basic Information
        basic_frame = tk.Frame(notebook, bg="white", padx=20, pady=20)
        notebook.add(basic_frame, text="Basic Information")
        
        # Date range selection
        date_frame = tk.LabelFrame(basic_frame, text="Report Period", 
                                 font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        date_frame.pack(fill="x", pady=10)
        
        date_grid = tk.Frame(date_frame, bg="white")
        date_grid.pack(fill="x", pady=5)
        
        start_label = tk.Label(date_grid, text="Start Date:", 
                             font=("Helvetica", 10), bg="white")
        start_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.start_date = DateEntry(date_grid, width=12, background='#1877f2',
                                  foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.start_date.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        end_label = tk.Label(date_grid, text="End Date:", 
                           font=("Helvetica", 10), bg="white")
        end_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        self.end_date = DateEntry(date_grid, width=12, background='#1877f2',
                                foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.end_date.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        # Quick date selection buttons
        quick_frame = tk.Frame(date_frame, bg="white")
        quick_frame.pack(fill="x", pady=5)
        
        periods = [
            ("Today", self.set_today),
            ("Yesterday", self.set_yesterday),
            ("Last 7 Days", self.set_last_7_days),
            ("Last 30 Days", self.set_last_30_days),
            ("This Month", self.set_this_month),
            ("Last Month", self.set_last_month)
        ]
        
        for i, (text, command) in enumerate(periods):
            period_button = tk.Button(quick_frame, text=text, 
                                    font=("Helvetica", 9), bg="#f0f2f5", 
                                    command=command)
            period_button.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="w")
        
        # Report details
        details_frame = tk.LabelFrame(basic_frame, text="Report Details", 
                                    font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        details_frame.pack(fill="x", pady=10)
        
        # Report title
        title_frame = tk.Frame(details_frame, bg="white")
        title_frame.pack(fill="x", pady=5)
        
        title_label = tk.Label(title_frame, text="Report Title:", 
                             font=("Helvetica", 10), bg="white")
        title_label.pack(anchor="w")
        
        self.report_title_entry = tk.Entry(title_frame, font=("Helvetica", 10), width=50)
        self.report_title_entry.pack(fill="x", pady=5)
        self.report_title_entry.insert(0, f"{report_type.title()} Report - {datetime.now().strftime('%B %Y')}")
        
        # Report description
        desc_frame = tk.Frame(details_frame, bg="white")
        desc_frame.pack(fill="x", pady=5)
        
        desc_label = tk.Label(desc_frame, text="Description (Optional):", 
                            font=("Helvetica", 10), bg="white")
        desc_label.pack(anchor="w")
        
        self.report_desc_entry = tk.Text(desc_frame, font=("Helvetica", 10), 
                                       width=50, height=4)
        self.report_desc_entry.pack(fill="x", pady=5)
        
        # Step 2: Report-specific data
        data_frame = tk.Frame(notebook, bg="white", padx=20, pady=20)
        notebook.add(data_frame, text="Report Data")
        
        # Different form fields based on report type
        if report_type == "attendance":
            self.setup_attendance_form(data_frame)
        elif report_type == "turnover":
            self.setup_turnover_form(data_frame)
        elif report_type == "progress":
            self.setup_progress_form(data_frame)
        elif report_type == "financial":
            self.setup_financial_form(data_frame)
        else:  # custom
            self.setup_custom_form(data_frame)
        
        # Step 3: Visualization Options
        viz_frame = tk.Frame(notebook, bg="white", padx=20, pady=20)
        notebook.add(viz_frame, text="Visualizations")
        
        # Chart type selection
        chart_frame = tk.LabelFrame(viz_frame, text="Chart Options", 
                                  font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        chart_frame.pack(fill="x", pady=10)
        
        # Chart type
        type_frame = tk.Frame(chart_frame, bg="white")
        type_frame.pack(fill="x", pady=5)
        
        type_label = tk.Label(type_frame, text="Chart Type:", 
                            font=("Helvetica", 10), bg="white")
        type_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.chart_type = tk.StringVar(value="bar")
        chart_types = [
            ("Bar Chart", "bar"),
            ("Line Chart", "line"),
            ("Pie Chart", "pie"),
            ("Area Chart", "area"),
            ("Scatter Plot", "scatter")
        ]
        
        for i, (text, value) in enumerate(chart_types):
            chart_radio = tk.Radiobutton(type_frame, text=text, value=value,
                                       variable=self.chart_type, bg="white")
            chart_radio.grid(row=i//3, column=i%3 + 1, padx=5, pady=5, sticky="w")
        
        # Chart title
        chart_title_frame = tk.Frame(chart_frame, bg="white")
        chart_title_frame.pack(fill="x", pady=5)
        
        chart_title_label = tk.Label(chart_title_frame, text="Chart Title:", 
                                   font=("Helvetica", 10), bg="white")
        chart_title_label.pack(anchor="w")
        
        self.chart_title_entry = tk.Entry(chart_title_frame, font=("Helvetica", 10), width=50)
        self.chart_title_entry.pack(fill="x", pady=5)
        self.chart_title_entry.insert(0, f"{report_type.title()} Overview")
        
        # Chart preview
        preview_frame = tk.LabelFrame(viz_frame, text="Chart Preview", 
                                    font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        preview_frame.pack(fill="both", expand=True, pady=10)
        
        # Create a button to generate preview
        preview_button = tk.Button(preview_frame, text="Generate Preview", 
                                 font=("Helvetica", 10), bg="#1877f2", fg="white",
                                 command=lambda: self.generate_chart_preview(preview_frame, report_type))
        preview_button.pack(pady=10)
        
        # Step 4: Output Options
        output_frame = tk.Frame(notebook, bg="white", padx=20, pady=20)
        notebook.add(output_frame, text="Output Options")
        
        # Output format
        format_frame = tk.LabelFrame(output_frame, text="Output Format", 
                                   font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        format_frame.pack(fill="x", pady=10)
        
        self.output_format = tk.StringVar(value="pdf")
        formats = [
            ("PDF Document", "pdf"),
            ("Excel Spreadsheet", "excel"),
            ("HTML Report", "html")
        ]
        
        for i, (text, value) in enumerate(formats):
            format_radio = tk.Radiobutton(format_frame, text=text, value=value,
                                        variable=self.output_format, bg="white")
            format_radio.pack(anchor="w", pady=5)
        
        # Distribution options
        dist_frame = tk.LabelFrame(output_frame, text="Distribution Options", 
                                 font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        dist_frame.pack(fill="x", pady=10)
        
        # Save locally option
        self.save_local = tk.BooleanVar(value=True)
        save_check = tk.Checkbutton(dist_frame, text="Save report locally", 
                                  variable=self.save_local, bg="white")
        save_check.pack(anchor="w", pady=5)
        
        # Save to database option
        self.save_to_db = tk.BooleanVar(value=True)
        db_check = tk.Checkbutton(dist_frame, text="Save report to database", 
                                variable=self.save_to_db, bg="white")
        db_check.pack(anchor="w", pady=5)
        
        # Email option
        self.send_email = tk.BooleanVar(value=False)
        email_check = tk.Checkbutton(dist_frame, text="Send report via email", 
                                   variable=self.send_email, bg="white",
                                   command=self.toggle_email_options)
        email_check.pack(anchor="w", pady=5)
        
        # Email options (initially hidden)
        self.email_options_frame = tk.Frame(dist_frame, bg="white")
        
        email_to_label = tk.Label(self.email_options_frame, text="Recipients (comma separated):", 
                                bg="white")
        email_to_label.pack(anchor="w", pady=(5, 0))
        
        self.email_to_entry = tk.Entry(self.email_options_frame, font=("Helvetica", 10), width=50)
        self.email_to_entry.pack(fill="x", pady=5)
        
        email_subject_label = tk.Label(self.email_options_frame, text="Email Subject:", 
                                     bg="white")
        email_subject_label.pack(anchor="w", pady=(5, 0))
        
        self.email_subject_entry = tk.Entry(self.email_options_frame, font=("Helvetica", 10), width=50)
        self.email_subject_entry.pack(fill="x", pady=5)
        self.email_subject_entry.insert(0, f"{report_type.title()} Report - {datetime.now().strftime('%B %Y')}")
        
        email_body_label = tk.Label(self.email_options_frame, text="Email Body:", 
                                  bg="white")
        email_body_label.pack(anchor="w", pady=(5, 0))
        
        self.email_body_entry = tk.Text(self.email_options_frame, font=("Helvetica", 10), 
                                      width=50, height=4)
        self.email_body_entry.pack(fill="x", pady=5)
        self.email_body_entry.insert("1.0", f"Please find attached the {report_type} report for your review.\n\nRegards,\n{self.current_user.username}")
        
        # Generate report button
        generate_button = tk.Button(output_frame, text="Generate Report", 
                                  font=("Helvetica", 12, "bold"), bg="#1877f2", fg="white",
                                  padx=20, pady=10,command=lambda: self.generate_report(report_type))
        generate_button.pack(pady=20)
        
    def setup_attendance_form(self, parent_frame):
        # Department selection
        dept_frame = tk.LabelFrame(parent_frame, text="Department", 
                                 font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        dept_frame.pack(fill="x", pady=10)
        
        # Fetch departments from database
        departments = ["All Departments"]
        query = "SELECT DISTINCT department FROM employees"
        result = self.db.execute_query(query)
        if result:
            for row in result:
                if 'department' in row and row['department']:
                    departments.append(row['department'])
        
        self.dept_var = tk.StringVar(value="All Departments")
        
        dept_dropdown = ttk.Combobox(dept_frame, textvariable=self.dept_var, 
                                   values=departments, state="readonly", width=30)
        dept_dropdown.pack(anchor="w", pady=5)
        
        # Attendance metrics
        metrics_frame = tk.LabelFrame(parent_frame, text="Attendance Metrics", 
                                    font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        metrics_frame.pack(fill="x", pady=10)
        
        # Create checkboxes for metrics
        self.include_present = tk.BooleanVar(value=True)
        present_check = tk.Checkbutton(metrics_frame, text="Include Present Days", 
                                     variable=self.include_present, bg="white")
        present_check.pack(anchor="w", pady=2)
        
        self.include_absent = tk.BooleanVar(value=True)
        absent_check = tk.Checkbutton(metrics_frame, text="Include Absent Days", 
                                    variable=self.include_absent, bg="white")
        absent_check.pack(anchor="w", pady=2)
        
        self.include_late = tk.BooleanVar(value=True)
        late_check = tk.Checkbutton(metrics_frame, text="Include Late Arrivals", 
                                  variable=self.include_late, bg="white")
        late_check.pack(anchor="w", pady=2)
        
        self.include_early_departure = tk.BooleanVar(value=True)
        early_check = tk.Checkbutton(metrics_frame, text="Include Early Departures", 
                                   variable=self.include_early_departure, bg="white")
        early_check.pack(anchor="w", pady=2)
        
        self.include_overtime = tk.BooleanVar(value=True)
        overtime_check = tk.Checkbutton(metrics_frame, text="Include Overtime", 
                                      variable=self.include_overtime, bg="white")
        overtime_check.pack(anchor="w", pady=2)
        
        # Working hours
        hours_frame = tk.LabelFrame(parent_frame, text="Working Hours", 
                                  font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        hours_frame.pack(fill="x", pady=10)
        
        start_hour_frame = tk.Frame(hours_frame, bg="white")
        start_hour_frame.pack(fill="x", pady=5)
        
        start_hour_label = tk.Label(start_hour_frame, text="Work Start Time:", 
                                  font=("Helvetica", 10), bg="white")
        start_hour_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.start_hour_var = tk.StringVar(value="09:00")
        start_hour_entry = tk.Entry(start_hour_frame, textvariable=self.start_hour_var, 
                                  width=10)
        start_hour_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # end_hour_label = tk.Label(start_hour_frame, text="Work End Time:",  sticky="w")
        # end_hour_label.grid(row=1, column=0, sticky="w")

        end_hour_label = tk.Label(start_hour_frame, text="Work End Time:",font=("Helvetica", 10), bg="white")
        end_hour_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        self.end_hour_var = tk.StringVar(value="17:00")
        end_hour_entry = tk.Entry(start_hour_frame, textvariable=self.end_hour_var, 
                                width=10)
        end_hour_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        # Holidays
        holiday_frame = tk.LabelFrame(parent_frame, text="Holidays", 
                                    font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        holiday_frame.pack(fill="x", pady=10)
        
        self.include_holidays = tk.BooleanVar(value=True)
        holiday_check = tk.Checkbutton(holiday_frame, text="Exclude Holidays from Calculations", 
                                     variable=self.include_holidays, bg="white")
        holiday_check.pack(anchor="w", pady=5)
        
        # Add holiday button
        add_holiday_button = tk.Button(holiday_frame, text="Add Holiday", 
                                     font=("Helvetica", 10), bg="#f0f2f5",
                                     command=self.add_holiday)
        add_holiday_button.pack(anchor="w", pady=5)
        
        # Holiday list
        holiday_list_frame = tk.Frame(holiday_frame, bg="white")
        holiday_list_frame.pack(fill="x", pady=5)
        
        holiday_list_label = tk.Label(holiday_list_frame, text="Holidays:", 
                                    font=("Helvetica", 10), bg="white")
        holiday_list_label.pack(anchor="w")
        
        self.holiday_listbox = tk.Listbox(holiday_list_frame, height=4, width=40)
        self.holiday_listbox.pack(side=tk.LEFT, fill="x", expand=True, pady=5)
        
        # Add sample holidays
        sample_holidays = [
            "2023-01-01: New Year's Day",
            "2023-05-29: Memorial Day",
            "2023-07-04: Independence Day",
            "2023-09-04: Labor Day"
        ]
        
        for holiday in sample_holidays:
            self.holiday_listbox.insert(tk.END, holiday)
        
        # Scrollbar for holiday list
        holiday_scrollbar = tk.Scrollbar(holiday_list_frame, orient="vertical")
        holiday_scrollbar.config(command=self.holiday_listbox.yview)
        holiday_scrollbar.pack(side=tk.RIGHT, fill="y")
        
        self.holiday_listbox.config(yscrollcommand=holiday_scrollbar.set)
        
        # Employee selection
        employee_frame = tk.LabelFrame(parent_frame, text="Employees", 
                                     font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        employee_frame.pack(fill="x", pady=10)
        
        self.all_employees = tk.BooleanVar(value=True)
        all_emp_check = tk.Checkbutton(employee_frame, text="Include All Employees", 
                                     variable=self.all_employees, bg="white",
                                     command=self.toggle_employee_selection)
        all_emp_check.pack(anchor="w", pady=5)
        
        # Employee selection list (initially hidden)
        self.employee_selection_frame = tk.Frame(employee_frame, bg="white")
        
        # Fetch employees from database
        query = "SELECT emp_id, name FROM employees ORDER BY name"
        employees = self.db.execute_query(query)
        
        if employees:
            self.employee_listbox = tk.Listbox(self.employee_selection_frame, height=6, width=40, selectmode=tk.MULTIPLE)
            for emp in employees:
                self.employee_listbox.insert(tk.END, f"{emp['emp_id']}: {emp['name']}")
            
            scrollbar = tk.Scrollbar(self.employee_selection_frame, orient="vertical")
            scrollbar.config(command=self.employee_listbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill="y")
            
            self.employee_listbox.config(yscrollcommand=scrollbar.set)
            self.employee_listbox.pack(side=tk.LEFT, fill="x", expand=True, pady=5)
        
    def setup_turnover_form(self, parent_frame):
        # Department selection
        dept_frame = tk.LabelFrame(parent_frame, text="Department", 
                                 font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        dept_frame.pack(fill="x", pady=10)
        
        # Fetch departments from database
        departments = ["All Departments"]
        query = "SELECT DISTINCT department FROM employees"
        result = self.db.execute_query(query)
        if result:
            for row in result:
                if 'department' in row and row['department']:
                    departments.append(row['department'])
        
        self.dept_var = tk.StringVar(value="All Departments")
        
        dept_dropdown = ttk.Combobox(dept_frame, textvariable=self.dept_var, 
                                   values=departments, state="readonly", width=30)
        dept_dropdown.pack(anchor="w", pady=5)
        
        # Turnover metrics
        metrics_frame = tk.LabelFrame(parent_frame, text="Turnover Metrics", 
                                    font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        metrics_frame.pack(fill="x", pady=10)
        
        # Create checkboxes for metrics
        self.include_new_hires = tk.BooleanVar(value=True)
        new_hires_check = tk.Checkbutton(metrics_frame, text="Include New Hires", 
                                       variable=self.include_new_hires, bg="white")
        new_hires_check.pack(anchor="w", pady=2)
        
        self.include_terminations = tk.BooleanVar(value=True)
        terminations_check = tk.Checkbutton(metrics_frame, text="Include Terminations", 
                                          variable=self.include_terminations, bg="white")
        terminations_check.pack(anchor="w", pady=2)
        
        self.include_voluntary = tk.BooleanVar(value=True)
        voluntary_check = tk.Checkbutton(metrics_frame, text="Include Voluntary Departures", 
                                       variable=self.include_voluntary, bg="white")
        voluntary_check.pack(anchor="w", pady=2)
        
        self.include_involuntary = tk.BooleanVar(value=True)
        involuntary_check = tk.Checkbutton(metrics_frame, text="Include Involuntary Departures", 
                                         variable=self.include_involuntary, bg="white")
        involuntary_check.pack(anchor="w", pady=2)
        
        # Comparison options
        comparison_frame = tk.LabelFrame(parent_frame, text="Comparison Options", 
                                       font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        comparison_frame.pack(fill="x", pady=10)
        
        self.compare_previous = tk.BooleanVar(value=True)
        compare_check = tk.Checkbutton(comparison_frame, text="Compare with Previous Period", 
                                     variable=self.compare_previous, bg="white")
        compare_check.pack(anchor="w", pady=5)
        
        # Breakdown options
        breakdown_frame = tk.LabelFrame(parent_frame, text="Breakdown Options", 
                                      font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        breakdown_frame.pack(fill="x", pady=10)
        
        self.breakdown_by_dept = tk.BooleanVar(value=True)
        dept_breakdown_check = tk.Checkbutton(breakdown_frame, text="Breakdown by Department", 
                                            variable=self.breakdown_by_dept, bg="white")
        dept_breakdown_check.pack(anchor="w", pady=2)
        
        self.breakdown_by_position = tk.BooleanVar(value=True)
        position_breakdown_check = tk.Checkbutton(breakdown_frame, text="Breakdown by Position", 
                                                variable=self.breakdown_by_position, bg="white")
        position_breakdown_check.pack(anchor="w", pady=2)
        
        self.breakdown_by_reason = tk.BooleanVar(value=True)
        reason_breakdown_check = tk.Checkbutton(breakdown_frame, text="Breakdown by Reason", 
                                              variable=self.breakdown_by_reason, bg="white")
        reason_breakdown_check.pack(anchor="w", pady=2)
        
    def setup_progress_form(self, parent_frame):
        # Project selection
        project_frame = tk.LabelFrame(parent_frame, text="Project Selection", 
                                    font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        project_frame.pack(fill="x", pady=10)
        
        self.project_var = tk.StringVar(value="All Projects")
        projects = ["All Projects", "Website Redesign", "Mobile App Development", 
                   "Database Migration", "Cloud Infrastructure", "Marketing Campaign"]
        
        project_dropdown = ttk.Combobox(project_frame, textvariable=self.project_var, 
                                      values=projects, state="readonly", width=30)
        project_dropdown.pack(anchor="w", pady=5)
        
        # Progress metrics
        metrics_frame = tk.LabelFrame(parent_frame, text="Progress Metrics", 
                                    font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        metrics_frame.pack(fill="x", pady=10)
        
        # Create checkboxes for metrics
        self.include_tasks_completed = tk.BooleanVar(value=True)
        tasks_check = tk.Checkbutton(metrics_frame, text="Include Tasks Completed", 
                                   variable=self.include_tasks_completed, bg="white")
        tasks_check.pack(anchor="w", pady=2)
        
        self.include_milestones = tk.BooleanVar(value=True)
        milestones_check = tk.Checkbutton(metrics_frame, text="Include Milestones", 
                                        variable=self.include_milestones, bg="white")
        milestones_check.pack(anchor="w", pady=2)
        
        self.include_budget = tk.BooleanVar(value=True)
        budget_check = tk.Checkbutton(metrics_frame, text="Include Budget Utilization", 
                                    variable=self.include_budget, bg="white")
        budget_check.pack(anchor="w", pady=2)
        
        self.include_timeline = tk.BooleanVar(value=True)
        timeline_check = tk.Checkbutton(metrics_frame, text="Include Timeline Progress", 
                                      variable=self.include_timeline, bg="white")
        timeline_check.pack(anchor="w", pady=2)
        
        self.include_resources = tk.BooleanVar(value=True)
        resources_check = tk.Checkbutton(metrics_frame, text="Include Resource Allocation", 
                                       variable=self.include_resources, bg="white")
        resources_check.pack(anchor="w", pady=2)
        
        # Team members
        team_frame = tk.LabelFrame(parent_frame, text="Team Members", 
                                 font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        team_frame.pack(fill="x", pady=10)
        
        self.include_team_performance = tk.BooleanVar(value=True)
        team_check = tk.Checkbutton(team_frame, text="Include Team Performance", 
                                  variable=self.include_team_performance, bg="white")
        team_check.pack(anchor="w", pady=5)
        
        # Team member list
        team_list_frame = tk.Frame(team_frame, bg="white")
        team_list_frame.pack(fill="x", pady=5)
        
        team_list_label = tk.Label(team_list_frame, text="Team Members:", 
                                 font=("Helvetica", 10), bg="white")
        team_list_label.pack(anchor="w")
        
        # Fetch employees from database for team members
        query = "SELECT emp_id, name FROM employees ORDER BY name"
        employees = self.db.execute_query(query)
        
        self.team_listbox = tk.Listbox(team_list_frame, height=4, width=40, selectmode=tk.MULTIPLE)
        
        if employees:
            for emp in employees:
                self.team_listbox.insert(tk.END, f"{emp['emp_id']}: {emp['name']}")
        else:
            # Sample team members if no database data
            sample_members = [
                "John Smith - Project Manager",
                "Sarah Johnson - Developer",
                "Michael Brown - Designer",
                "Emily Davis - QA Engineer",
                "Robert Wilson - DevOps"
            ]
            
            for member in sample_members:
                self.team_listbox.insert(tk.END, member)
        
        self.team_listbox.pack(side=tk.LEFT, fill="x", expand=True, pady=5)
        
        # Scrollbar for team list
        team_scrollbar = tk.Scrollbar(team_list_frame, orient="vertical")
        team_scrollbar.config(command=self.team_listbox.yview)
        team_scrollbar.pack(side=tk.RIGHT, fill="y")
        
        self.team_listbox.config(yscrollcommand=team_scrollbar.set)
        
        # Risk assessment
        risk_frame = tk.LabelFrame(parent_frame, text="Risk Assessment", 
                                 font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        risk_frame.pack(fill="x", pady=10)
        
        self.include_risks = tk.BooleanVar(value=True)
        risk_check = tk.Checkbutton(risk_frame, text="Include Risk Assessment", 
                                  variable=self.include_risks, bg="white")
        risk_check.pack(anchor="w", pady=5)
        
    def setup_financial_form(self, parent_frame):
        # Department selection
        dept_frame = tk.LabelFrame(parent_frame, text="Department", 
                                 font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        dept_frame.pack(fill="x", pady=10)
        
        # Fetch departments from database
        departments = ["All Departments"]
        query = "SELECT DISTINCT department FROM employees"
        result = self.db.execute_query(query)
        if result:
            for row in result:
                if 'department' in row and row['department']:
                    departments.append(row['department'])
        
        self.dept_var = tk.StringVar(value="All Departments")
        
        dept_dropdown = ttk.Combobox(dept_frame, textvariable=self.dept_var, 
                                   values=departments, state="readonly", width=30)
        dept_dropdown.pack(anchor="w", pady=5)
        
        # Financial metrics
        metrics_frame = tk.LabelFrame(parent_frame, text="Financial Metrics", 
                                    font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        metrics_frame.pack(fill="x", pady=10)
        
        # Create checkboxes for metrics
        self.include_revenue = tk.BooleanVar(value=True)
        revenue_check = tk.Checkbutton(metrics_frame, text="Include Revenue", 
                                     variable=self.include_revenue, bg="white")
        revenue_check.pack(anchor="w", pady=2)
        
        self.include_expenses = tk.BooleanVar(value=True)
        expenses_check = tk.Checkbutton(metrics_frame, text="Include Expenses", 
                                      variable=self.include_expenses, bg="white")
        expenses_check.pack(anchor="w", pady=2)
        
        self.include_profit = tk.BooleanVar(value=True)
        profit_check = tk.Checkbutton(metrics_frame, text="Include Profit/Loss", 
                                    variable=self.include_profit, bg="white")
        profit_check.pack(anchor="w", pady=2)
        
        self.include_budget_variance = tk.BooleanVar(value=True)
        budget_var_check = tk.Checkbutton(metrics_frame, text="Include Budget Variance", 
                                        variable=self.include_budget_variance, bg="white")
        budget_var_check.pack(anchor="w", pady=2)
        
        # Salary information
        salary_frame = tk.LabelFrame(parent_frame, text="Salary Information", 
                                   font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        salary_frame.pack(fill="x", pady=10)
        
        self.include_salary = tk.BooleanVar(value=True)
        salary_check = tk.Checkbutton(salary_frame, text="Include Salary Details", 
                                    variable=self.include_salary, bg="white")
        salary_check.pack(anchor="w", pady=5)
        
        self.include_benefits = tk.BooleanVar(value=True)
        benefits_check = tk.Checkbutton(salary_frame, text="Include Benefits (Medical, Conveyance, etc.)", 
                                      variable=self.include_benefits, bg="white")
        benefits_check.pack(anchor="w", pady=5)
        
        self.include_deductions = tk.BooleanVar(value=True)
        deductions_check = tk.Checkbutton(salary_frame, text="Include Deductions (PF, etc.)", 
                                        variable=self.include_deductions, bg="white")
        deductions_check.pack(anchor="w", pady=5)
        
        # Comparison options
        comparison_frame = tk.LabelFrame(parent_frame, text="Comparison Options", 
                                       font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        comparison_frame.pack(fill="x", pady=10)
        
        self.compare_previous = tk.BooleanVar(value=True)
        compare_check = tk.Checkbutton(comparison_frame, text="Compare with Previous Period", 
                                     variable=self.compare_previous, bg="white")
        compare_check.pack(anchor="w", pady=2)
        
        self.compare_yoy = tk.BooleanVar(value=True)
        yoy_check = tk.Checkbutton(comparison_frame, text="Year-over-Year Comparison", 
                                 variable=self.compare_yoy, bg="white")
        yoy_check.pack(anchor="w", pady=2)
        
    def setup_custom_form(self, parent_frame):
        # Custom report fields
        fields_frame = tk.LabelFrame(parent_frame, text="Report Fields", 
                                   font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        fields_frame.pack(fill="x", pady=10)
        
        # Available fields
        available_frame = tk.Frame(fields_frame, bg="white")
        available_frame.pack(fill="x", pady=5)
        
        available_label = tk.Label(available_frame, text="Available Fields:", 
                                 font=("Helvetica", 10), bg="white")
        available_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.available_listbox = tk.Listbox(available_frame, height=8, width=30, selectmode=tk.MULTIPLE)
        self.available_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        # Get database fields
        available_fields = []
        
        # Employee fields
        query = "SHOW COLUMNS FROM employees"
        emp_columns = self.db.execute_query(query)
        if emp_columns:
            for col in emp_columns:
                available_fields.append(f"Employee: {col['Field']}")
        
        # Salary fields
        query = "SHOW COLUMNS FROM employee_salary"
        salary_columns = self.db.execute_query(query)
        if salary_columns:
            for col in salary_columns:
                if col['Field'] != 'emp_id' and col['Field'] != 'emp_name':  # Skip duplicates
                    available_fields.append(f"Salary: {col['Field']}")
        
        # If no database fields, use sample fields
        if not available_fields:
            available_fields = [
                "Employee Name",
                "Employee ID",
                "Department",
                "Position",
                "Hire Date",
                "Salary",
                "Performance Rating",
                "Training Hours",
                "Projects Completed",
                "Attendance Rate",
                "Overtime Hours",
                "Leave Balance",
                "Skills",
                "Certifications"
            ]
        
        for field in available_fields:
            self.available_listbox.insert(tk.END, field)
        
        # Buttons to move fields
        buttons_frame = tk.Frame(available_frame, bg="white")
        buttons_frame.grid(row=1, column=1, padx=10, pady=5)
        
        add_button = tk.Button(buttons_frame, text=">>", 
                             command=self.add_field)
        add_button.pack(pady=5)
        
        remove_button = tk.Button(buttons_frame, text="<<", 
                                command=self.remove_field)
        remove_button.pack(pady=5)
        
        # Selected fields
        selected_label = tk.Label(available_frame, text="Selected Fields:", 
                                font=("Helvetica", 10), bg="white")
        selected_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        self.selected_listbox = tk.Listbox(available_frame, height=8, width=30, selectmode=tk.MULTIPLE)
        self.selected_listbox.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        
        # Add some default selected fields
        default_selected = [
            "Employee: name",
            "Employee: emp_id",
            "Employee: doj",
            "Salary: base_pay"
        ]
        
        for field in default_selected:
            if field in available_fields:
                self.selected_listbox.insert(tk.END, field)
                idx = available_fields.index(field)
                self.available_listbox.delete(idx)
        
        # Filters
        filters_frame = tk.LabelFrame(parent_frame, text="Filters", 
                                    font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        filters_frame.pack(fill="x", pady=10)
        
        # Add filter button
        add_filter_button = tk.Button(filters_frame, text="Add Filter", 
                                    font=("Helvetica", 10), bg="#f0f2f5",
                                    command=self.add_filter)
        add_filter_button.pack(anchor="w", pady=5)
        
        # Filter list
        self.filters_frame = tk.Frame(filters_frame, bg="white")
        self.filters_frame.pack(fill="x", pady=5)
        
        # Add a sample filter
        self.add_sample_filter()
        
        # Sorting
        sorting_frame = tk.LabelFrame(parent_frame, text="Sorting", 
                                    font=("Helvetica", 12, "bold"), bg="white", padx=10, pady=10)
        sorting_frame.pack(fill="x", pady=10)
        
        sort_field_frame = tk.Frame(sorting_frame, bg="white")
        sort_field_frame.pack(fill="x", pady=5)
        
        sort_field_label = tk.Label(sort_field_frame, text="Sort By:", 
                                  font=("Helvetica", 10), bg="white")
        sort_field_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.sort_field_var = tk.StringVar(value="Employee: name")
        sort_fields = ["Employee: name", "Employee: emp_id", "Employee: doj", "Salary: base_pay"]
        
        sort_field_dropdown = ttk.Combobox(sort_field_frame, textvariable=self.sort_field_var, 
                                         values=sort_fields, state="readonly", width=20)
        sort_field_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        sort_order_label = tk.Label(sort_field_frame, text="Order:", 
                                  font=("Helvetica", 10), bg="white")
        sort_order_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        self.sort_order_var = tk.StringVar(value="Ascending")
        sort_orders = ["Ascending", "Descending"]
        
        sort_order_dropdown = ttk.Combobox(sort_field_frame, textvariable=self.sort_order_var, 
                                         values=sort_orders, state="readonly", width=15)
        sort_order_dropdown.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
    def toggle_employee_selection(self):
        if self.all_employees.get():
            self.employee_selection_frame.pack_forget()
        else:
            self.employee_selection_frame.pack(fill="x", pady=5)
    
    def add_field(self):
        selected_indices = self.available_listbox.curselection()
        for i in reversed(selected_indices):
            field = self.available_listbox.get(i)
            self.selected_listbox.insert(tk.END, field)
            self.available_listbox.delete(i)
    
    def remove_field(self):
        selected_indices = self.selected_listbox.curselection()
        for i in reversed(selected_indices):
            field = self.selected_listbox.get(i)
            self.available_listbox.insert(tk.END, field)
            self.selected_listbox.delete(i)
    
    def add_filter(self):
        filter_frame = tk.Frame(self.filters_frame, bg="white")
        filter_frame.pack(fill="x", pady=2)
        
        # Field selection
        fields = []
        
        # Get fields from database
        query = "SHOW COLUMNS FROM employees"
        emp_columns = self.db.execute_query(query)
        if emp_columns:
            for col in emp_columns:
                fields.append(f"Employee: {col['Field']}")
        
        query = "SHOW COLUMNS FROM employee_salary"
        salary_columns = self.db.execute_query(query)
        if salary_columns:
            for col in salary_columns:
                if col['Field'] != 'emp_id' and col['Field'] != 'emp_name':  # Skip duplicates
                    fields.append(f"Salary: {col['Field']}")
        
        # If no database fields, use sample fields
        if not fields:
            fields = ["Employee Name", "Department", "Position", "Hire Date", "Salary", "Performance Rating"]
        
        field_var = tk.StringVar(value=fields[0])
        field_dropdown = ttk.Combobox(filter_frame, textvariable=field_var, 
                                    values=fields, state="readonly", width=15)
        field_dropdown.grid(row=0, column=0, padx=2, pady=2)
        
        # Operator selection
        operators = ["equals", "contains", "greater than", "less than", "between"]
        operator_var = tk.StringVar(value=operators[0])
        operator_dropdown = ttk.Combobox(filter_frame, textvariable=operator_var, 
                                       values=operators, state="readonly", width=10)
        operator_dropdown.grid(row=0, column=1, padx=2, pady=2)
        
        # Value entry
        value_entry = tk.Entry(filter_frame, width=15)
        value_entry.grid(row=0, column=2, padx=2, pady=2)
        
        # Remove button
        remove_button = tk.Button(filter_frame, text="X", 
                                command=lambda: filter_frame.destroy())
        remove_button.grid(row=0, column=3, padx=2, pady=2)
    
    def add_sample_filter(self):
        filter_frame = tk.Frame(self.filters_frame, bg="white")
        filter_frame.pack(fill="x", pady=2)
        
        # Field selection
        fields = []
        
        # Get fields from database
        query = "SHOW COLUMNS FROM employees"
        emp_columns = self.db.execute_query(query)
        if emp_columns:
            for col in emp_columns:
                fields.append(f"Employee: {col['Field']}")
        
        query = "SHOW COLUMNS FROM employee_salary"
        salary_columns = self.db.execute_query(query)
        if salary_columns:
            for col in salary_columns:
                if col['Field'] != 'emp_id' and col['Field'] != 'emp_name':  # Skip duplicates
                    fields.append(f"Salary: {col['Field']}")
        
        # If no database fields, use sample fields
        if not fields:
            fields = ["Employee Name", "Department", "Position", "Hire Date", "Salary", "Performance Rating"]
            field_var = tk.StringVar(value="Department")
        else:
            field_var = tk.StringVar(value=fields[0])
        
        field_dropdown = ttk.Combobox(filter_frame, textvariable=field_var, 
                                    values=fields, state="readonly", width=15)
        field_dropdown.grid(row=0, column=0, padx=2, pady=2)
        
        # Operator selection
        operators = ["equals", "contains", "greater than", "less than", "between"]
        operator_var = tk.StringVar(value="equals")
        operator_dropdown = ttk.Combobox(filter_frame, textvariable=operator_var, 
                                       values=operators, state="readonly", width=10)
        operator_dropdown.grid(row=0, column=1, padx=2, pady=2)
        
        # Value entry
        value_entry = tk.Entry(filter_frame, width=15)
        value_entry.insert(0, "IT")
        value_entry.grid(row=0, column=2, padx=2, pady=2)
        
        # Remove button
        remove_button = tk.Button(filter_frame, text="X", 
                                command=lambda: filter_frame.destroy())
        remove_button.grid(row=0, column=3, padx=2, pady=2)
    
    def add_holiday(self):
        # Create a simple dialog to add a holiday
        holiday_dialog = tk.Toplevel(self.root)
        holiday_dialog.title("Add Holiday")
        holiday_dialog.geometry("300x150")
        holiday_dialog.configure(bg="white")
        
        # Date selection
        date_frame = tk.Frame(holiday_dialog, bg="white")
        date_frame.pack(fill="x", pady=10, padx=20)
        
        date_label = tk.Label(date_frame, text="Date:", bg="white")
        date_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        date_entry = DateEntry(date_frame, width=12, background='#1877f2',
                             foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Holiday name
        name_frame = tk.Frame(holiday_dialog, bg="white")
        name_frame.pack(fill="x", pady=10, padx=20)
        
        name_label = tk.Label(name_frame, text="Holiday Name:", bg="white")
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        name_entry = tk.Entry(name_frame, width=20)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Add button
        add_button = tk.Button(holiday_dialog, text="Add Holiday", bg="#1877f2", fg="white",
                             command=lambda: self.save_holiday(date_entry.get(), name_entry.get(), holiday_dialog))
        add_button.pack(pady=10)
    
    def save_holiday(self, date, name, dialog):
        if date and name:
            self.holiday_listbox.insert(tk.END, f"{date}: {name}")
            dialog.destroy()
        else:
            messagebox.showerror("Error", "Please enter both date and holiday name.")
    
    def toggle_email_options(self):
        if self.send_email.get():
            self.email_options_frame.pack(fill="x", pady=5)
        else:
            self.email_options_frame.pack_forget()
    
    def set_today(self):
        today = datetime.now()
        self.start_date.set_date(today)
        self.end_date.set_date(today)
    
    def set_yesterday(self):
        yesterday = datetime.now() - timedelta(days=1)
        self.start_date.set_date(yesterday)
        self.end_date.set_date(yesterday)
    
    def set_last_7_days(self):
        today = datetime.now()
        last_week = today - timedelta(days=6)
        self.start_date.set_date(last_week)
        self.end_date.set_date(today)
    
    def set_last_30_days(self):
        today = datetime.now()
        last_month = today - timedelta(days=29)
        self.start_date.set_date(last_month)
        self.end_date.set_date(today)
    
    def set_this_month(self):
        today = datetime.now()
        first_day = today.replace(day=1)
        self.start_date.set_date(first_day)
        self.end_date.set_date(today)
    
    def set_last_month(self):
        today = datetime.now()
        first_day_this_month = today.replace(day=1)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        first_day_last_month = last_day_last_month.replace(day=1)
        self.start_date.set_date(first_day_last_month)
        self.end_date.set_date(last_day_last_month)
    
    def generate_chart_preview(self, parent_frame, report_type):
        # Clear previous chart if any
        for widget in parent_frame.winfo_children():
            if isinstance(widget, tk.Button):
                continue
            widget.destroy()
        
        # Create figure and axis
        fig = plt.Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Generate sample data based on report type
        if report_type == "attendance":
            self.generate_attendance_chart(ax)
        elif report_type == "turnover":
            self.generate_turnover_chart(ax)
        elif report_type == "progress":
            self.generate_progress_chart(ax)
        elif report_type == "financial":
            self.generate_financial_chart(ax)
        else:  # custom
            self.generate_custom_chart(ax)
        
        # Set chart title
        ax.set_title(self.chart_title_entry.get())
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def generate_attendance_chart(self, ax):
        # Sample data
        chart_type = self.chart_type.get()
        
        # Try to get real data from database
        attendance_data = None
        try:
            # This is a simplified example - in a real app, you would have an attendance table
            # Here we're using present_days from employee_salary as a proxy
            query = """
            SELECT emp_name, present_days 
            FROM employee_salary 
            ORDER BY emp_name
            LIMIT 5
            """
            attendance_data = self.db.execute_query(query)
        except Exception as e:
            print(f"Error fetching attendance data: {e}")
        
        if attendance_data and len(attendance_data) > 0:
            if chart_type == "bar":
                names = [row['emp_name'] for row in attendance_data]
                present = [row['present_days'] for row in attendance_data]
                # Assuming working days in a month is 22
                absent = [22 - row['present_days'] for row in attendance_data]
                
                x = np.arange(len(names))
                width = 0.35
                
                ax.bar(x - width/2, present, width, label='Present')
                ax.bar(x + width/2, absent, width, label='Absent')
                
                ax.set_xlabel('Employee')
                ax.set_ylabel('Days')
                ax.set_xticks(x)
                ax.set_xticklabels(names, rotation=45, ha='right')
                ax.legend()
                
            elif chart_type == "pie":
                total_present = sum(row['present_days'] for row in attendance_data)
                total_absent = len(attendance_data) * 22 - total_present  # Assuming 22 working days
                
                labels = ['Present', 'Absent']
                sizes = [total_present, total_absent]
                
                # ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                sizes = [max(0, value) for value in sizes]  # Prevent negative values
                if sum(sizes) == 0:  # If all values are zero, provide default values
                    sizes = [1] * len(labels)

                ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

                ax.axis('equal')
                
            else:  # line, area, scatter
                names = [row['emp_name'] for row in attendance_data]
                present = [row['present_days'] for row in attendance_data]
                
                if chart_type == "line":
                    ax.plot(names, present, marker='o')
                elif chart_type == "area":
                    ax.fill_between(np.arange(len(names)), present)
                    ax.set_xticks(np.arange(len(names)))
                    ax.set_xticklabels(names, rotation=45, ha='right')
                else:  # scatter
                    ax.scatter(np.arange(len(names)), present)
                    ax.set_xticks(np.arange(len(names)))
                    ax.set_xticklabels(names, rotation=45, ha='right')
                
                ax.set_xlabel('Employee')
                ax.set_ylabel('Present Days')
        else:
            # Use sample data if no database data
            if chart_type == "bar":
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
                present = [42, 40, 45, 39, 41]
                absent = [3, 5, 0, 6, 4]
                late = [2, 3, 3, 2, 3]
                
                x = np.arange(len(days))
                width = 0.25
                
                ax.bar(x - width, present, width, label='Present')
                ax.bar(x, absent, width, label='Absent')
                ax.bar(x + width, late, width, label='Late')
                
                ax.set_xlabel('Day of Week')
                ax.set_ylabel('Number of Employees')
                ax.set_xticks(x)
                ax.set_xticklabels(days)
                ax.legend()
                
            elif chart_type == "pie":
                labels = ['Present', 'Absent', 'Late']
                sizes = [85, 10, 5]
                
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                
            elif chart_type == "line":
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
                attendance_rate = [93, 89, 95, 87, 91]
                
                ax.plot(days, attendance_rate, marker='o')
                ax.set_xlabel('Day of Week')
                ax.set_ylabel('Attendance Rate (%)')
                ax.set_ylim([80, 100])
                
            else:  # area or scatter
                days = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
                attendance = np.array([92, 94, 91, 88, 90, 85, 87, 89, 92, 95, 93, 91, 90, 89, 88, 92, 94, 95, 93, 91])
                
                if chart_type == "area":
                    ax.fill_between(days, attendance)
                    ax.set_xlabel('Day of Month')
                    ax.set_ylabel('Attendance Rate (%)')
                    ax.set_ylim([80, 100])
                else:  # scatter
                    ax.scatter(days, attendance)
                    ax.set_xlabel('Day of Month')
                    ax.set_ylabel('Attendance Rate (%)')
                    ax.set_ylim([80, 100])
    
    def generate_financial_chart(self, ax):
        # Sample data
        chart_type = self.chart_type.get()
        
        # Try to get real data from database
        salary_data = None
        try:
            query = """
            SELECT emp_name, base_pay, medical, conveyance, pf, net_salary 
            FROM employee_salary 
            ORDER BY emp_name
            LIMIT 5
            """
            salary_data = self.db.execute_query(query)
        except Exception as e:
            print(f"Error fetching salary data: {e}")
        
        if salary_data and len(salary_data) > 0:
            if chart_type == "bar":
                names = [row['emp_name'] for row in salary_data]
                base_pay = [float(row['base_pay']) for row in salary_data]
                net_salary = [float(row['net_salary']) for row in salary_data]
                
                x = np.arange(len(names))
                width = 0.35
                
                ax.bar(x - width/2, base_pay, width, label='Base Pay')
                ax.bar(x + width/2, net_salary, width, label='Net Salary')
                
                ax.set_xlabel('Employee')
                ax.set_ylabel('Amount ($)')
                ax.set_xticks(x)
                ax.set_xticklabels(names, rotation=45, ha='right')
                ax.legend()
                
            elif chart_type == "pie":
                # Calculate total for each component
                total_base = sum(float(row['base_pay']) for row in salary_data)
                total_medical = sum(float(row['medical']) for row in salary_data)
                total_conveyance = sum(float(row['conveyance']) for row in salary_data)
                total_pf = sum(float(row['pf']) for row in salary_data)
                
                labels = ['Base Pay', 'Medical', 'Conveyance', 'PF']
                sizes = [total_base, total_medical, total_conveyance, total_pf]
                
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                
            else:  # line, area, scatter
                names = [row['emp_name'] for row in salary_data]
                base_pay = [float(row['base_pay']) for row in salary_data]
                net_salary = [float(row['net_salary']) for row in salary_data]
                
                if chart_type == "line":
                    ax.plot(names, base_pay, marker='o', label='Base Pay')
                    ax.plot(names, net_salary, marker='s', label='Net Salary')
                    # ax.set_xticklabels(names, rotation=45, ha='right')
                    ax.set_xticks(range(len(names)))  # Set fixed tick positions
                    ax.set_xticklabels(names, rotation=45, ha='right')  # Now safe to use

                    ax.legend()
                elif chart_type == "area":
                    ax.fill_between(np.arange(len(names)), base_pay, alpha=0.5, label='Base Pay')
                    ax.fill_between(np.arange(len(names)), net_salary, alpha=0.5, label='Net Salary')
                    ax.set_xticks(np.arange(len(names)))
                    ax.set_xticklabels(names, rotation=45, ha='right')
                    ax.legend()
                else:  # scatter
                    ax.scatter(np.arange(len(names)), base_pay, label='Base Pay')
                    ax.scatter(np.arange(len(names)), net_salary, label='Net Salary')
                    ax.set_xticks(np.arange(len(names)))
                    ax.set_xticklabels(names, rotation=45, ha='right')
                    ax.legend()
                
                ax.set_xlabel('Employee')
                ax.set_ylabel('Amount ($)')
        else:
            # Use sample data if no database data
            if chart_type == "bar":
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
                revenue = [120000, 135000, 128000, 142000, 150000, 165000]
                expenses = [95000, 102000, 98000, 105000, 110000, 115000]
                
                x = np.arange(len(months))
                width = 0.35
                
                ax.bar(x - width/2, revenue, width, label='Revenue')
                ax.bar(x + width/2, expenses, width, label='Expenses')
                
                ax.set_xlabel('Month')
                ax.set_ylabel('Amount ($)')
                ax.set_xticks(x)
                ax.set_xticklabels(months)
                ax.legend()
                
            elif chart_type == "pie":
                labels = ['Salaries', 'Marketing', 'Operations', 'IT', 'R&D', 'Other']
                sizes = [45, 15, 20, 10, 5, 5]
                
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                
            elif chart_type == "line":
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
                revenue = [120000, 135000, 128000, 142000, 150000, 165000]
                expenses = [95000, 102000, 98000, 105000, 110000, 115000]
                profit = [r - e for r, e in zip(revenue, expenses)]
                
                ax.plot(months, revenue, marker='o', label='Revenue')
                ax.plot(months, expenses, marker='s', label='Expenses')
                ax.plot(months, profit, marker='^', label='Profit')
                ax.set_xlabel('Month')
                ax.set_ylabel('Amount ($)')
                ax.legend()
                
            else:  # area or scatter
                quarters = ['Q1-2022', 'Q2-2022', 'Q3-2022', 'Q4-2022', 'Q1-2023', 'Q2-2023']
                revenue = [350000, 380000, 410000, 450000, 420000, 460000]
                expenses = [280000, 300000, 320000, 350000, 330000, 350000]
                
                if chart_type == "area":
                    ax.fill_between(np.arange(len(quarters)), revenue, label='Revenue', alpha=0.5)
                    ax.fill_between(np.arange(len(quarters)), expenses, label='Expenses', alpha=0.5)
                    ax.set_xlabel('Quarter')
                    ax.set_ylabel('Amount ($)')
                    ax.set_xticks(np.arange(len(quarters)))
                    ax.set_xticklabels(quarters)
                    ax.legend()
                else:  # scatter
                    ax.scatter(np.arange(len(quarters)), revenue, label='Revenue')
                    ax.scatter(np.arange(len(quarters)), expenses, label='Expenses')
                    ax.set_xlabel('Quarter')
                    ax.set_ylabel('Amount ($)')
                    ax.set_xticks(np.arange(len(quarters)))
                    ax.set_xticklabels(quarters)
                    ax.legend()
    
    def generate_turnover_chart(self, ax):
        # For turnover chart, we'll use sample data since we don't have a turnover table
        chart_type = self.chart_type.get()
        
        if chart_type == "bar":
            departments = ['IT', 'HR', 'Finance', 'Marketing', 'Sales']
            hires = [5, 2, 3, 4, 6]
            terminations = [2, 1, 2, 3, 4]
            
            x = np.arange(len(departments))
            width = 0.35
            
            ax.bar(x - width/2, hires, width, label='New Hires')
            ax.bar(x + width/2, terminations, width, label='Terminations')
            
            ax.set_xlabel('Department')
            ax.set_ylabel('Number of Employees')
            ax.set_xticks(x)
            ax.set_xticklabels(departments)
            ax.legend()
            
        elif chart_type == "pie":
            labels = ['Voluntary', 'Involuntary', 'Retirement', 'End of Contract']
            sizes = [45, 25, 15, 15]
            
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            
        elif chart_type == "line":
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            turnover_rate = [2.5, 3.1, 2.8, 3.2, 2.9, 3.5]
            
            ax.plot(months, turnover_rate, marker='o')
            ax.set_xlabel('Month')
            ax.set_ylabel('Turnover Rate (%)')
            
        else:  # area or scatter
            quarters = ['Q1-2022', 'Q2-2022', 'Q3-2022', 'Q4-2022', 'Q1-2023', 'Q2-2023']
            turnover = [2.8, 3.2, 3.5, 3.0, 2.7, 3.1]
            
            if chart_type == "area":
                ax.fill_between(np.arange(len(quarters)), turnover)
                ax.set_xlabel('Quarter')
                ax.set_ylabel('Turnover Rate (%)')
                ax.set_xticks(np.arange(len(quarters)))
                ax.set_xticklabels(quarters)
            else:  # scatter
                ax.scatter(np.arange(len(quarters)), turnover)
                ax.set_xlabel('Quarter')
                ax.set_ylabel('Turnover Rate (%)')
                ax.set_xticks(np.arange(len(quarters)))
                ax.set_xticklabels(quarters)
    
    def generate_progress_chart(self, ax):
        # For progress chart, we'll use sample data since we don't have a progress table
        chart_type = self.chart_type.get()
        
        if chart_type == "bar":
            milestones = ['Planning', 'Design', 'Development', 'Testing', 'Deployment']
            completed = [100, 85, 60, 30, 10]
            
            ax.bar(milestones, completed, color='#1877f2')
            ax.set_xlabel('Project Milestone')
            ax.set_ylabel('Completion (%)')
            ax.set_ylim([0, 100])
            
            # Add completion percentage labels
            for i, v in enumerate(completed):
                ax.text(i, v + 3, f"{v}%", ha='center')
            
        elif chart_type == "pie":
            labels = ['Completed', 'In Progress', 'Not Started']
            sizes = [45, 35, 20]
            
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            
        elif chart_type == "line":
            weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6']
            actual_progress = [15, 28, 42, 53, 67, 75]
            planned_progress = [10, 25, 40, 55, 70, 85]
            
            ax.plot(weeks, actual_progress, marker='o', label='Actual')
            ax.plot(weeks, planned_progress, marker='s', linestyle='--', label='Planned')
            ax.set_xlabel('Timeline')
            ax.set_ylabel('Progress (%)')
            ax.set_ylim([0, 100])
            ax.legend()
            
        else:  # area or scatter
            tasks = ['Task 1', 'Task 2', 'Task 3', 'Task 4', 'Task 5', 'Task 6', 'Task 7', 'Task 8']
            completion = [100, 100, 85, 70, 60, 40, 20, 0]
            
            if chart_type == "area":
                ax.fill_between(np.arange(len(tasks)), completion, alpha=0.5)
                ax.set_xlabel('Tasks')
                ax.set_ylabel('Completion (%)')
                ax.set_xticks(np.arange(len(tasks)))
                ax.set_xticklabels(tasks, rotation=45)
                ax.set_ylim([0, 100])
            else:  # scatter
                ax.scatter(np.arange(len(tasks)), completion)
                ax.set_xlabel('Tasks')
                ax.set_ylabel('Completion (%)')
                ax.set_xticks(np.arange(len(tasks)))
                ax.set_xticklabels(tasks, rotation=45)
                ax.set_ylim([0, 100])
    
    def generate_custom_chart(self, ax):
        # For custom chart, we'll try to use data from the selected fields
        chart_type = self.chart_type.get()
        
        # Try to get real data from database
        try:
            # Get selected fields
            selected_fields = []
            for i in range(self.selected_listbox.size()):
                field = self.selected_listbox.get(i)
                selected_fields.append(field)
            
            # If we have employee and salary fields, we can generate a chart
            if selected_fields and len(selected_fields) >= 2:
                # For simplicity, we'll use the first two fields
                field1 = selected_fields[0]
                field2 = selected_fields[1]
                
                # Extract table and column names
                table1, col1 = field1.split(': ') if ': ' in field1 else ('Employee', field1)
                table2, col2 = field2.split(': ') if ': ' in field2 else ('Employee', field2)
                
                # Adjust table names
                table1 = 'employees' if table1 == 'Employee' else 'employee_salary'
                table2 = 'employees' if table2 == 'Employee' else 'employee_salary'
                
                # Build query
                if table1 == table2:
                    query = f"SELECT {col1}, {col2} FROM {table1} LIMIT 5"
                else:
                    query = f"""
                    SELECT e.{col1}, s.{col2} 
                    FROM employees e
                    JOIN employee_salary s ON e.emp_id = s.emp_id
                    LIMIT 5
                    """
                
                # Execute query
                data = self.db.execute_query(query)
                
                if data and len(data) > 0:
                    # Extract data
                    x_values = [row[col1] for row in data]
                    y_values = [float(row[col2]) if isinstance(row[col2], (int, float, str)) and row[col2] is not None else 0 for row in data]
                    
                    # Generate chart
                    if chart_type == "bar":
                        ax.bar(x_values, y_values, color='#1877f2')
                        ax.set_xlabel(col1)
                        ax.set_ylabel(col2)
                        ax.set_xticklabels(x_values, rotation=45, ha='right')
                        
                    elif chart_type == "pie":
                        ax.pie(y_values, labels=x_values, autopct='%1.1f%%', startangle=90)
                        ax.axis('equal')
                        
                    elif chart_type == "line":
                        ax.plot(x_values, y_values, marker='o')
                        ax.set_xlabel(col1)
                        ax.set_ylabel(col2)
                        ax.set_xticklabels(x_values, rotation=45, ha='right')
                        
                    else:  # area or scatter
                        if chart_type == "area":
                            ax.fill_between(np.arange(len(x_values)), y_values, alpha=0.5)
                        else:  # scatter
                            ax.scatter(np.arange(len(x_values)), y_values)
                        
                        ax.set_xlabel(col1)
                        ax.set_ylabel(col2)
                        ax.set_xticks(np.arange(len(x_values)))
                        ax.set_xticklabels(x_values, rotation=45, ha='right')
                    
                    return
        except Exception as e:
            print(f"Error generating custom chart: {e}")
        
        # If we couldn't generate a chart from database, use sample data
        if chart_type == "bar":
            categories = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']
            values = [45, 32, 67, 28, 53]
            
            ax.bar(categories, values, color='#1877f2')
            ax.set_xlabel('Category')
            ax.set_ylabel('Value')
            
        elif chart_type == "pie":
            labels = ['Segment 1', 'Segment 2', 'Segment 3', 'Segment 4']
            sizes = [35, 25, 20, 20]
            
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            
        elif chart_type == "line":
            x = np.arange(10)
            y = [12, 14, 18, 23, 28, 35, 41, 48, 55, 61]
            
            ax.plot(x, y, marker='o')
            ax.set_xlabel('X Axis')
            ax.set_ylabel('Y Axis')
            
        else:  # area or scatter
            x = np.arange(10)
            y = [12, 14, 18, 23, 28, 35, 41, 48, 55, 61]
            
            if chart_type == "area":
                ax.fill_between(x, y, alpha=0.5)
                ax.set_xlabel('X Axis')
                ax.set_ylabel('Y Axis')
            else:  # scatter
                ax.scatter(x, y)
                ax.set_xlabel('X Axis')
                ax.set_ylabel('Y Axis')
    
    def generate_report(self, report_type):
        # Get report parameters
        title = self.report_title_entry.get()
        start_date = self.start_date.get()
        end_date = self.end_date.get()
        
        # Validate inputs
        if not title:
            messagebox.showerror("Error", "Please enter a report title.")
            return
        
        # Show progress dialog
        progress_dialog = tk.Toplevel(self.root)
        progress_dialog.title("Generating Report")
        progress_dialog.geometry("300x150")
        progress_dialog.configure(bg="white")
        
        progress_label = tk.Label(progress_dialog, text="Generating report...", 
                                font=("Helvetica", 12), bg="white")
        progress_label.pack(pady=20)
        
        progress_bar = ttk.Progressbar(progress_dialog, orient="horizontal", 
                                     length=200, mode="determinate")
        progress_bar.pack(pady=10)
        
        # Simulate progress
        for i in range(101):
            progress_bar["value"] = i
            progress_dialog.update()
            time.sleep(0.02)
        
        # Close progress dialog
        progress_dialog.destroy()
        
        # Generate PDF report
        if self.output_format.get() == "pdf":
            file_path = self.generate_pdf_report(report_type, title, start_date, end_date)
            
            # Save to database if selected
            if self.save_to_db.get() and file_path:
                self.save_report_to_database(report_type, title, file_path)
        
        # Send email if selected
        if self.send_email.get():
            self.send_report_email(report_type, title, file_path)
        
        # Show success message
        messagebox.showinfo("Success", f"{report_type.title()} report generated successfully!")
        
        # Return to main screen
        self.back_to_main()
    
    def save_report_to_database(self, report_type, title, file_path):
        try:
            # Read the PDF file as binary data
            with open(file_path, 'rb') as file:
                pdf_data = file.read()
            
            # Get employee ID if specific employee report
            # emp_id = None
            date_created = datetime.now().strftime('%Y-%m-%d') 
            name = self.username_entry.get().strip()  # Get name from entry field

            query = "SELECT emp_id FROM employees WHERE name = %s"
            params = (name,)  # Parameterized query to prevent SQL injection

            result = self.db.execute_query(query, params)

            if result:
                emp_id = result[0]['emp_id']  # Extract emp_id from the result
                
            else:
                print("Employee not found")

            if hasattr(self, 'employee_listbox') and not self.all_employees.get():
                selected = self.employee_listbox.curselection()
                if selected:
                    emp_info = self.employee_listbox.get(selected[0])
                    emp_id = emp_info.split(':')[0].strip()
            
            # if not emp_id:
            #     # Use a default employee ID for company-wide reports
            #     emp_id = "COMP001"
            
            # Insert into salary_slips table
            query = "INSERT INTO reports (emp_id, pdf_file,report_type,created_date,created_by) VALUES (%s, %s,%s,%s,%s)"
            self.db.execute_query(query, (emp_id, pdf_data,report_type,date_created,name), fetch=False)
            
            messagebox.showinfo("Database", "Report saved to database successfully!")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save report to database: {e}")
            print(f"Error saving to database: {e}")
    
    def generate_pdf_report(self, report_type, title, start_date, end_date):
        # Ask user where to save the file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            initialfile=f"{report_type}_report_{datetime.now().strftime('%Y%m%d')}.pdf"
        )
        
        if not file_path:
            return None
        
        # Create PDF document
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Add title
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Title'],
            fontSize=18,
            alignment=1,
            spaceAfter=12
        )
        elements.append(Paragraph(title, title_style))
        
        # Add date range
        date_style = ParagraphStyle(
            'Date',
            parent=styles['Normal'],
            fontSize=12,
            alignment=1,
            spaceAfter=12
        )
        elements.append(Paragraph(f"Period: {start_date} to {end_date}", date_style))
        
        # Add report description
        if hasattr(self, 'report_desc_entry') and self.report_desc_entry.get("1.0", tk.END).strip():
            desc_style = ParagraphStyle(
                'Description',
                parent=styles['Normal'],
                fontSize=10,
                alignment=0,
                spaceAfter=12
            )
            elements.append(Paragraph(self.report_desc_entry.get("1.0", tk.END), desc_style))
        
        # Add spacer
        elements.append(Spacer(1, 12))
        
        # Add chart
        fig = plt.Figure(figsize=(6, 3), dpi=100)
        ax = fig.add_subplot(111)
        
        # Generate chart based on report type
        if report_type == "attendance":
            self.generate_attendance_chart(ax)
        elif report_type == "turnover":
            self.generate_turnover_chart(ax)
        elif report_type == "progress":
            self.generate_progress_chart(ax)
        elif report_type == "financial":
            self.generate_financial_chart(ax)
        else:  # custom
            self.generate_custom_chart(ax)
        
        # Set chart title
        ax.set_title(self.chart_title_entry.get())
        
        # Save chart to buffer
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        
        # Add chart to PDF
        # img = Image(buf, width=450, height=250)
        # elements.append(img)
        img = Image.open(buf)  # Use .open() instead of calling Image like a function
        img = img.resize((450, 250))  # Resize if needed

        # Add spacer
        elements.append(Spacer(1, 12))
        
        # Add table with data based on report type
        data = []
        
        if report_type == "attendance":
            # Try to get real data from database
            try:
                # Header row
                data.append(["Employee ID", "Name", "Present Days", "Absent Days", "Attendance Rate"])
                
                # Get employee data
                query = """
                SELECT e.emp_id, e.name, s.present_days
                FROM employees e
                JOIN employee_salary s ON e.emp_id = s.emp_id
                ORDER BY e.name
                LIMIT 10
                """
                employees = self.db.execute_query(query)
                
                if employees:
                    for emp in employees:
                        # Assuming 22 working days in a month
                        present_days = emp['present_days'] if emp['present_days'] is not None else 0
                        absent_days = 22 - present_days
                        attendance_rate = f"{(present_days / 22 * 100):.1f}%"
                        
                        data.append([
                            emp['emp_id'],
                            emp['name'],
                            str(present_days),
                            str(absent_days),
                            attendance_rate
                        ])
            except Exception as e:
                print(f"Error fetching attendance data: {e}")
                # Use sample data if database query fails
                data = [
                    ["Employee ID", "Name", "Present Days", "Absent Days", "Attendance Rate"],
                    ["EMP001", "John Smith", "20", "1", "95%"],
                    ["EMP002", "Sarah Johnson", "21", "0", "98%"],
                    ["EMP003", "Michael Brown", "19", "2", "90%"],
                    ["EMP004", "Emily Davis", "18", "3", "86%"],
                    ["EMP005", "Robert Wilson", "21", "0", "100%"]
                ]
            
        elif report_type == "financial":
            # Try to get real data from database
            try:
                # Header row
                data.append(["Employee ID", "Name", "Base Pay", "Medical", "Conveyance", "PF", "Net Salary"])
                
                # Get salary data
                query = """
                SELECT e.emp_id, e.name, s.base_pay, s.medical, s.conveyance, s.pf, s.net_salary
                FROM employees e
                JOIN employee_salary s ON e.emp_id = s.emp_id
                ORDER BY e.name
                LIMIT 10
                """
                salaries = self.db.execute_query(query)
                
                if salaries:
                    for salary in salaries:
                        data.append([
                            salary['emp_id'],
                            salary['name'],
                            f"${float(salary['base_pay']):.2f}",
                            f"${float(salary['medical']):.2f}",
                            f"${float(salary['conveyance']):.2f}",
                            f"${float(salary['pf']):.2f}",
                            f"${float(salary['net_salary']):.2f}"
                        ])
            except Exception as e:
                print(f"Error fetching salary data: {e}")
                # Use sample data if database query fails
                data = [
                    ["Employee ID", "Name", "Base Pay", "Medical", "Conveyance", "PF", "Net Salary"],
                    ["EMP001", "John Smith", "$5,000.00", "$500.00", "$300.00", "$600.00", "$5,200.00"],
                    ["EMP002", "Sarah Johnson", "$6,000.00", "$600.00", "$350.00", "$720.00", "$6,230.00"],
                    ["EMP003", "Michael Brown", "$4,500.00", "$450.00", "$250.00", "$540.00", "$4,660.00"],
                    ["EMP004", "Emily Davis", "$5,500.00", "$550.00", "$320.00", "$660.00", "$5,710.00"],
                    ["EMP005", "Robert Wilson", "$7,000.00", "$700.00", "$400.00", "$840.00", "$7,260.00"]
                ]
        else:
            # For other report types, use sample data
            if report_type == "turnover":
                data = [
                    ["Department", "Headcount", "New Hires", "Terminations", "Turnover Rate"],
                    ["IT", "45", "5", "2", "4.4%"],
                    ["HR", "15", "2", "1", "6.7%"],
                    ["Finance", "30", "3", "2", "6.7%"],
                    ["Marketing", "25", "4", "3", "12.0%"],
                    ["Sales", "50", "6", "4", "8.0%"]
                ]
            elif report_type == "progress":
                data = [
                    ["Milestone", "Planned Completion", "Actual Completion", "Status", "Variance"],
                    ["Planning", "100%", "100%", "Completed", "0%"],
                    ["Design", "100%", "85%", "In Progress", "-15%"],
                    ["Development", "75%", "60%", "In Progress", "-15%"],
                    ["Testing", "50%", "30%", "In Progress", "-20%"],
                    ["Deployment", "25%", "10%", "In Progress", "-15%"]
                ]
            else:  # custom
                # Try to get data from selected fields
                try:
                    # Get selected fields
                    selected_fields = []
                    for i in range(self.selected_listbox.size()):
                        field = self.selected_listbox.get(i)
                        selected_fields.append(field)
                    
                    if selected_fields:
                        # Header row
                        data.append(selected_fields)
                        
                        # Build query based on selected fields
                        query_parts = []
                        for field in selected_fields:
                            table, col = field.split(': ') if ': ' in field else ('Employee', field)
                            table = 'employees' if table == 'Employee' else 'employee_salary'
                            query_parts.append(f"{table}.{col}")
                        
                        query = f"""
                        SELECT {', '.join(query_parts)}
                        FROM employees
                        JOIN employee_salary ON employees.emp_id = employee_salary.emp_id
                        LIMIT 10
                        """
                        
                        results = self.db.execute_query(query)
                        
                        if results:
                            for row in results:
                                data_row = []
                                for field in selected_fields:
                                    table, col = field.split(': ') if ': ' in field else ('Employee', field)
                                    data_row.append(str(row[col]))
                                data.append(data_row)
                    else:
                        # Default custom report
                        data = [
                            ["Category", "Value 1", "Value 2", "Value 3", "Total"],
                            ["Category A", "45", "32", "18", "95"],
                            ["Category B", "36", "28", "22", "86"],
                            ["Category C", "52", "41", "33", "126"],
                            ["Category D", "29", "17", "14", "60"],
                            ["Category E", "38", "25", "19", "82"]
                        ]
                except Exception as e:
                    print(f"Error fetching custom report data: {e}")
                    # Default custom report
                    data = [
                        ["Category", "Value 1", "Value 2", "Value 3", "Total"],
                        ["Category A", "45", "32", "18", "95"],
                        ["Category B", "36", "28", "22", "86"],
                        ["Category C", "52", "41", "33", "126"],
                        ["Category D", "29", "17", "14", "60"],
                        ["Category E", "38", "25", "19", "82"]
                    ]
        
        # Create table
        table = Table(data)
        
        # Style the table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        table.setStyle(style)
        
        # Add table to elements
        elements.append(table)
        
        # Add spacer
        elements.append(Spacer(1, 12))
        
        # Add footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            alignment=1,
            textColor=colors.gray
        )
        elements.append(Paragraph(f"Generated by Employee Report Generator on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", footer_style))
        
        # Build PDF
        doc.build(elements)
        
        return file_path
    
    def send_report_email(self, report_type, title, file_path=None):
        # Get email parameters
        recipients = self.email_to_entry.get()
        subject = self.email_subject_entry.get()
        body = self.email_body_entry.get("1.0", tk.END)
        
        # Validate inputs
        if not recipients:
            messagebox.showerror("Error", "Please enter at least one recipient email address.")
            return
        
        # In a real application, you would use smtplib to send the email with the attachment
        # For this example, we'll just show a mock email sent dialog
        messagebox.showinfo("Email Sent", f"Report '{title}' has been sent to {recipients}.")
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Validate inputs
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return
        
        # Check credentials against database
        try:
            # Hash the password (in a real app, you would use a more secure method)
            hashed_password = hashlib.md5(password.encode()).hexdigest()
            
            # Query the database
            query = "SELECT id, username FROM users WHERE username = %s AND password = %s"
            result = self.db.execute_query(query, (username, password))
            
            if result and len(result) > 0:
                # User found
                user_id = result[0]['id']
                username = result[0]['username']
                
                # Create user object
                self.current_user = User(user_id, username, role="admin")  # Assuming admin role for simplicity
                
                # Show main screen
                self.show_main()
                return
            else:
                # Invalid credentials
                messagebox.showerror("Error", "Invalid username or password.")
        except Exception as e:
            print(f"Login error: {e}")
            # Fallback to sample users if database connection fails
            sample_users = [
                {"username": "admin", "password": "admin123"},
                {"username": "john", "password": "john123"},
                {"username": "sarah", "password": "sarah123"}
            ]
            
            for user in sample_users:
                if user["username"] == username and user["password"] == password:
                    self.current_user = User(1, username, role="admin")
                    self.show_main()
                    return
            
            messagebox.showerror("Error", "Invalid username or password.")
    
    def logout(self):
        # self.current_user = None
        # self.show_login()
         root.destroy()  # Close home.py window
         subprocess.run(["python", "home.py"])  # Open main.py

    
    def show_login(self):
        self.main_frame.pack_forget()
        self.report_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)
    
    def show_main(self):
        self.login_frame.pack_forget()
        self.report_frame.pack_forget()
        
        # Setup main UI if not already set up
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.setup_main_ui()
        
        self.main_frame.pack(fill="both", expand=True)
    
    def show_register(self):
       
        root.destroy()
        subprocess.run(["python","signup.py"])
    
    def open_report_form(self, report_type):
        self.login_frame.pack_forget()
        self.main_frame.pack_forget()
        
        # Setup report form
        self.setup_report_form(report_type)
        
        self.report_frame.pack(fill="both", expand=True)
    
    def back_to_main(self):
        self.report_frame.pack_forget()
        self.show_main()

if __name__ == "__main__":
    root = tk.Tk()
    app = ReportApp(root)
    root.mainloop()