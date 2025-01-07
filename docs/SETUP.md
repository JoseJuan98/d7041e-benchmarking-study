# Setup

## Python environment

### Make installation

Make installation is optional, but it is a good tool to have in your system. It is a build automation tool that can be
used to install dependencies, run tests, etc.

- For Windows execute `winget install GnuWin32.Make` in the PowerShell and then add `C:\Program Files (x86)\GnuWin32\bin` 
(or where it has been installed) to the `PATH` in the system environment variables.
- For MacOS execute `brew install make` in the terminal.
- For Linux, it should be already installed.

### Using make


- Install the dependencies:

```bash
make init
```


### Using poetry

```bash
pip install poetry
poetry install
```

### Using pip

- Download [python3.13](https://www.python.org/downloads/) (or other version we will use) if you don't have it.
- Install virtualenv or any other virtual env manager tool of your preference:

```bash
pip install --no-cache-dir virtualenv
```

- Create the python virtual env pointing to your python3.13 binary/.exe file:

```bash
python -m virtualenv .venv --python="C:\Program Files\python3.13\python.exe"
```

If you have the computer in Swedish the path where python is installed can be slightly different.

- Activate the environment and install the dependencies

```bash
# windows
.venv/Scripts/activate

# Linux/macOS
source .venv/bin/activate

# install depedencies
pip install -e .[dev]
```

### venv Activiation

If conda was used to create the environment, it created a virtual environment called `aai-benchmarking-study`. To activate it:

```bash
conda activate aai-benchmarking-study
```

Otherwise, use the following command to activate the virtual environment:

```bash
# windows
.venv/Scripts/activate

# Linux/macOS
source .venv/bin/activate
```

## Automatic formating on save

After install via conda or installing the `dev-requirements.txt`

Then go to settings and just type black and select the same settings as:

![](attachments/black_on_save.png)

Now every time that you save a file, it will be automatically formatted to black style.

## Docstring style

Got to settings, search for `docstring` and in dosctring format select Google:

![](attachments/change_docstring_style.png)
