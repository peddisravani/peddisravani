from database import PRODUCTS
from ml.model import SIMILARITY
def get_recommendations(pid):
    ids=SIMILARITY.get(pid,[])
    return [p for p in PRODUCTS if p["id"] in ids]
