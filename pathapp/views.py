from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import solver

import json

def index(request):
    return render(request, 'index.html')

@csrf_exempt
@require_http_methods(['POST'])
def solve(request):
    return JsonResponse(solver.solve_puzzle(json.loads(request.body.decode('utf-8'))))