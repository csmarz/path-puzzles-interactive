from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import solver

import json
import os
import glob

def index(request):
    return render(request, 'index.html')

@csrf_exempt
@require_http_methods(['POST'])
def solve(request):
    return JsonResponse(solver.solve_puzzle(json.loads(request.body.decode('utf-8'))))

@csrf_exempt
@require_http_methods(['GET'])
def case(request):
    data = []
    path = os.path.join(os.path.dirname(__file__), 'static', 'tc', '*.in')
    for filename in glob.glob(path):
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            m, n = map(int, f.readline().strip().split())
            start_x, start_y = map(int, f.readline().strip().split())
            finish_x, finish_y = map(int, f.readline().strip().split())
            start_x -= 1; start_y -= 1; finish_x -= 1; finish_y -= 1
            _ = f.readline()
            cr = list(map(int, f.readline().strip().split()))
            cc = list(map(int, f.readline().strip().split()))
            f.close()
        basename = os.path.basename(filename).split('.')[0]
        data.append({
            'name': basename, 
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
    return JsonResponse({
        'data': data
    })