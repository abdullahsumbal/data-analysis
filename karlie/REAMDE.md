# Karlie's Application

## Getting Started

### Prerequisites

1. Install [anaconda](https://www.anaconda.com/distribution/).
2. step up python environment
    ```buildoutcfg
    conda create --name data-analysis python=3.7
    ``` 
3. activate environment
    ```buildoutcfg
    conda activate data-analysis
    ```

### Installation
Install required python libraries 
```buildoutcfg
conda install -c conda-forge --file requirements.txt
pip install -r requirements.txt

```
### Run Application (dev)
Run the following command on terminal
```buildoutcfg
python app.py
```
### Deploy Application
Run the following command on terminal
```buildoutcfg
pyinstaller --noconsole -n karlie  app.py
```