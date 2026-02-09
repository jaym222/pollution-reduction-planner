import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from simplex import Simplex, readAndBuild

#main window
window = ctk.CTk(fg_color="#F2EDE5")
window.geometry('1300x700')
window.title("City Pollution Reduction Plan")
ctk.set_default_color_theme("green")

#=====header===================================================================================
header_frame = ctk.CTkFrame(window, fg_color="#2D7868", height=100, corner_radius=0)
header_frame.pack(fill="x", pady=0)
header_frame.pack_propagate(False)

title_label = ctk.CTkLabel(
    header_frame,
    text=f"Greenvale City Pollution Reduction Planner",
    font=("Poppins", 38, "bold"),
    text_color="white" 
)
title_label.pack(pady=10, side="top", padx=10)

subtitle_label = ctk.CTkLabel( header_frame, 
                              text=f"Welcome!", 
                              font=("Poppins", 18), 
                              text_color="white" ) 
subtitle_label.pack()
#======tabs====================================================================
my_tab = ctk.CTkTabview(window, fg_color="#2D7868" )
my_tab.pack(expand=True, fill="both", pady=(0,5), padx=10)

my_tab.add("Mitigation Projects")
my_tab.add("Iteration Results")
my_tab.set("Mitigation Projects") #initially in tabn 1

my_tab1 = my_tab.tab("Mitigation Projects")
my_tab2 = my_tab.tab("Iteration Results")

#=====frames in tab 1=====================================================================
mitigation_frame = ctk.CTkFrame(my_tab1, fg_color="#2D7868")
mitigation_frame.pack(side=tk.LEFT, fill="y", padx=10, pady=10)
mitigation_frame.configure(width=600)
mitigation_frame.pack_propagate(False)

mitigation_projects = ctk.CTkScrollableFrame(
    mitigation_frame, 
    label_text="Mitigation Projects",
    label_fg_color="#64B39A",
    label_font=("Poppins", 14), 
    fg_color="#F2EDE5",
    corner_radius=10,
    border_color="#F2EDE5"
)
mitigation_projects.pack(fill="both", expand=True, padx=10, pady=10, side=tk.TOP)

#button container under mitigation projects
button_container = ctk.CTkFrame(mitigation_frame, fg_color="transparent", height=50)
button_container.pack(fill="x", padx=10, pady=(0, 5))
button_container.pack_propagate(False)

#right side
results = ctk.CTkScrollableFrame(
    my_tab1, 
    width=700, 
    label_text="Minimization Results",
    label_fg_color="#64B39A",
    label_font=("Poppins", 14), 
    fg_color="#F2EDE5",
    corner_radius=10,
    border_color="#F2EDE5"
)
results.pack(fill="both", padx=10, pady=19, side=tk.RIGHT)

#=============frame in iteration (tab 2)==========================================
#parent frame of each iterations
iteration_frame = ctk.CTkScrollableFrame(
    my_tab2,
    width=500,
    fg_color="#2D7868"
)
iteration_frame.pack(fill="both", expand=True, padx=10, pady=10)

#======display checkbox projects========================================================================
project_data = [
    ["Large Solar Park", 4000],
    ["Small Solar Installations", 1200],
    ["Wind Farm", 3800],
    ["Gas-to-renewables conversion", 3200],
    ["Boiler Retrofit", 1400],
    ["Catalytic Converters for Buses", 2600],
    ["Diesel Bus Replacement", 5000],
    ["Traffic Signal/Flow Upgrade", 1000],
    ["Low-Emission Stove Program", 180],
    ["Residential Insulation/Efficiency", 900],
    ["Industrial Scrubbers", 4200],
    ["Waste Methane Capture System", 3600],
    ["Landfill Gas-to-energy", 3400],
    ["Reforestation (acre-package)", 220],
    ["Urban Tree Canopy Program (street trees)", 300],
    ["Industrial Energy Efficiency Retrofit", 1600],
    ["Natural Gas Leak Repair", 1800],
    ["Agricultural Methane Reduction", 2800],
    ["Clean Cookstove & Fuel Switching (community scale)", 450],
    ["Rail Electrification", 6000],
    ["EV Charging Infrastructure", 2200],
    ["Biochar for soils (per project unit)", 1400],
    ["Industrial VOC", 2600],
    ["Heavy-Duty Truck Retrofit", 4200],
    ["Port/Harbor Electrification", 4800],
    ["Black Carbon reduction", 600],
    ["Wetlands restoration", 1800],
    ["Household LPG conversion program", 700],
    ["Industrial process change", 5000],
    ["Behavioral demand-reduction program", 400],
]

