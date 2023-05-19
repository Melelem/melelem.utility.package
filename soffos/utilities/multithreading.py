from concurrent.futures import ThreadPoolExecutor, as_completed

def multithread(task: callable, items: list, **kwargs):

    with ThreadPoolExecutor(max_workers=len(items)) as executor:
        future_index = {
            executor.submit(task, item, **kwargs): i
                for i, item in enumerate(items)
        }

    results = {
        future_index[future]: future.result()
            for future in as_completed(future_index)
    }
    
    # Cast dictionary to list of tuples, sort by key (index) and return the second element (value) for each tuple
    return [i[1] for i in sorted(results.items())]