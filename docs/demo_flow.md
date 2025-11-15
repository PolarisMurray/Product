# BioReport Copilot - Demo Flow Guide

This guide walks you through how to run a live demo of the BioReport Copilot application. It's designed to be simple and clear, even if you're not familiar with bioinformatics or FastAPI.

## Prerequisites

Before starting, make sure you have:

- **Python 3.8+** installed
- **Node.js 16+** and **npm** installed
- The project files downloaded/cloned

## Step 1: Start the Backend Server

The backend is a FastAPI application that provides the API endpoints for analysis and report generation.

1. Open a terminal window
2. Navigate to the backend folder:
   ```bash
   cd backend
   ```
3. Install Python dependencies (first time only):
   ```bash
   pip install -r requirements.txt
   ```
4. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete.
```

**Keep this terminal window open** - the server needs to keep running.

The backend is now available at `http://localhost:8000`. You can verify it's working by opening `http://localhost:8000/docs` in your browser to see the API documentation.

## Step 2: Start the Frontend Application

The frontend is a React application that provides the user interface.

1. Open a **new terminal window** (keep the backend terminal running)
2. Navigate to the project root directory (where `package.json` is located):
   ```bash
   cd /path/to/Product
   ```
   (Replace with your actual project path)
3. Install frontend dependencies (first time only):
   ```bash
   npm install
   ```
   This may take a minute or two.
4. Start the frontend development server:
   ```bash
   npm run dev
   ```

You should see output like:
```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

5. Open your web browser and go to: `http://localhost:5173`

You should see the BioReport Copilot application with a header showing "BioReport Copilot" and two mode buttons: "Research Mode" and "Personal Genomics Mode".

---

## Demo Script: Research Mode

This demonstrates the research analysis feature for bioinformatics data.

### Step 1: Switch to Research Mode

- In the browser, click the **"Research Mode"** button at the top of the page (it should already be selected by default, but you can click it to make sure)

### Step 2: Fill in the Form

You'll see a form with several fields:

1. **Project Name** (optional): Enter something like "Demo Research Project"
2. **Species** (optional): Enter "Homo sapiens" or "Mus musculus"
3. **Contrast Label** (optional): Enter something like "Treatment vs Control"
4. **DEG File** (required): Click "Choose File" and select a CSV or TSV file containing differential expression data
   - For demo purposes, you can use any CSV file - the backend will accept it and return stub data
   - The file should have columns like gene names, log fold change, p-values, etc.
5. **Enrichment File** (optional): You can optionally upload an enrichment results file

### Step 3: Generate the Report

1. Click the **"Generate Report"** button
2. You'll see a loading spinner with "Analyzing..." text
3. After a few seconds, the analysis results will appear

### Step 4: View the Results

The results page will show:

1. **Success Message**: A green banner confirming "Analysis Complete"
2. **Visualizations Section**: 
   - Multiple plot cards showing:
     - Volcano Plot
     - PCA Analysis
     - Heatmap
     - Pathway Enrichment (if enrichment file was uploaded)
   - Each plot card shows the plot name, description, and the visualization image
3. **Narrative Sections**:
   - **Results** section: AI-generated text describing the findings
   - **Discussion** section: AI-generated interpretation and context
   - These appear side-by-side on larger screens
4. **Summary Statistics**:
   - A grid showing key numbers like:
     - Number of DEGs (differentially expressed genes)
     - Up-regulated genes count
     - Down-regulated genes count
     - Total genes analyzed

### Step 5: Export the Report

1. Scroll down to the bottom of the results
2. Click the **"Export Scientific Report (PDF)"** button
3. You'll see a loading spinner with "Exporting..." text
4. After a moment, a toast notification will appear showing:
   - "Report generated: /static/reports/research-{timestamp}.pdf"
5. The download URL is also logged to the browser console (open Developer Tools to see it)

**Note**: Currently, the backend returns a placeholder URL. In production, this would be a real downloadable file.

---

