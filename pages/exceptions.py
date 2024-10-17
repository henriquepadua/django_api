from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Chama o exception_handler padrão primeiro para obter a resposta inicial
    response = exception_handler(exc, context)

    if response is None:
        # Se o exception_handler padrão não tratou a exceção, retornamos uma resposta genérica
        return Response({'detail': 'Ocorreu um erro inesperado no servidor.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response