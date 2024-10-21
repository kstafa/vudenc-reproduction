# Vudenc Reproduction

A minimal reproduction of the Vudenc project.

Download the dataset from [here](https://zenodo.org/records/3559480/files/pythontraining_withString_X?download=1) and place it in the `w2v` folder.

### How to Run:

#### Step 1: Create a Virtual Environment

```bash
python -m venv venv
```

#### Step 2: Activate the Virtual Environment

- On macOS/Linux:

  ```bash
  source venv/bin/activate
  ```

- On Windows:

  ```bash
  venv\Scripts\activate
  ```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 4: Run the Project

Now you're ready to run the project. Follow the instructions in the main Python script to process the dataset and train the Word2Vec model.

#### Step 5: Deactivate the Virtual Environment

```bash
deactivate
```

