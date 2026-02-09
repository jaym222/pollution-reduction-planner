CMSC 150 Project

**Greenvale City Pollution Reduction Planner**

**1. Introduction **
    a. Objective 
        The Greenvale City Pollution Reduction Planner serves as a strategic 
        decision-making tool for the City of Greenvale. Its main goal is to help the city council 
        decide how many units of each mitigation project option should be implemented to meet the 
        annual reduction target of each priority pollutant. 
    b. Specification of the Problem 
        Greenvale City is required by the national government to drastically reduce 10 
        major pollutants, but each pollutant has its own minimum reduction target that must be 
        met. Although the city has 30 mitigation options available, each project can only be 
        implemented at most 20 units, which makes it difficult to determine the best combination.  
    c. Solution 
        The Pollution Reduction Planner uses the Simplex minimization method to 
        compute the most cost-efficient combination of mitigation projects that still meets all 
        required pollutant reduction targets.  
**2. Prerequisites **
    Hardware :Basic computer with standard processing power (Window, Mac, Linux). 
    Software: Installed Python, Custom Tkinter, and Numpy 
    Moreover, the application relies on the following modules. To install them, run these 
    commands in your command prompt: 
    pip install tkinter                             
    pip install customtkinter                
    pip install numpy                            
**4. How to Run **
    1. Download JJMBaez_CMSC150Project.zip and extract it to your preferred directory. 
    2. Open Command Prompt and change directory. Use cd -yourpreferedfiledirectory-  
    (e.g cd Documents\BaezProject) 
    3. Run the main by the input python main.py 
    4. The system will display the application and you may maximize the window. 

**5. How to Use **
  **Selecting Projects **
    On the left frame, you'll see the Mitigation Projects. This displays all available pollution 
    reduction options with their costs. 
      ● Select Projects: Click any project checkbox to select it.  
      o Checked: The project is SELECTED and will be included in the calculation. 
      o Unchecked: The project is EXCLUDED. 
      ● Bulk Controls: Use the "Select All" button to choose all projects at once, or "Reset" 
      to deselect everything. 
  **Optimization **
  Once you're satisfied with your selection, click the Minimize button at the bottom of the 
  frame to calculate the optimal solution. 
  Reading Results 
    On the right frame , you’ll see the Minimization Results. This displays the results of the 
    minimization including the projects that has more than 1 unit after optimization (column 1), 
    the required units (column 2), and the total cost of each projects (column 3). 
    Switch to the Iteration Results tab to view detailed updates in iterations. 
       ** ● Initial Tableau: **·  Displays the raw mathematical matrix (simplex tableau) 
      representing the constraints before solving. Shows the initial setup with constraint 
      coefficients and values. 
        **● Iteration (i) :** Displays the updated tableau after an iteration in simplex is applied. It 
      includes the slacks, additional, decision variables, Z and RHS 
        **● Basic Solution:**  Shows the final optimal solution after an iteration completes. 
      Moreover, the last basic solution table indicates how many units(x1-x30) of each 
      project to implement for minimum cost while meeting pollution reduction targets. 
**6. Troubleshooting **
  **Issue:** No Selection 
  **Reason:** You likely clicked Minimize without selecting any project. 
  **Fix:** Select at least one project. 
  
  **Issue:** Optimization Error 
  **Reason:** The project you selected do not have enough combined capacity to meet 
  one or more pollutant targets. 
  **Fix:** Select all mitigation projects or manually select possible combination projects 
  that will meet the target of each pollutants.
