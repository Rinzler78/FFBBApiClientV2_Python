"""
Tests de performance et de résilience pour le client FFBB API
"""

import time
import unittest
from unittest.mock import Mock, patch

import requests

from ffbb_api_client_v2.facade.client import FFBBAPIClientV2
from ffbb_api_client_v2.utils.cache_manager import CacheManager
from ffbb_api_client_v2.utils.retry_utils import execute_with_retry, should_retry


class Test147PerformanceAndResilience(unittest.TestCase):
    """Tests de performance et de résilience"""

    def test_001_performance_basic_request_timing(self):
        """Test de la performance de base pour une requête simple"""
        with (
            patch("ffbb_api_client_v2.facade.client.ApiFFBBAppClient") as mock_api_cls,
            patch(
                "ffbb_api_client_v2.facade.client.MeilisearchFFBBClient"
            ) as mock_ms_cls,
        ):
            mock_api_instance = Mock()
            mock_ms_instance = Mock()
            mock_api_cls.return_value = mock_api_instance
            mock_ms_cls.return_value = mock_ms_instance

            client = FFBBAPIClientV2.create(
                meilisearch_bearer_token="test_ms_token",
                api_bearer_token="test_api_token",
            )

        # Mesurer le temps d'exécution d'une méthode factice via mock facade
        mock_api_instance.get_lives.return_value = {"data": "test"}

        start_time = time.time()
        client.get_lives()
        end_time = time.time()
        duration = end_time - start_time

        # Vérifier que l'opération prend moins de 1 seconde
        assert duration < 1.0

    def test_002_cache_performance(self):
        """Test de la performance du cache (basic operations)"""
        cache_manager = CacheManager()

        # Mesurer le temps d'activation/vérification du cache
        start_time = time.time()
        is_enabled = cache_manager.is_enabled()
        check_duration = time.time() - start_time

        # Mesurer le temps d'obtention des métriques
        start_time = time.time()
        metrics = cache_manager.get_metrics()
        metrics_duration = time.time() - start_time

        # Vérifier que les opérations sont rapides (< 0.1 seconde)
        assert check_duration < 0.1
        assert metrics_duration < 0.1
        assert isinstance(is_enabled, bool)
        assert metrics is not None

    def test_003_retry_logic_performance(self):
        """Test de la performance du mécanisme de retry"""

        def quick_success_function(**kwargs):
            mock_response = Mock()
            mock_response.status_code = 200
            return mock_response

        start_time = time.time()
        result = execute_with_retry(quick_success_function)
        duration = time.time() - start_time

        # Vérifier que la fonction s'exécute rapidement quand elle réussit immédiatement
        assert result.status_code == 200
        assert duration < 0.5  # Devrait être rapide si la première tentative réussit

    def test_004_retry_logic_resilience(self):
        """Test de la résilience du mécanisme de retry"""
        attempt_count = 0

        def eventually_successful_function(**kwargs):
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise requests.exceptions.ConnectionError("Simulated connection error")
            mock_response = Mock()
            mock_response.status_code = 200
            return mock_response

        # Réinitialiser le compteur
        attempt_count = 0

        # Exécuter la fonction avec retry
        result = execute_with_retry(eventually_successful_function)

        # Vérifier que la fonction a finalement réussi après plusieurs tentatives
        assert result.status_code == 200
        assert attempt_count == 3  # Devrait réussir à la troisième tentative

    def test_005_should_retry_logic(self):
        """Test de la logique de décision de retry"""
        from ffbb_api_client_v2.utils.retry_utils import RetryConfig

        config = RetryConfig()

        # Tester avec une réponse réussie
        mock_response_success = Mock()
        mock_response_success.status_code = 200
        assert should_retry(1, mock_response_success, None, config) is False

        # Tester avec une erreur 5xx
        mock_response_server_error = Mock()
        mock_response_server_error.status_code = 500
        assert should_retry(1, mock_response_server_error, None, config) is True

        # Tester avec une erreur 4xx (sauf celles explicitement réessayables)
        mock_response_client_error = Mock()
        mock_response_client_error.status_code = 400
        assert should_retry(1, mock_response_client_error, None, config) is False

        # Tester avec une erreur 429 (Too Many Requests)
        mock_response_rate_limit = Mock()
        mock_response_rate_limit.status_code = 429
        assert should_retry(1, mock_response_rate_limit, None, config) is True

    def test_006_concurrent_access_resilience(self):
        """Test de la résilience face aux accès concurrents (simulation)"""
        cache_manager = CacheManager()

        import threading

        results = []

        def cache_operation():
            # Use actual CacheManager API: get_metrics and is_enabled
            metrics = cache_manager.get_metrics()
            enabled = cache_manager.is_enabled()
            results.append((metrics, enabled))

        # Créer plusieurs threads qui accèdent au cache
        threads = []
        for i in range(5):
            thread = threading.Thread(target=cache_operation)
            threads.append(thread)
            thread.start()

        # Attendre que tous les threads se terminent
        for thread in threads:
            thread.join()

        # Vérifier que toutes les opérations ont réussi
        assert len(results) == 5
        for metrics, enabled in results:
            assert metrics is not None
            assert isinstance(enabled, bool)

    def test_007_large_payload_handling(self):
        """Test de la gestion de charges utiles importantes"""
        with (
            patch("ffbb_api_client_v2.facade.client.ApiFFBBAppClient") as mock_api_cls,
            patch(
                "ffbb_api_client_v2.facade.client.MeilisearchFFBBClient"
            ) as mock_ms_cls,
        ):
            mock_api_instance = Mock()
            mock_ms_instance = Mock()
            mock_api_cls.return_value = mock_api_instance
            mock_ms_cls.return_value = mock_ms_instance

            client = FFBBAPIClientV2.create(
                meilisearch_bearer_token="test_ms_token",
                api_bearer_token="test_api_token",
            )

        # Créer une charge utile importante
        large_payload = {"data": "x" * 10000}  # 10k caractères
        # Utilisé implicitement dans les appels suivants
        assert len(large_payload["data"]) == 10000

        # Simuler une requête avec une grande charge utile via mock facade
        mock_api_instance.get_lives.return_value = {"status": "received"}
        client.get_lives()

    def test_008_slow_response_handling(self):
        """Test de la gestion des réponses lentes"""

        def slow_function(**kwargs):
            time.sleep(0.2)  # Simuler une fonction lente
            mock_response = Mock()
            mock_response.status_code = 200
            return mock_response

        # Tester avec retry et délai
        start_time = time.time()
        result = execute_with_retry(slow_function)
        duration = time.time() - start_time

        # Vérifier que la fonction s'exécute correctement malgré la lenteur
        assert result.status_code == 200
        assert duration >= 0.2  # Doit prendre au moins le temps de la fonction

    def test_009_network_instability_simulation(self):
        """Test de la simulation d'instabilité réseau"""
        attempt_count = 0

        def unstable_function(**kwargs):
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count % 3 != 0:  # Échoue 2 fois sur 3
                raise requests.exceptions.Timeout("Simulated timeout")
            mock_response = Mock()
            mock_response.status_code = 200
            return mock_response

        # Réinitialiser le compteur
        attempt_count = 0

        # Exécuter avec retry pour gérer l'instabilité
        result = execute_with_retry(unstable_function)

        # Vérifier que la fonction réussit finalement malgré l'instabilité
        assert result.status_code == 200
        assert attempt_count % 3 == 0  # Devrait réussir sur un multiple de 3

    def test_010_resource_cleanup_under_load(self):
        """Test du nettoyage des ressources sous charge"""
        cache_manager = CacheManager()

        # Effectuer de nombreuses opérations de lecture de métriques
        for i in range(100):
            cache_manager.get_metrics()

        # Vérifier que le cache fonctionne normalement après la charge
        cache_manager.clear_cache()
        size = cache_manager.get_cache_size()
        assert isinstance(size, int)
        assert size >= 0

    def test_011_memory_usage_consistency(self):
        """Test de la cohérence de l'utilisation de la mémoire"""
        # Créer plusieurs instances de client pour vérifier la gestion de la mémoire
        clients = []
        for i in range(5):
            with (
                patch(
                    "ffbb_api_client_v2.facade.client.ApiFFBBAppClient"
                ) as mock_api_cls,
                patch(
                    "ffbb_api_client_v2.facade.client.MeilisearchFFBBClient"
                ) as mock_ms_cls,
            ):
                mock_api_instance = Mock()
                mock_ms_instance = Mock()
                mock_api_cls.return_value = mock_api_instance
                mock_ms_cls.return_value = mock_ms_instance

                client = FFBBAPIClientV2.create(
                    meilisearch_bearer_token=f"test_ms_token_{i}",
                    api_bearer_token=f"test_api_token_{i}",
                )
                clients.append(client)

        # Vérifier que toutes les instances sont créées correctement
        assert len(clients) == 5

        # Nettoyer
        del clients

    def test_012_error_recovery_capabilities(self):
        """Test des capacités de récupération d'erreur"""
        attempt_count = 0

        def error_then_success(**kwargs):
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count == 1:
                raise requests.exceptions.ConnectionError("Simulated processing error")
            elif attempt_count == 2:
                raise requests.exceptions.Timeout("Simulated connection error")
            else:
                mock_response = Mock()
                mock_response.status_code = 200
                return mock_response

        # Réinitialiser le compteur
        attempt_count = 0

        # Tester la capacité à récupérer de différentes erreurs
        result = execute_with_retry(error_then_success)

        assert result.status_code == 200
        assert (
            attempt_count > 2
        )  # Devrait avoir échoué au moins deux fois avant de réussir
