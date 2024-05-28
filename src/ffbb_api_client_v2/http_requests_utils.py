import json
import time
from typing import Any, Dict
from urllib.parse import urlencode

import requests
from requests import Response
from requests_cache import CachedSession


def to_json_from_response(response: Response) -> Dict[str, Any]:
    """
    Converts the HTTP response to a JSON dictionary.

    Args:
        response (Response): The HTTP response.

    Returns:
        Dict[str, Any]: The JSON dictionary extracted from the response.
    """
    data_str = response.text.strip()

    try:
        return json.loads(data_str)
    except json.JSONDecodeError:
        pass

    if data_str.endswith(","):
        data_str = data_str[:-1]

    data_str = data_str.replace("][", ",")
    data_str = data_str.replace("KO", "")

    if data_str.startswith('""'):
        data_str = data_str[2:]

    return json.loads(data_str)


def http_get(
    url: str,
    headers: Dict[str, str],
    debug: bool = False,
    cached_session: CachedSession = None,
    timeout: int = 20,
) -> Response:
    """
    Performs an HTTP GET request.

    Args:
        url (str): The URL of the request.
        headers (Dict[str, str]): The headers of the request.
        debug (bool): Whether to enable debug mode or not. Default is False.
        use_cache (bool): Whether to use cache or not. Default is True.
        timeout (int): The timeout value in seconds. Default is 20.

    Returns:
        Response: The HTTP response.
    """
    if debug:
        print(f"Making GET request to {url}")
        start_time = time.time()

    if cached_session:
        response = cached_session.get(url, headers=headers, timeout=timeout)
    else:
        response = requests.get(url, headers=headers, timeout=timeout)

    if debug:
        end_time = time.time()
        print(f"GET request to {url} took {end_time - start_time} seconds.")

    return response


def http_post(
    url: str,
    headers: Dict[str, str],
    data: Dict[str, Any] = None,
    debug: bool = False,
    cached_session: CachedSession = None,
    timeout: int = 20,
) -> Response:
    """
    Performs an HTTP POST request.

    Args:
        url (str): The URL of the request.
        headers (Dict[str, str]): The headers of the request.
        data (Dict[str, Any]): The data of the request.
        debug (bool): Whether to enable debug mode or not. Default is False.
        use_cache (bool): Whether to use cache or not. Default is True.
        timeout (int): The timeout value in seconds. Default is 20.

    Returns:
        Response: The HTTP response.
    """
    if debug:
        data_str = ", ".join([f"{k}:{v}" for k, v in data.items()]) if data else ""
        print(f"Making POST request to {url} {data_str}")
        start_time = time.time()

    if cached_session:
        response = cached_session.post(url, headers=headers, data=data, timeout=timeout)
    else:
        response = requests.post(url, headers=headers, data=data, timeout=timeout)

    if debug:
        end_time = time.time()
        print(f"POST request to {url} {data_str} took {end_time - start_time} seconds.")

    return response


def http_get_json(
    url: str,
    headers: Dict[str, str],
    debug: bool = False,
    cached_session: CachedSession = None,
    timeout: int = 20,
) -> Dict[str, Any]:
    """
    Performs an HTTP GET request and returns the result in JSON format.

    Args:
        url (str): The URL of the request.
        headers (Dict[str, str]): The headers of the request.
        debug (bool): Whether to enable debug mode or not. Default is False.
        use_cache (bool): Whether to use cache or not. Default is True.
        timeout (int): The timeout value in seconds. Default is 20.

    Returns:
        Dict[str, Any]: The result of the request in JSON format.
    """
    response = http_get(
        url, headers, debug=debug, cached_session=cached_session, timeout=timeout
    )
    return to_json_from_response(response)


def http_post_json(
    url: str,
    headers: Dict[str, str],
    data: Dict[str, Any] = None,
    debug: bool = False,
    cached_session: CachedSession = None,
    timeout: int = 20,
) -> Dict[str, Any]:
    """
    Performs an HTTP POST request and returns the result in JSON format.

    Args:
        url (str): The URL of the request.
        headers (Dict[str, str]): The headers of the request.
        data (Dict[str, Any]): The data of the request.
        debug (bool): Whether to enable debug mode or not. Default is False.
        use_cache (bool): Whether to use cache or not. Default is True.
        timeout (int): The timeout value in seconds. Default is 20.

    Returns:
        Dict[str, Any]: The result of the request in JSON format.
    """
    filtered_data = {k: v for k, v in data.items() if v is not None} if data else None
    response = http_post(
        url,
        headers,
        filtered_data,
        debug=debug,
        cached_session=cached_session,
        timeout=timeout,
    )
    return to_json_from_response(response)


def encode_params(params: Dict[str, Any]) -> str:
    """
    Encodes the request parameters into a query string.

    Args:
        params (Dict[str, Any]): The request parameters.

    Returns:
        str: The encoded query string.
    """
    encoded_params = urlencode({k: v for k, v in params.items() if v is not None})
    return encoded_params


def url_with_params(url: str, params: Dict[str, Any]) -> str:
    """
    Adds the request parameters to the URL.

    Args:
        url (str): The URL of the request.
        params (Dict[str, Any]): The request parameters.

    Returns:
        str: The URL with the request parameters.
    """
    encoded_params = encode_params(params)
    if encoded_params:
        return f"{url}?{encoded_params}"
    else:
        return url
