
SAMPLE_CODES = {
    'linear_search': {
        'code': '''
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
''',
        'expected_complexity': 'O(n)'
    },
    
    'bubble_sort': {
        'code': '''
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
''',
        'expected_complexity': 'O(n²)'
    },
    
    'binary_search': {
        'code': '''
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
''',
        'expected_complexity': 'O(log n)'
    },
    
    'fibonacci_recursive': {
        'code': '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
''',
        'expected_complexity': 'O(2^n)'
    },
    
    'matrix_multiplication': {
        'code': '''
def matrix_multiply(A, B):
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    
    result = [[0] * cols_B for _ in range(rows_A)]
    
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    
    return result
''',
        'expected_complexity': 'O(n³)'
    }
} 