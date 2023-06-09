from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import solver

import json
import random
import string
import os

def index(request):
    return render(request, 'index.html')

@csrf_exempt
@require_http_methods(['POST'])
def solve(request):
    return JsonResponse(solver.solve_puzzle(json.loads(request.body.decode('utf-8'))))

@csrf_exempt
@require_http_methods(['GET'])
def case(request):
    letter = random.choice(string.ascii_lowercase)
    file_path = os.path.join(os.path.dirname(__file__), 'static', 'tc', f'{letter}.in')

    f = open(file_path)
    m, n = map(int, f.readline().strip().split())
    start_x, start_y = map(int, f.readline().strip().split())
    finish_x, finish_y = map(int, f.readline().strip().split())
    start_x -= 1; start_y -= 1; finish_x -= 1; finish_y -= 1
    _ = f.readline()
    cr = list(map(int, f.readline().strip().split()))
    cc = list(map(int, f.readline().strip().split()))
    f.close()

    return JsonResponse({
        'letter': letter, 
        'instance': {
            'm': m, 
            'n': n, 
            'start_x':start_x, 
            'start_y':start_y, 
            'finish_x':finish_x,
            'finish_y':finish_y,
            'cr':cr,
            'cc':cc,
        }
    })