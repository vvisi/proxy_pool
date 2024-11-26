#!/bin/bash
docker exec -it proxy_pool sh -c 'rm -rf /app/log/checker.log'
docker exec -it proxy_pool sh -c 'rm -rf /app/log/fetcher.log'