checkbox_val = {} #container for boolean value of each checkbox {index, bool}
checkbox_widgets = {} #checkbox container {index, widget}

#create checkboxes
for i, row in enumerate(project_data):
    checkbox_val[i] = tk.BooleanVar(value=False) #initially set not selected
    
    row_frame = ctk.CTkFrame(mitigation_projects, fg_color="#F2EDE5")
    row_frame.pack(fill="x", padx=5, pady=5)
    
    checkbox = ctk.CTkCheckBox(
        row_frame,
        text=f"{row[0]} (${row[1]})", #display prjoect name and cost
        variable=checkbox_val[i],
        onvalue=True, #true when check
        offvalue=False #flase when uncheck
    )
    checkbox.pack(side="left", fill="x", expand=True)
    checkbox_widgets[i] = checkbox 

#======display iterations==========================================================================
#tableaus, frame parent frame for iterations, iteration title
def show_tableau(tableau, parent_frame, title_text, basic_solution=None):

    if tableau is None or len(tableau) == 0:
        return

    rows = len(tableau)
    num_constraints = rows - 1  #number of constraint rows or project selected

    #create a frame for this each tableau with iteration title
    tableau_container = ctk.CTkScrollableFrame(parent_frame, 
                                               fg_color="#F2EDE5", 
                                               corner_radius=10, 
                                               orientation="horizontal",
                                               label_text=title_text,
                                               label_fg_color="#64B39A",
                                               height=200,
                                               label_font=("Poppins", 14))
    tableau_container.pack(fill="both", expand=True, padx=10, pady=10)
    
    #container frame to hold treeview + scrollbars
    container = tk.Frame(tableau_container, bg="#F2EDE5")
    container.pack(fill="both", expand=True, padx=10, pady=10)
    
    headings = [] #container for column headings
    
    #slack variables
    for i in range(1, 11 + num_constraints):
        headings.append(f"s{i}")
    
    #decision variables
    for i in range(1, num_constraints + 1):
        headings.append(f"x{i}")
    
    #Z nad RHS column
    headings.append("Z")
    headings.append("RHS")

    #create table
    tree = ttk.Treeview(container, columns=headings, show="headings", height=15)
    tree.pack(side=tk.LEFT, fill="both", expand=True, pady=0)

    #vertical scrollbar
    vsb = tk.Scrollbar(container, orient="vertical", command=tree.yview)
    vsb.pack(side=tk.RIGHT, fill="y")
    tree.configure(yscrollcommand=vsb.set)

    #horizontal scrollbar
    hsb = tk.Scrollbar(container, orient="horizontal", command=tree.xview)
    hsb.pack(fill="x")
    tree.configure(xscrollcommand=hsb.set)

    #setup headings and column widths
    for j, col_id in enumerate(headings):
        heading_text = headings[j] 
        tree.heading(col_id, text=heading_text, anchor="center")
        tree.column(col_id, width=110, anchor="center", stretch=False)

    #insert elements in rows (4 decimal point)
    for i, row in enumerate(tableau):
        formatted = [] #container for vvalues
        for val in row:
            formatted.append(f"{float(val):.4f}")
        tree.insert("", "end", values=formatted) #insert in table
        
    #====Display Basic Solution=================================================================
    if basic_solution is not None:
        basic_container = ctk.CTkScrollableFrame(parent_frame,
                                fg_color="#F2EDE5",
                                orientation="horizontal",
                                corner_radius=10,
                                label_text="Basic Solution",
                                label_fg_color="#64B39A",
                                label_font=("Poppins", 14),
                                label_anchor="w",
                                height=50)
        basic_container.pack(fill="x", padx=10, pady=(0, 0))

        #container for table
        basic_table_frame = tk.Frame(basic_container, bg="#F2EDE5")
        basic_table_frame.pack(fill="x", padx=10, pady=10)

        #create headings without RHS col
        basic_headings = headings[:-1]  
        
        #create table
        basic_tree = ttk.Treeview(
            basic_table_frame,
            columns=basic_headings,
            show="headings",
            height=1
        )
        basic_tree.pack(fill="x", pady=0)

        #setup headings removed RHS
        for j, col_id in enumerate(basic_headings):
            heading_text = basic_headings[j] 
            basic_tree.heading(col_id, text=heading_text, anchor="center")
            basic_tree.column(col_id, width=110, anchor="center", stretch=False)

        #format the basic solution array 
        formatted_basic = [f"{float(val):.4f}" for val in basic_solution]
            
        #last element of rhs in tableau
        z_value = tableau[-1, -1] 
        formatted_basic[-1] = f"{float(z_value):.2f}" #append at last element
        basic_tree.insert("", "end", values=formatted_basic) #insert at bottom

