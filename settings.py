#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Global variables (but leave out logger functions)"""

__author__ = "Anna Buch, TU Berlin"
__email__ = "anna.buch@tu-berlin.de"


from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
import subprocess



# local or remote machine 
hostname = subprocess.run(['hostname'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()



class Settings(BaseSettings):

    # paths
    PATH_SRC: str = "./src"
    ## store logs and data outside of the repository
    PATH_LOGS: str = "../logs/"
    PATH_DATA: str = "../data/"
    PATH_EVALUATION: str = PATH_DATA + 'evaluation/'


    #  Define data paths 
    PATH_PROMPTS: Path = Path("./prompt_templates/")

    PATH_LLM_DATA: Path = Path(PATH_DATA + "llm_outputs/")
    LLM_DATA_FILENAME: str = "llm_1_simple.csv" 

    HF_TOKEN: str
    model_config = SettingsConfigDict(env_file=".env")  # load HF_TOKEN from .env file

    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50



    # if hostname == "a-buch-ThinkPad-X1-Extreme-Gen-4i":
    #     print("Running on local machine")
  
    #     # HF directory
    #     HF_HOME_DIR: str = "/home/a-buch/Documents/TUB_DWN/_PROJECTS/CI-impacts-information-retrieval/notebooks/huggingface_mirror/hub"
    #     HF_TOKEN_PATH: str = "/home/a-buch/Documents/TUB_DWN/_PROJECTS/CI-impacts-information-retrieval/notebooks/huggingface_mirror/token"
        
    #     # settings for CUDA and PYTORCH
    #     os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
    #     os.environ["CUDA_VISIBLE_DEVICES"]="0"   #  nvidia gpu
    #     os.environ["PYTORCH_CUDA_ALLOC_CONF"]="expandable_segments:True" ## improve memory allocation

    #     # settings for distributed computing
    #     os.environ["WORLD_SIZE"]="1"
    #     os.environ["RANK"]="0"
    #     os.environ["LOCAL_RANK"]="0"


    # else:
    #     print("Running on TUB Cluster")
    #     HF_HOME_DIR: str = "/beegfs/home/users/a/a-buch/_PROJECTS/CI-impacts-information-retrieval/notebooks/huggingface_mirror/hub"
    #     HF_TOKEN_PATH: str = "/beegfs/home/users/a/a-buch/_PROJECTS/CI-impacts-information-retrieval/notebooks/huggingface_mirror/token"


settings = Settings()