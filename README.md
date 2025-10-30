## PyLogShipper-cf2os

### Overview
`PyLogShipper-cf2os` is a lightweight Python utility that transfers Cloudflare HTTP request logs to OpenSearch (or any Elasticsearch-compatible endpoint).
It serves as a connector between Cloudflare’s GraphQL log export API and your OpenSearch datastore, enabling you to efficiently collect, index, search, and visualize Cloudflare traffic data within your analytics stack.


### Features
- **Marketing Attribute Tracking** – Parsed URLs to extract and record key marketing parameters,, including Standard and Extended UTM tags, Google Ads (GCLID), Microsoft Ads (Bing), Facebook, LinkedIn, and Auto-Tagging parameters. These are then stored in OpenSearch for reporting and analytics. [Read more](docs/Marketing-attributes.md)
- Connects to **Cloudflare GraphQL API** export endpoints to **retrieve logs**.
- Supports **shipping** to OpenSearch / Elasticsearch endpoints via HTTP bulk API.
- Supports both **Basic** and **Premium (Bot Management / Enterprise)** field sets from the Cloudflare log schema. [Read more](docs/Cloudflare-fields.md)
- Batches and transforms log records into OpenSearch bulk-compatible format.
- **Dockerized** for easy deployment.
- Configuration via environment variables or `.env` file.
- Basic error handling, retry logic and logging.
- Sequence diagram for the [PyLogShipper-cf2os workflow](docs/assets/Diagram-Sequence.png)

### Use Cases
- Ingest Cloudflare HTTP request logs into OpenSearch for analytics and dashboards.
- Ship Cloudflare audit logs (account changes, firewall rule updates, etc.) into your search index.

### Getting Started

### Prerequisites
- A Cloudflare **Read-Only API access** is required, using a Read-Only API token that includes permissions for the Cloudflare GraphQL and Logs API.
Refer to [documentation](docs/Cloudflare-create-read-only-api-user.md) for detailed steps on how to generate this API token.
-  MaxMind **GeoLite2** databases for IP geolocation into the project directory at:

```
src/db/
```
see the [GeoLite2 Database Setup](docs/GeoLite2-Download.md).

- An OpenSearch (or Elasticsearch-compatible) endpoint accessible from the running container or host. [Sandbox OpenSearch Standalone](git@github.com:danydavila/POC-Elasticsearch-Opensearch.git) 
- [Docker & docker-compose](https://www.docker.com/) (if running via Docker), or Python 3.11+ (if running locally).

### Configuration

1. Copy the sample env file:

```bash
cp .env.example .env
```

2. Edit `.env` (or export environment variables) setting e.g.:

```
CLOUDFLARE_API_TOKEN=your_token
CLOUDFLARE_ACCOUNT_ID=your_account_id
CLOUDFLARE_ZONE_ID=your_zone_id
OPENSEARCH_ENDPOINT=https://your-opensearch.example.com:9200
OPENSEARCH_API_KEY=your_api_key_or_credentials
INDEX_NAME=cloudflare_logs
BATCH_SIZE=500
LOG_LEVEL=INFO
```

> Ensure the credentials and endpoints are correct and reachable.

### Running

#### via Docker

```bash
docker compose up
```

This will start the service, pick up logs from Cloudflare and ship them into OpenSearch.

#### via Python direct (for development)

```bash
pip install -r requirements.txt  
python src/pull-traffics.py
```

### Acknowledgements

Thanks to the Cloudflare and OpenSearch communities for their excellent APIs and tooling.
Inspired by log-shipping patterns common in security logging, observability and analytics.


Made with love ❤️