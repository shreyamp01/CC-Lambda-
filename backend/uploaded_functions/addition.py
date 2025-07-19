def handler(event):
    # This function is expected by the platform
    a = event.get("a", 0)
    b = event.get("b", 0)
    return {"result": a + b}
