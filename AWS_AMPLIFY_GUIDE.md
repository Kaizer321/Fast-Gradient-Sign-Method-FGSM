# Click-by-Click AWS Amplify Guide

You have updated your code to point to the AWS Backend. Now we need to put that code on the internet.

## Part 1: Update GitHub (Vital!)

**AWS Amplify creates your site from your GitHub code.** If you don't put your local changes (the new IP address) on GitHub, Amplify will deploy the old version that points to `localhost`, and it won't work.

1.  **Open GitHub**: Go to your repository page (e.g., `https://github.com/Kaizer321/Fast-Gradient-Sign-Method-FGSM-`).
2.  **Navigate**: Click on the folder `frontend`, then `app`.
3.  **Upload**:
    *   Click **Add file** (top right of the file list) -> **Upload files**.
    *   Drag and drop your local `page.tsx` file (from `Assessment\frontend\app\page.tsx`) into the box.
    *   **Commit**: Scroll down, type "Update backend URL" in the box, and click the green **Commit changes** button.

## Part 2: AWS Amplify Deployment

1.  **Search**: Log in to AWS. In the top search bar, type `Amplify`.
2.  **Click**: Click **AWS Amplify** from the results.
3.  **Create**: Scroll down or look for the orange button **Create new app**.
    *   If you see "Host web app" or "Gen 1", choose that. (Sometimes checking "Build an app" -> "Host web app").
    *   *Goal*: We want "Amplify Hosting".
4.  **Source**: Select **GitHub** and click **Next**.
5.  **Authorize**:
    *   A window will pop up asking for permission.
    *   Click **Authorize AWS Amplify**.
    *   You might need to verify your GitHub password.
6.  **Select Repository**:
    *   **Repository**: Choose `Fast-Gradient-Sign-Method-FGSM-` from the dropdown.
    *   **Branch**: Select `main` (or `master`).
    *   Click **Next**.
7.  **Build Settings (Crucial Step)**:
    *   Amplify sees your repository root, but your app is inside the `frontend` folder.
    *   Look for a section called **App root** or **Monorepo settings** (it might be an "Edit" button next to the settings).
    *   **Click Edit**.
    *   Change the **App root** path from `/` to `frontend`.
    *   **Result**: Once you do this, Amplify should automatically update the build command to `npm run build` and the output directory to `.next`.
    *   If it doesn't auto-update, enter these manually:
        *   **Build command**: `npm run build`
        *   **Build output directory**: `.next`
    *   Click **Next**.
8.  **Review**: Click **Save and deploy**.

## Troubleshooting: "Build failed - package.json not found"

If you get an error saying `ENOENT: no such file or directory, open '.../package.json'`, it means Amplify is still looking in the wrong folder.

**The Fix (Force it to look in frontend):**

1.  In the Amplify Console, on the left menu, click **App settings** -> **Build settings**.
2.  Scroll down to **Build specification** (it shows code/YAML).
3.  Click **Edit**.
4.  Adding `cd frontend` to the commands is the safest fix. Replace the entire code with this:

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - cd frontend
        - npm ci
    build:
      commands:
        - cd frontend
        - npm run build
  artifacts:
    baseDirectory: frontend/.next
    files:
      - '**/*'
  cache:
    paths:
      - frontend/node_modules/**/*
```

5.  Click **Save**.
6.  Go back to the top of the page and click **Redeploy this version** (or go to the list of builds and click Redeploy).

## Part 3: Wait & Test

1.  **Watch**: You will see a list of steps: *Provision, Build, Deploy, Verify*.
2.  **Wait**: This takes about 3-5 minutes.
3.  **Success**: Once "Verify" is green, you will see a link like `https://main.d12345.amplifyapp.com`.
4.  **Click it**: Open the link.
5.  **Test**: Upload your `sample_7.png` (white digit on black background).
    *   Set Epsilon to 0.1.
    *   Click **Run Attack**.
    *   It should talk to your EC2 instance and show the result!
