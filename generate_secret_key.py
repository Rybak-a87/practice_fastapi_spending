from secrets import token_urlsafe

secret_key = token_urlsafe(32)    # 32 случайных символа
print(secret_key)
