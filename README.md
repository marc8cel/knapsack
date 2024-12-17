# Knapsack Optimization App with Docker

This project contains a **Streamlit application** to solve the **Knapsack Optimization problem**.  
You can input values and weights for items, set a maximum capacity for the knapsack, and run the optimization to find the most valuable selection of items without exceeding the capacity.

---

### How to Run the Application with Docker

1. **Build the Docker Image**:  
   In the project directory, open a terminal and run the following command to build the Docker image:
   ```bash
   docker build -t knapsack-optimization .
  
2. **Run the Docker Container**
Once the image is built, run the container with:
   ```bash
    docker run -p 8501:8501 knapsack-optimization
   
4. **Access the Application**
Open your browser and go to http://localhost:8501 to access the app.

## Notes
The setup.py file is available in the repository but is not used. It caused issues during the installation of the GLPK solver, so we opted for a Docker setup that directly installs dependencies from requirements.txt and sets up the necessary environment.

Enjoy optimizing your knapsack!
