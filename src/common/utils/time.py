# -*- coding: utf-8 -*-
"""Time utils.

This module provides a time_it function that can be used to measure the time taken by a function to execute.
"""
import logging
import time


def time_it(funct: callable, logger: logging.Logger, name: str = "", **kwargs):
    """Decorator to estimate execution time.

    Examples:
        >>> time_it(name="My Function", func=my_function, arg1=arg1, arg2=arg2)
        My Function execution time: 0.0001 secs.
    """
    start = time.perf_counter()

    output = funct(**kwargs)

    end = time.perf_counter()

    total_time = end - start

    if total_time > 60:
        timed = f"{total_time // 60:.4f} mins {total_time % 60:.4f} secs"
    elif total_time > 1:
        timed = f"{total_time:.4f} secs"
    else:
        timed = f"{total_time * 1e3:.4f} ms"

    logger.info(f"{f'{name} e' if name else 'E'}xecution time: {timed}.")

    return output, total_time
