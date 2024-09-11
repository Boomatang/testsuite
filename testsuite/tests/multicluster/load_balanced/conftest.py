"""Conftest for load-balanced multicluster tests"""

import pytest

from testsuite.kuadrant.policy.dns import DNSPolicy, LoadBalancing


@pytest.fixture(scope="package")
def dns_config(testconfig):
    """Configuration for DNS tests"""
    testconfig.validators.validate(only="dns")
    return testconfig["dns"]


@pytest.fixture(scope="package")
def dns_server(dns_config):
    """DNS server in the first geo region"""
    return dns_config["dns_server"]


@pytest.fixture(scope="package")
def dns_server2(dns_config):
    """DNS server in the second geo region"""
    return dns_config["dns_server2"]


@pytest.fixture(scope="module")
def dns_policy(blame, cluster, gateway, dns_server, module_label, dns_provider_secret):
    """DNSPolicy with load-balancing for the first cluster"""
    load_balancing = LoadBalancing(default_geo=dns_server["geo_code"], default_weight=10)
    return DNSPolicy.create_instance(
        cluster, blame("dns"), gateway, dns_provider_secret, load_balancing, labels={"app": module_label}
    )


@pytest.fixture(scope="module")
def dns_policy2(blame, cluster2, gateway2, dns_server, module_label, dns_provider_secret):
    """DNSPolicy with load-balancing for the second cluster"""
    load_balancing = LoadBalancing(default_geo=dns_server["geo_code"], default_weight=10)
    return DNSPolicy.create_instance(
        cluster2, blame("dns"), gateway2, dns_provider_secret, load_balancing, labels={"app": module_label}
    )