## Demo Script: Personal Genomics Mode

This demonstrates the personal genomics analysis feature for individual genetic data.

### Step 1: Switch to Personal Genomics Mode

- Click the **"Personal Genomics Mode"** button at the top of the page
- The page will switch to show the Personal Genomics interface

### Step 2: Enter SNP Data

**Note**: Currently, the Personal Genomics Mode page is a placeholder. The full form for entering SNPs and lifestyle data is coming soon. For now, you can demonstrate the export functionality if you have test data.

When the form is available, you would:

1. **Enter SNPs**: Add one or more SNP entries with:
   - **rsID**: The SNP identifier (e.g., "rs762551")
   - **Genotype**: The genotype value (e.g., "AA", "AG", "GG")
2. **Enter Lifestyle Factors** (optional):
   - Caffeine intake: "low", "moderate", or "high"
   - Exercise frequency: e.g., "3-4 times/week"
   - Sleep duration: Number of hours (e.g., 7.5)
   - Diet pattern: e.g., "Mediterranean"

### Step 3: Analyze the Genome

1. Click the **"Analyze My Genome"** button (or similar - exact label TBD)
2. The system will process the SNP data and generate insights

### Step 4: View the Results

The results page will show:

1. **Insight Cards**: 
   - Multiple cards, each showing:
     - Domain name (e.g., "Caffeine Metabolism")
     - Summary text explaining the finding
     - Score and percentile compared to peers
     - Personalized recommendations
2. **Peer Comparison Section**:
   - Metrics showing how the individual compares to the general population
   - Each metric shows value, percentile, and a label
3. **Genetic BioCard**:
   - A shareable card showing:
     - Title and subtitle
     - Badges (e.g., "Caffeine Analyzed", "Lactose Analyzed")
     - Key highlights
   - Includes buttons to copy summary or download as image

### Step 5: Export the Report (Optional)

1. Scroll down to find the **"Export Personal Genome Report (PDF)"** button
2. Click it to generate a PDF report
3. A toast notification will show the download URL

---

## Troubleshooting

### Backend won't start

- Make sure Python is installed: `python --version`
- Make sure you're in the `backend` directory
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Check if port 8000 is already in use

### Frontend won't start

- Make sure Node.js is installed: `node --version`
- Make sure npm is installed: `npm --version`
- Make sure you're in the project root (where `package.json` is)
- Try deleting `node_modules` and running `npm install` again

### Can't see the app in browser

- Make sure both backend and frontend are running
- Check that you're going to the correct URL: `http://localhost:5173`
- Check the browser console for errors (F12 → Console tab)
- Make sure the backend is accessible at `http://localhost:8000`

### API calls failing

- Verify the backend is running and accessible at `http://localhost:8000/health`
- Check the browser's Network tab (F12 → Network) to see the API requests
- Make sure CORS is properly configured (it should be set up already)

### Files won't upload

- Make sure you're selecting actual files (not folders)
- Check that the file format is supported (CSV, TSV, or XLSX)
- For demo purposes, any CSV file should work - the backend will accept it

---

## Tips for a Smooth Demo

1. **Prepare test files**: Have a few CSV files ready before the demo
2. **Test both modes**: Practice switching between Research and Personal modes
3. **Check console**: Open browser Developer Tools to see API calls and responses
4. **Keep terminals visible**: Have both terminal windows visible so you can show the server logs
5. **Explain what's happening**: As you click buttons, explain what the system is doing
6. **Highlight features**: Point out the auto-generated plots, AI narrative, and export functionality

---

## What's Next?

After the demo, you might want to:

- Explore the API documentation at `http://localhost:8000/docs`
- Check the code structure in `backend/routers/` and `src/pages/`
- Read the API contract in `docs/api_contract.md`
- Customize the stub data in the backend routers to show different results

---

## Quick Reference

**Backend:**
```bash
cd backend
uvicorn main:app --reload
```

**Frontend:**
```bash
npm install  # First time only
npm run dev
```

**URLs:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

