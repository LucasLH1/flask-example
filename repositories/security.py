import hashlib

#on sépare les fonctions même si identifiques pour respecter les principes SOLID
#les regrouper servirait le principe DRY mais en cas de perspective d'évolution, autant séparer les deux
def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def generate_sha256_id(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()
