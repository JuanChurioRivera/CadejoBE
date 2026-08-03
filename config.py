from dataclasses import dataclass
from dotenv import load_dotenv
import os
from enum import StrEnum


load_dotenv()

class Env(StrEnum):
    PROD = "PRODUCTION"
    STAGING = "STAGING"

@dataclass
class Config:
    env = Env.STAGING
    supabase_host = os.getenv("host","")
    supabase_key = os.getenv("key","")
    
    
config = Config()