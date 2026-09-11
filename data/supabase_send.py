import pandas as pd
from supabase import create_client
import tomllib  


with open("./.streamlit/secrets.toml", "rb") as f:
    secrets = tomllib.load(f)

supabase = create_client(secrets["SUPABASE_URL"], secrets["SUPABASE_KEY"])

df = pd.read_pickle("data/no_bloom.pkl")

records = df.rename(columns={
    "ID": "id",
    "Question": "question",
    "Section": "section",
    "Type": "type",
    "Subskill": "subskill",
    "Keywords": "keywords",
    "Question Total": "question_total",
    "Count": "count",
}).to_dict(orient="records")

supabase.table("ieb_exams").insert(records).execute()