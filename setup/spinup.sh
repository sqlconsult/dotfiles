curl -X POST "https://api.digitalocean.com/v2/droplets" -d '{"region": "nyc3", "ssh_keys": ["18638077"], "tags": ["assessment"], "monitoring": "true", "name": "Phase-2", "image": "ubuntu-16-04-x64", "size": "1gb"}' -H "Authorization: Bearer 7b439befc034bebf3493852dc4578c79dfd6a4aeab06410cf06af77a0d49e9c1" -H "Content-Type: application/json" > spinup.log
