# Board-Level Reliability (BLR) Simulator Dashboard

This project is a Python Streamlit web dashboard for evaluating semiconductor Board-Level Reliability (BLR). It reads thermal simulation data, calculates the Process Capability Index (CpK), displays Design of Experiments (DOE) scatter plots, and automatically generates an 8D Problem Solving Report if the process limits are breached.

## Local Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Generate the mock thermal simulation data:
   ```bash
   python simulate_data.py
   ```

3. Run the Streamlit Dashboard:
   ```bash
   streamlit run app.py
   ```

## Deployment

**Note on Vercel:** Vercel is designed for serverless functions (like Next.js or Flask) and does not natively support Streamlit because Streamlit requires WebSockets and a long-running server. 

For the best experience, and to put a live link on your resume, it is highly recommended to deploy this on **Streamlit Community Cloud** or **Render**.

### Option 1: Deploying to Streamlit Community Cloud (Recommended)

1. **Push to GitHub**:
   - Initialize a git repository in this folder: `git init`
   - Add all files: `git add .`
   - Commit: `git commit -m "Initial commit"`
   - Go to [GitHub](https://github.com/), create a new repository, and push your code following their instructions.
2. **Deploy**:
   - Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
   - Click "New app".
   - Select your newly created repository, the branch (`main` or `master`), and set the Main file path to `app.py`.
   - Click "Deploy!". Within a few minutes, you will have a public URL to put on your resume.

### Option 2: Deploying to Render
1. Push your code to GitHub as described above.
2. Go to [Render](https://render.com/) and create a new "Web Service".
3. Connect your GitHub repository.
4. Set the build command to `pip install -r requirements.txt`.
5. Set the start command to `streamlit run app.py --server.port $PORT`.
6. Click "Create Web Service".
