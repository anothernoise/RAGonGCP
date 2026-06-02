from ragongcp.ingestion.sources.web import host_allowed


def test_host_allowed_exact_match():
    allow = ["bcfsa.ca", "www.bcfsa.ca"]
    assert host_allowed("https://www.bcfsa.ca/x", allow)
    assert host_allowed("https://bcfsa.ca/y", allow)


def test_host_not_allowed():
    allow = ["bcfsa.ca"]
    assert not host_allowed("https://evil.example.com/x", allow)
    # subdomain not explicitly listed is rejected
    assert not host_allowed("https://sub.bcfsa.ca/x", allow)
