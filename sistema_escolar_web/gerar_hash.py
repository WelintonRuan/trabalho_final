import bcrypt

# Defina a senha que você quer usar
senha_admin = "admin123"  # Altere para a senha desejada

# Gera o hash
hash_senha = bcrypt.hashpw(senha_admin.encode(), bcrypt.gensalt()).decode()

print(f"Login: admin")
print(f"Senha: {senha_admin}")
print(f"Hash para o SQL:\n'{hash_senha}'")