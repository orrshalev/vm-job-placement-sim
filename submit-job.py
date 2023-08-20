import argparse
from multiprocessing import Process
import time
import logging
import requests
import random

parser = argparse.ArgumentParser()
# parser.add_argument(
#     "-n",
#     "--n-jobs-max",
#     type=int,
#     help="Max number of jobs that can be accommodated on VM",
#     default=40,
# )
# parser.add_argument(
#     "-f",
#     "--failure-time",
#     type=int,
#     help="VM Failure time in seconds",
#     default=10,
# )
parser.add_argument(
    "-u",
    "--url",
    type=str,
    help="URL of job service",
    required=True,
)
parser.add_argument(
    "-c",
    "--completion",
    type=int,
    nargs=2,
    help="Job completion time in seconds",
    default=[5, 60],
)
parser.add_argument(
    "-e",
    "--evaluation-time",
    type=int,
    help="Time of evaluation in seconds",
    default=60 * 60 * 1,  # 1 hour
)
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="Enable info logging",
)
args = parser.parse_args()

# N_JOBS_MAX = args.n_jobs_max
# FAILURE_TIME = args.failure_time
# COMPLETION_TIME_UPPER, COMPLETION_TIME_LOWER = args.completion
COMPLETION_TIME_UPPER, COMPLETION_TIME_LOWER = args.completion
URL = args.url
EVALUATION_TIME = args.evaluation_time
if args.verbose:
    logging.basicConfig(level=logging.INFO)

# logging.info("N_JOBS_MAX: %d", N_JOBS_MAX)
# logging.info("FAILURE_TIME: %d", FAILURE_TIME)
logging.info("COMPLETION_TIME_UPPER: %d", COMPLETION_TIME_UPPER)
logging.info("COMPLETION_TIME_LOWER: %d", COMPLETION_TIME_LOWER)
logging.info("URL: %s", URL)
logging.info("EVALUATION_TIME: %d", EVALUATION_TIME)


def submit_job(url: str, completion_time: float):
    r = requests.post(
        f"{url}/job",
        json={
            "timeSeconds": completion_time,
        },
    )
    print(r.content)


# start_time = time.time()
# while time.time() - start_time < EVALUATION_TIME:
# for _ in range(400):
completion_time = random.uniform(COMPLETION_TIME_LOWER, COMPLETION_TIME_UPPER)
submit_job(URL, 1)
# time.sleep(0.01)
