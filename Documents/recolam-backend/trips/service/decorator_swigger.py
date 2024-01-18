def custom_swagger_decorador(func):
    setattr(func, 'swagger_custom_info', {
        'description': 'Informacion adicional'
    })
    return func
