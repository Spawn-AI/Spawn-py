# Selas Python

Selas is a Python library for the [Selas](https://selas.ai) API. It provides a simple interface to the Selas API, allowing you to easily integrate Selas into your Python application.

You can find the full documentation for the Selas API [here](https://docs.selas.ai).

## Installation

Install the library using pip:

```bash
pip install selas
```

## Usage

### Authentication

To use the Selas API, you need to create an account and get your API key. You can do this by visiting the [Selas dashboard](https://selas.ai/dashboard).

Once you have your API key, you can authenticate with the Selas API by creating a `SelasClient` object:

```python
from selas import Client

client = SelasClient(
    app_id, key, secret
)
```

### Generating an image

To generate an image, you can use the `run_stable_diffusion` method:

```python
job = client.run_stable_diffusion(
    "a cute cat"
)
```

This will return a `{"job_id": str, costs: int}` object. You can use this job ID to get the image:

```python
image = client.get_result(job["job_id"])
```

This will return a `{"url": str}` object, where the URL points to the generated image.
