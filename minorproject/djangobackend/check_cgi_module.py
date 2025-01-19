try:
    import cgi
    print("cgi module is available")
except ImportError:
    print("cgi module is not available")
