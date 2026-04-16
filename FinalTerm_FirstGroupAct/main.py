import random
import time
from multiprocessing import Process, Queue, Manager

# Sequential Merge Sort 
def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort(data):
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])
    return merge(left, right)

#  Parallel Merge Sort 
def sort_chunk(chunk, output, index):
    output[index] = merge_sort(chunk)

def parallel_merge_sort(data):
    manager = Manager()
    output = manager.dict()

    chunk_size = len(data) // 4
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    processes = []
    for i, chunk in enumerate(chunks):
        p = Process(target=sort_chunk, args=(chunk, output, i))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    # Merge sorted chunks
    sorted_data = output[0]
    for i in range(1, len(chunks)):
        sorted_data = merge(sorted_data, output[i])

    return sorted_data

# Sequential Linear Search 
def linear_search(data, target):
    for i in range(len(data)):
        if data[i] == target:
            return i
    return -1

#  Parallel Linear Search 
def worker(sub_data, target, q, offset):
    for i in range(len(sub_data)):
        if sub_data[i] == target:
            q.put(i + offset)
            return
    q.put(-1)

def parallel_search(data, target):
    q = Queue()
    chunk_size = len(data) // 4
    processes = []

    for i in range(0, len(data), chunk_size):
        sub_data = data[i:i + chunk_size]
        p = Process(target=worker, args=(sub_data, target, q, i))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    results = [q.get() for _ in processes]
    for r in results:
        if r != -1:
            return r
    return -1

# Testing
def test(size):
    print(f"\nDataset size: {size}")

    random_data = [random.randint(1, 1000000) for _ in range(size)]
    sorted_data = list(range(size))
    reverse_data = list(range(size, 0, -1))

    datasets = [
        ("Random", random_data),
        ("Sorted", sorted_data),
        ("Reverse", reverse_data)
    ]

    for name, data in datasets:
        print(f"\n--- {name} Data ---")
        target = data[-1]

        # Sequential Sort
        start = time.time()
        merge_sort(data.copy())
        print("Sequential Sort Time:", time.time() - start)

        # Parallel Sort
        start = time.time()
        parallel_merge_sort(data.copy())
        print("Parallel Sort Time:", time.time() - start)

        # Sequential Search
        start = time.time()
        linear_search(data, target)
        print("Sequential Search Time:", time.time() - start)

        # Parallel Search
        start = time.time()
        parallel_search(data, target)
        print("Parallel Search Time:", time.time() - start)

if __name__ == "__main__":
    for size in [1000, 100000, 1000000]:
        test(size)