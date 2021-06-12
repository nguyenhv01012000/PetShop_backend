def correct_base_url(baseUrl: str):
    if baseUrl.endswith("/"):
        return baseUrl
    return baseUrl + "/"