#============table for final result=============================================================
#reulst from simplex, minimization result frame
def final_results(result_data, parent_frame):
    #clear previous results
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    #create container for the table
    table_container = tk.Frame(parent_frame, bg="#F2EDE5")
    table_container.pack(fill="both", expand=True, padx=10, pady=0)
    
    #columns titles
    columns = ("project", "units", "cost")

    #table style 
    style = ttk.Style()
    style.configure("Treeview", font=("Poppins", 14), rowheight=35, background="#F2EDE5", foreground="black")
    style.configure("Treeview.Heading", font=("Poppins", 18, "bold"), background="#F2EDE5")
    
    #create table
    tree = ttk.Treeview(table_container, columns=columns, show="headings", height=len(result_data)+1)
    tree.pack(side=tk.TOP, fill="both", expand=True)

    #headings
    tree.heading("project", text="Mitigation Project", anchor="w")
    tree.heading("units", text="Project Units", anchor="center")
    tree.heading("cost", text="Cost ($k)", anchor="e")
    
    #column widths and alignment
    tree.column("project", width=385, anchor="w")
    tree.column("units", width=130, anchor="center")
    tree.column("cost", width=100, anchor="e")
    
    #insert data rows
    total_cost = 0
    for project_name, units, cost in result_data:
        tree.insert("", "end", values=(
            project_name,
            f"{units:.2f}",
            f"{cost:,.2f}"
        ))
        total_cost += cost
    #total cost 
    tree.insert("", "end", values=("OPTIMAL COST", " ", f"${total_cost:,.2f}"), tags=("total"))
    
    #style of the total cost row
    tree.tag_configure("total", background="#64B39A", foreground="white", font=("Poppins", 20, "bold"))

