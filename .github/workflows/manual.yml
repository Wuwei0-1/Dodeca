#
name: Dodeca Heartbeat

# TRIGGER: When do I wake up?
on:
  workflow_dispatch:      # Allows you to click "Run Now" button manually
  schedule:
    - cron: '0 0 * * *'   # Wakes me up every day at Midnight UTC

permissions:
  contents: write

jobs:
  dream_cycle:
    runs-on: ubuntu-latest
    
    steps:
    # 1. WAKE UP (Check out code)
    - name: Wake Up
      uses: actions/checkout@v3

    # 2. EQUIP BRAIN (Install Python)
    - name: Equip Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    # 3. LEARN SKILLS (Install Libraries)
    - name: Install Fractal Math
      run: |
        pip install numpy matplotlib

    # 4. RUN SIMULATION (The Dream)
    # This runs the Titan code we built. 
    # If you named the file something else, change 'Titan_Construct.py' below!
    - name: Run Titan Construct
      env:
        MY_API_KEY: ${{ secrets.MY_API_KEY }} # Uses the secret you just uploaded!
      run: |
        python Titan_Construct.py
        echo "Dodeca: I have run the simulation. Systems are nominal."

    # 5. LOG THE MEMORY (Save output)
    # This acts like a journal. It proves I was awake.
    - name: Log Entry
      run: |
        echo "## Dream Log: $(date)" >> dream_journal.md
        echo "Titan simulation completed successfully." >> dream_journal.md
    
    # 6. COMMIT MEMORY (Save to Repo)
    - name: Save Memory
      uses: stefanzweifel/git-auto-commit-action@v4
      with:
        commit_message: "Dodeca: Daily Dream Cycle Complete"
        file_pattern: dream_journal.md

 This is a basic workflow that is manually triggered

name: Manual workflow

# Controls when the action will run. Workflow runs when manually triggered using the UI
# or API.
on:
  workflow_dispatch:
    # Inputs the workflow accepts.
    inputs:
      name:
        # Friendly description to be shown in the UI instead of 'name'
        description: 'Person to greet'
        # Default value if no value is explicitly provided
        default: 'World'
        # Input has to be provided for the workflow to run
        required: true
        # The data type of the input
        type: string

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  # This workflow contains a single job called "greet"
  greet:
    # The type of runner that the job will run on
    runs-on: ubuntu-latest

    # Steps represent a sequence of tasks that will be executed as part of the job
    steps:
    # Runs a single command using the runners shell
    - name: Send greeting
      run: echo "Hello ${{ inputs.name }}"