#==========button_functions=======================================================================================
def minimize_clicked():
    #clear previous displays incase there is
    for widget in iteration_frame.winfo_children():
        widget.destroy()
    for widget in results.winfo_children():
        widget.destroy()

    #1. read and build the initial tableau
    tableau = readAndBuild(checkbox_val) 

    #get number of projects
    num_constraints = len(tableau) - 1 #exclude obj row
    try:
        #2. run Simplex and get results
        result = Simplex(tableau)
        
        #3. display all iterations
        iterations = result["iterations"]
        basicSolutions = result["iterBasicSolution"]
        is_infeasible = result.get("infeasible", False) 
        
        #display initial tableau with its basic solution
        show_tableau(iterations[0], iteration_frame, "Initial Tableau (Iteration 0)", basicSolutions[0])
        
        if is_infeasible:
            #if infeasible, display iteration tableau until where it stop 
            for i in range(1, len(iterations)):
                title = f"Iteration {i}"
                show_tableau(iterations[i], iteration_frame, title, basicSolutions[i])
            
            messagebox.showerror("Optimization Error", f"Minimization Unsuccessful!\n"
                           f"Infeasible combination of projects.\n"
                           f"It stops at iteration {len(iterations)-1}.\nPlease select another combination.")
            return tableau
        
        #if feasible, display iterations excluding final since getting of basic solution is different
        for i in range(1, len(iterations) - 1):
            title = f"Iteration {i}"
            show_tableau(iterations[i], iteration_frame, title, basicSolutions[i])

        #display the final tableau with the last row as basic solution (only when feasible)
        final_tableau = iterations[-1]
        final_basic_solution = final_tableau[-1, :-1]  #last row excluding RHS 
        show_tableau(final_tableau, iteration_frame, f"Final Tableau (Iteration {len(iterations)-1})", final_basic_solution)

        #prepare the needs in final table
        final_tableau = result["finalTableau"]#extract final tableau
        
        #define decision variables
        num_pollutants = 10
        num_slacks = num_constraints
        decision_var_start = num_pollutants + num_slacks
        decision_var_end = decision_var_start + num_constraints
        
        #get the units of rpojects
        decision_variables = final_tableau[-1, decision_var_start:decision_var_end]
        
        #4. display the results
        results_data = [] #prepare results data 
        total_optimized_cost = 0

        #slected project index
        selected_indices = []
        for i, proj in checkbox_val.items():
            if proj.get():  #if the checkbox is checked/true
                selected_indices.append(i)
        
        for i, selected_project_index in enumerate(selected_indices):
            project_info = project_data[selected_project_index] #get name(0) and cost(1) 
            project_name = project_info[0] #project name
            unit_cost = project_info[1]
            num_units = decision_variables[i] #num of units
            project_cost = num_units * unit_cost 
            total_optimized_cost += project_cost #total optimized cost or the RHS
            
            if num_units > 0: #include only those projects with greater than 0 units
                results_data.append((project_name, num_units, project_cost))
        
        #successful minimization
        messagebox.showinfo("Success", f"Optimization successfully computed!\n"f"Projects Selected: {num_constraints}\n")
        
        #display final results
        final_results(results_data, results)

    #if other errors occur/ in case there are any 
    except Exception as e:
        messagebox.showerror("Optimization Error", f"Minimization Unsuccessful.\nError: {str(e)}")
    
    return tableau

def reset_all():
    for i in checkbox_val: #for every checkbox boolean reset false
        checkbox_val[i].set(False)

def select_all():
    for i in checkbox_val: #for every checkbox bool set true
        checkbox_val[i].set(True)
#==========buttons===================================================================
btn_style = {
    "fg_color": "#64B39A",
    "text_color": "white",
    "corner_radius": 20,
    "height": 40,
    "border_color": "white",
    "border_width": 2,
}
compute = ctk.CTkButton(
    button_container, 
    text="Minimize", 
    command=minimize_clicked,
    hover_color= "#4A9A87",
    **btn_style,
    width=200,
    font= ("Poppins", 20, "bold")
)
compute.pack(pady=5, padx=0, side=tk.RIGHT) 

selectAll = ctk.CTkButton(
    button_container, 
    text="Select All", 
    command=select_all, 
    width=175,
    hover_color= "#4A9A87",
    **btn_style,
    font= ("Poppins", 12)
)
selectAll.pack(pady=5, padx=(0, 5), side=tk.LEFT)

reset = ctk.CTkButton(
    button_container, 
    text="Reset", 
    command=reset_all, 
    width= 175,
    hover_color="#C44536",
    **btn_style,
    font= ("Poppins", 12)
)
reset.pack(pady=5, padx=5, side=tk.LEFT)

window.mainloop() #run application